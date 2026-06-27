"""
AI API Endpoints

REST API for the Master AI Orchestrator system.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import uuid

from app.core.security import verify_token

router = APIRouter(prefix="/ai", tags=["AI Orchestrator"])


# ==================== REQUEST MODELS ====================

class ChatRequest(BaseModel):
    """Chat request model."""
    message: str = Field(..., min_length=1, max_length=10000)
    context: Optional[Dict[str, Any]] = None
    model: Optional[str] = None
    stream: bool = False


class WorkflowRequest(BaseModel):
    """Workflow execution request."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    tasks: List[Dict[str, Any]] = Field(..., min_items=1)
    variables: Optional[Dict[str, Any]] = None


class TaskRequest(BaseModel):
    """Single task execution request."""
    task_type: str = Field(..., min_length=1)
    input_data: Dict[str, Any] = Field(default_factory=dict)
    agent_id: Optional[str] = None
    model: Optional[str] = None


class PromptRenderRequest(BaseModel):
    """Prompt template rendering request."""
    template_name: str
    variables: Dict[str, Any] = Field(default_factory=dict)


# ==================== RESPONSE MODELS ====================

class ChatResponse(BaseModel):
    """Chat response model."""
    request_id: str
    success: bool
    content: Optional[str] = None
    model: Optional[str] = None
    provider: Optional[str] = None
    tokens_used: int = 0
    cost_usd: float = 0.0
    execution_time_ms: float = 0.0
    metadata: Optional[Dict[str, Any]] = None


class WorkflowResponse(BaseModel):
    """Workflow execution response."""
    workflow_id: str
    status: str
    tasks: Dict[str, Any]
    total_cost_usd: float = 0.0


class AgentResponse(BaseModel):
    """Agent information response."""
    id: str
    name: str
    display_name: str
    agent_type: str
    status: str
    health_status: str
    active_executions: int
    success_rate: float


class ModelResponse(BaseModel):
    """Model information response."""
    provider: str
    model_id: str
    display_name: str
    cost_per_1k_tokens: float
    average_latency_ms: float
    quality_score: float
    capabilities: List[str]


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    components: Dict[str, str]
    timestamp: str


class MetricsResponse(BaseModel):
    """Metrics response."""
    total_executions: int
    success_rate: float
    total_cost_usd: float
    average_execution_time_ms: float


# ==================== ENDPOINTS ====================

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user_id: str = Depends(verify_token)
):
    """
    Send a chat message to the AI Orchestrator.
    
    The orchestrator will:
    1. Analyze the request
    2. Select the best model
    3. Execute the request
    4. Perform quality checks
    5. Return the response
    """
    from app.services.ai.orchestrator import orchestrator, AIRequest, RequestType
    
    await orchestrator.initialize()
    
    ai_request = AIRequest(
        id=str(uuid.uuid4()),
        request_type=RequestType.CHAT,
        user_id=current_user_id,
        organization_id=None,
        workspace_id=None,
        prompt=request.message,
        context=request.context or {},
        constraints={"model": request.model} if request.model else {},
        metadata={}
    )
    
    response = await orchestrator.process_request(ai_request)
    
    return ChatResponse(
        request_id=response.request_id,
        success=response.success,
        content=response.output.get("content") if isinstance(response.output, dict) else str(response.output),
        model=response.output.get("model") if isinstance(response.output, dict) else None,
        provider=response.output.get("provider") if isinstance(response.output, dict) else None,
        tokens_used=response.tokens_used,
        cost_usd=response.cost_usd,
        execution_time_ms=response.execution_time_ms,
        metadata=response.metadata
    )


@router.post("/workflow", response_model=WorkflowResponse)
async def execute_workflow(
    request: WorkflowRequest,
    current_user_id: str = Depends(verify_token)
):
    """
    Execute a multi-step AI workflow.
    
    Workflows support:
    - Sequential task execution
    - Parallel task execution
    - Dependency resolution
    - Automatic retries
    """
    from app.services.ai.workflow import workflow_engine
    
    await workflow_engine.initialize()
    
    workflow_id = await workflow_engine.create_workflow(
        name=request.name,
        description=request.description or "",
        workflow_type="api",
        tasks=request.tasks,
        variables=request.variables
    )
    
    result = await workflow_engine.execute_workflow(
        workflow_id=workflow_id,
        variables=request.variables
    )
    
    # Calculate total cost from task results
    total_cost = 0.0
    for task_id, task_data in result.get("tasks", {}).items():
        output = task_data.get("output", {})
        if isinstance(output, dict):
            total_cost += output.get("cost", 0.0)
    
    return WorkflowResponse(
        workflow_id=workflow_id,
        status=result.get("status", "unknown"),
        tasks=result.get("tasks", {}),
        total_cost_usd=round(total_cost, 6)
    )


@router.post("/execute", response_model=ChatResponse)
async def execute_task(
    request: TaskRequest,
    current_user_id: str = Depends(verify_token)
):
    """
    Execute a single AI task.
    
    The task will be routed to the best agent and model.
    """
    from app.services.ai.orchestrator import orchestrator, AIRequest, RequestType
    
    await orchestrator.initialize()
    
    ai_request = AIRequest(
        id=str(uuid.uuid4()),
        request_type=RequestType.TASK,
        user_id=current_user_id,
        organization_id=None,
        workspace_id=None,
        prompt=request.task_type,
        context=request.input_data,
        constraints={
            "agent_id": request.agent_id,
            "model": request.model
        },
        metadata={}
    )
    
    response = await orchestrator.process_request(ai_request)
    
    return ChatResponse(
        request_id=response.request_id,
        success=response.success,
        content=response.output.get("content") if isinstance(response.output, dict) else str(response.output),
        tokens_used=response.tokens_used,
        cost_usd=response.cost_usd,
        execution_time_ms=response.execution_time_ms,
        metadata=response.metadata
    )


@router.get("/agents", response_model=List[AgentResponse])
async def list_agents(
    current_user_id: str = Depends(verify_token)
):
    """
    List all registered AI agents.
    """
    from app.services.ai.registry import agent_registry
    
    await agent_registry.initialize()
    
    agents = []
    for agent in agent_registry.agents.values():
        agents.append(AgentResponse(
            id=agent.id,
            name=agent.name,
            display_name=agent.display_name,
            agent_type=agent.agent_type,
            status="active" if agent.is_active else "inactive",
            health_status=agent.health_status.value,
            active_executions=agent.active_executions,
            success_rate=agent.success_rate
        ))
    
    return agents


@router.get("/agents/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: str,
    current_user_id: str = Depends(verify_token)
):
    """
    Get details of a specific AI agent.
    """
    from app.services.ai.registry import agent_registry
    
    await agent_registry.initialize()
    
    agent = await agent_registry.get_agent(agent_id)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    return AgentResponse(
        id=agent.id,
        name=agent.name,
        display_name=agent.display_name,
        agent_type=agent.agent_type,
        status="active" if agent.is_active else "inactive",
        health_status=agent.health_status.value,
        active_executions=agent.active_executions,
        success_rate=agent.success_rate
    )


@router.get("/models", response_model=List[ModelResponse])
async def list_models(
    current_user_id: str = Depends(verify_token)
):
    """
    List all available AI models.
    """
    from app.services.ai.router import router
    
    await router.initialize()
    
    models = []
    for model in router.models.values():
        if model.is_available:
            models.append(ModelResponse(
                provider=model.provider,
                model_id=model.model_id,
                display_name=model.model_name,
                cost_per_1k_tokens=model.cost_per_1k_tokens,
                average_latency_ms=model.average_latency_ms,
                quality_score=model.quality_score,
                capabilities=model.capabilities
            ))
    
    return models


@router.post("/prompts/render")
async def render_prompt(
    request: PromptRenderRequest,
    current_user_id: str = Depends(verify_token)
):
    """
    Render a prompt template with variables.
    """
    from app.services.ai.prompts import prompt_library
    
    await prompt_library.initialize()
    
    template = await prompt_library.get_template(name=request.template_name)
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    try:
        result = await prompt_library.render(
            template_id=template.id,
            variables=request.variables
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Check health of all AI components.
    """
    from app.services.ai.orchestrator import orchestrator
    
    await orchestrator.initialize()
    
    status_info = orchestrator.get_status()
    
    components = {}
    for service, initialized in status_info.get("services", {}).items():
        components[service] = "healthy" if initialized else "unhealthy"
    
    overall_status = "healthy" if all(v == "healthy" for v in components.values()) else "degraded"
    
    return HealthResponse(
        status=overall_status,
        components=components,
        timestamp=datetime.now(timezone.utc).isoformat()
    )


@router.get("/metrics", response_model=MetricsResponse)
async def get_metrics(
    current_user_id: str = Depends(verify_token)
):
    """
    Get AI system metrics.
    """
    from app.services.ai.orchestrator import orchestrator
    
    await orchestrator.initialize()
    
    metrics = orchestrator.get_metrics()
    
    return MetricsResponse(
        total_executions=metrics.get("total_executions", 0),
        success_rate=metrics.get("success_rate", 0.0),
        total_cost_usd=metrics.get("total_cost_usd", 0.0),
        average_execution_time_ms=metrics.get("average_execution_time_ms", 0.0)
    )


@router.get("/memory/stats")
async def get_memory_stats(
    current_user_id: str = Depends(verify_token)
):
    """
    Get memory system statistics.
    """
    from app.services.ai.memory import memory_engine
    
    await memory_engine.initialize()
    
    return memory_engine.get_stats()


@router.get("/quality/stats")
async def get_quality_stats(
    current_user_id: str = Depends(verify_token)
):
    """
    Get quality engine statistics.
    """
    from app.services.ai.quality import quality_engine
    
    await quality_engine.initialize()
    
    return quality_engine.get_quality_stats()
