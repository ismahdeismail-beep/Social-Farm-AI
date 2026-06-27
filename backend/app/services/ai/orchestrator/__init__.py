"""
Master AI Orchestrator Service

The central brain of the AI system.
Coordinates planning, reasoning, delegation, agent selection,
workflow execution, monitoring, recovery, and learning.
"""

from typing import Optional, Dict, Any, List, AsyncGenerator
from datetime import datetime, timezone
from dataclasses import dataclass, field
from enum import Enum
import logging
import asyncio
import json

logger = logging.getLogger(__name__)


class OrchestratorState(Enum):
    """Orchestrator state."""
    IDLE = "idle"
    PLANNING = "planning"
    EXECUTING = "executing"
    MONITORING = "monitoring"
    RECOVERING = "recovering"
    LEARNING = "learning"


class RequestType(Enum):
    """Types of AI requests."""
    CHAT = "chat"
    WORKFLOW = "workflow"
    TASK = "task"
    ANALYSIS = "analysis"
    CREATION = "creation"
    RESEARCH = "research"


@dataclass
class AIRequest:
    """Incoming AI request."""
    id: str
    request_type: RequestType
    user_id: str
    organization_id: Optional[str]
    workspace_id: Optional[str]
    prompt: str
    context: Dict[str, Any]
    constraints: Dict[str, Any]
    metadata: Dict[str, Any]
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class ExecutionPlan:
    """Plan for executing a request."""
    request_id: str
    tasks: List[Dict[str, Any]]
    estimated_cost: float
    estimated_duration_ms: int
    required_agents: List[str]
    required_models: List[str]
    risk_assessment: str


@dataclass
class OrchestratorResponse:
    """Response from the orchestrator."""
    request_id: str
    success: bool
    output: Any
    metadata: Dict[str, Any]
    execution_time_ms: float
    cost_usd: float
    tokens_used: int
    agents_used: List[str]
    models_used: List[str]


class MasterOrchestrator:
    """
    Master AI Orchestrator - The Central Brain
    
    Responsibilities:
    - Planning: Analyze requests and create execution plans
    - Reasoning: Determine best approach for each task
    - Delegation: Assign tasks to appropriate agents
    - Agent Selection: Choose the best agent for each task
    - Workflow Execution: Coordinate multi-step workflows
    - Monitoring: Track execution progress
    - Recovery: Handle failures and retries
    - Learning: Improve from feedback and outcomes
    """
    
    def __init__(self):
        self.state = OrchestratorState.IDLE
        self.active_requests: Dict[str, AIRequest] = {}
        self.execution_history: List[Dict[str, Any]] = []
        self.learning_data: Dict[str, Any] = {}
        
        # Service references (will be injected)
        self.gateway = None
        self.router = None
        self.memory_engine = None
        self.prompt_library = None
        self.agent_registry = None
        self.workflow_engine = None
        self.quality_engine = None
        
        self._initialized = False
    
    async def initialize(self):
        """Initialize the orchestrator and all sub-services."""
        if self._initialized:
            return
        
        # Import services
        from app.services.ai.gateway import gateway
        from app.services.ai.router import router
        from app.services.ai.memory import memory_engine
        from app.services.ai.prompts import prompt_library
        from app.services.ai.registry import agent_registry
        from app.services.ai.workflow import workflow_engine
        from app.services.ai.quality import quality_engine
        
        self.gateway = gateway
        self.router = router
        self.memory_engine = memory_engine
        self.prompt_library = prompt_library
        self.agent_registry = agent_registry
        self.workflow_engine = workflow_engine
        self.quality_engine = quality_engine
        
        # Initialize all services
        await asyncio.gather(
            self.gateway.initialize(),
            self.router.initialize(),
            self.memory_engine.initialize(),
            self.prompt_library.initialize(),
            self.agent_registry.initialize(),
            self.workflow_engine.initialize(),
            self.quality_engine.initialize()
        )
        
        self._initialized = True
        logger.info("Master AI Orchestrator initialized")
    
    async def process_request(
        self,
        request: AIRequest
    ) -> OrchestratorResponse:
        """
        Process an AI request through the full orchestration pipeline.
        
        Pipeline:
        1. Analyze request
        2. Create execution plan
        3. Select agents
        4. Execute workflow
        5. Quality check
        6. Return response
        """
        start_time = datetime.now(timezone.utc)
        
        try:
            self.state = OrchestratorState.PLANNING
            self.active_requests[request.id] = request
            
            # Step 1: Analyze request and create plan
            plan = await self._create_execution_plan(request)
            
            # Step 2: Store context in memory
            await self._store_context(request)
            
            # Step 3: Execute based on request type
            if request.request_type == RequestType.CHAT:
                result = await self._execute_chat(request, plan)
            elif request.request_type == RequestType.WORKFLOW:
                result = await self._execute_workflow(request, plan)
            elif request.request_type == RequestType.TASK:
                result = await self._execute_task(request, plan)
            else:
                result = await self._execute_generic(request, plan)
            
            # Step 4: Quality check
            quality_result = await self._quality_check(result, request.context)
            
            # Step 5: Learn from execution
            await self._learn_from_execution(request, result, quality_result)
            
            # Calculate metrics
            execution_time = (datetime.now(timezone.utc) - start_time).total_seconds() * 1000
            
            response = OrchestratorResponse(
                request_id=request.id,
                success=True,
                output=result,
                metadata={
                    "plan": {
                        "tasks": len(plan.tasks),
                        "estimated_cost": plan.estimated_cost,
                        "risk": plan.risk_assessment
                    },
                    "quality": {
                        "score": quality_result.overall_score,
                        "passed": quality_result.passed
                    }
                },
                execution_time_ms=execution_time,
                cost_usd=plan.estimated_cost,
                tokens_used=result.get("tokens_used", 0) if isinstance(result, dict) else 0,
                agents_used=plan.required_agents,
                models_used=plan.required_models
            )
            
            # Record execution
            self.execution_history.append({
                "request_id": request.id,
                "request_type": request.request_type.value,
                "success": True,
                "execution_time_ms": execution_time,
                "cost_usd": plan.estimated_cost,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
            
            return response
            
        except Exception as e:
            logger.error(f"Orchestrator error: {e}")
            
            execution_time = (datetime.now(timezone.utc) - start_time).total_seconds() * 1000
            
            return OrchestratorResponse(
                request_id=request.id,
                success=False,
                output=None,
                metadata={"error": str(e)},
                execution_time_ms=execution_time,
                cost_usd=0.0,
                tokens_used=0,
                agents_used=[],
                models_used=[]
            )
        
        finally:
            self.active_requests.pop(request.id, None)
            self.state = OrchestratorState.IDLE
    
    async def _create_execution_plan(
        self,
        request: AIRequest
    ) -> ExecutionPlan:
        """Create an execution plan for the request."""
        
        # Analyze request complexity
        complexity = self._analyze_complexity(request)
        
        # Determine required capabilities
        required_capabilities = self._determine_capabilities(request)
        
        # Estimate tasks
        tasks = await self._decompose_into_tasks(request, required_capabilities)
        
        # Estimate cost and duration
        estimated_cost = sum(t.get("estimated_cost", 0.001) for t in tasks)
        estimated_duration = sum(t.get("estimated_duration_ms", 1000) for t in tasks)
        
        # Select agents
        required_agents = []
        for task in tasks:
            agent = await self.agent_registry.select_agent(
                task_type=task.get("task_type", "chat"),
                require_healthy=True
            )
            if agent:
                required_agents.append(agent.id)
                task["assigned_agent"] = agent.id
        
        # Select models
        required_models = []
        for task in tasks:
            model = await self.router.route(
                task_type=task.get("task_type", "chat"),
                requirements=task.get("requirements")
            )
            if model:
                required_models.append(f"{model.provider}:{model.model_id}")
                task["assigned_model"] = f"{model.provider}:{model.model_id}"
        
        # Risk assessment
        risk = "low"
        if estimated_cost > 0.1:
            risk = "medium"
        if estimated_cost > 1.0:
            risk = "high"
        
        return ExecutionPlan(
            request_id=request.id,
            tasks=tasks,
            estimated_cost=estimated_cost,
            estimated_duration_ms=estimated_duration,
            required_agents=list(set(required_agents)),
            required_models=list(set(required_models)),
            risk_assessment=risk
        )
    
    def _analyze_complexity(self, request: AIRequest) -> str:
        """Analyze request complexity."""
        prompt_length = len(request.prompt)
        has_context = bool(request.context)
        has_constraints = bool(request.constraints)
        
        if prompt_length > 1000 or (has_context and len(request.context) > 5):
            return "high"
        elif prompt_length > 500 or has_context:
            return "medium"
        return "low"
    
    def _determine_capabilities(self, request: AIRequest) -> List[str]:
        """Determine required capabilities for the request."""
        capabilities = ["chat"]  # Default
        
        prompt_lower = request.prompt.lower()
        
        if any(word in prompt_lower for word in ["research", "find", "search", "look up"]):
            capabilities.append("research")
        if any(word in prompt_lower for word in ["create", "write", "generate", "draft"]):
            capabilities.append("content_creation")
        if any(word in prompt_lower for word in ["analyze", "analysis", "review"]):
            capabilities.append("analysis")
        if any(word in prompt_lower for word in ["image", "picture", "photo", "thumbnail"]):
            capabilities.append("image_generation")
        if any(word in prompt_lower for word in ["publish", "post", "share"]):
            capabilities.append("publishing")
        
        return capabilities
    
    async def _decompose_into_tasks(
        self,
        request: AIRequest,
        capabilities: List[str]
    ) -> List[Dict[str, Any]]:
        """Decompose request into atomic tasks."""
        tasks = []
        
        # Simple decomposition based on capabilities
        for i, cap in enumerate(capabilities):
            task = {
                "id": f"task_{i}",
                "name": f"{cap}_task",
                "task_type": cap,
                "input_data": {"prompt": request.prompt, "context": request.context},
                "estimated_cost": 0.001,
                "estimated_duration_ms": 1000,
                "depends_on": []
            }
            tasks.append(task)
        
        # Add quality check task
        tasks.append({
            "id": "quality_check",
            "name": "quality_review",
            "task_type": "quality_review",
            "input_data": {},
            "estimated_cost": 0.001,
            "estimated_duration_ms": 500,
            "depends_on": [t["id"] for t in tasks]
        })
        
        return tasks
    
    async def _store_context(self, request: AIRequest):
        """Store request context in memory."""
        from app.services.ai.memory import MemoryType
        
        await self.memory_engine.store(
            memory_type=MemoryType.CONVERSATION,
            content=f"User request: {request.prompt}",
            tags=["user_request", request.request_type.value],
            importance=0.7,
            metadata={
                "user_id": request.user_id,
                "request_id": request.id
            }
        )
    
    async def _execute_chat(
        self,
        request: AIRequest,
        plan: ExecutionPlan
    ) -> Dict[str, Any]:
        """Execute a chat request."""
        # Select model
        model = await self.router.route(
            task_type="chat",
            requirements={"capabilities": ["chat"]}
        )
        
        # Build messages
        messages = [
            {"role": "user", "content": request.prompt}
        ]
        
        # Add context from memory if available
        from app.services.ai.memory import MemoryQuery, MemoryType
        memory_query = MemoryQuery(
            query=request.prompt[:100],
            memory_types=[MemoryType.CONVERSATION],
            max_results=5
        )
        relevant_memories = await self.memory_engine.retrieve(memory_query)
        
        if relevant_memories:
            context_msg = "Relevant context:\n"
            for mem in relevant_memories[:3]:
                context_msg += f"- {mem.content[:200]}\n"
            messages.insert(0, {"role": "system", "content": context_msg})
        
        # Execute via gateway
        from app.services.ai.gateway import AIRequest as GatewayRequest
        gateway_request = GatewayRequest(
            model=f"{model.provider}:{model.model_id}",
            messages=messages,
            temperature=0.7
        )
        
        response = await self.gateway.execute(gateway_request)
        
        return {
            "content": response.content,
            "model": response.model,
            "provider": response.provider,
            "tokens_used": response.tokens_total,
            "cost_usd": response.cost_usd
        }
    
    async def _execute_workflow(
        self,
        request: AIRequest,
        plan: ExecutionPlan
    ) -> Dict[str, Any]:
        """Execute a workflow request."""
        # Create workflow
        workflow_id = await self.workflow_engine.create_workflow(
            name=f"workflow_{request.id}",
            description=f"Workflow for request {request.id}",
            workflow_type=request.request_type.value,
            tasks=plan.tasks,
            variables=request.context
        )
        
        # Execute workflow
        result = await self.workflow_engine.execute_workflow(
            workflow_id=workflow_id,
            variables=request.context
        )
        
        return result
    
    async def _execute_task(
        self,
        request: AIRequest,
        plan: ExecutionPlan
    ) -> Dict[str, Any]:
        """Execute a single task request."""
        if not plan.tasks:
            return {"error": "No tasks to execute"}
        
        task = plan.tasks[0]
        
        # Select and execute via agent
        agent = await self.agent_registry.select_agent(
            task_type=task.get("task_type", "chat")
        )
        
        if agent:
            await self.agent_registry.record_execution_start(agent.id)
            
            try:
                # Execute via gateway
                model_info = task.get("assigned_model", "openai:gpt-4o-mini")
                provider, model_id = model_info.split(":")
                
                from app.services.ai.gateway import AIRequest as GatewayRequest
                gateway_request = GatewayRequest(
                    model=model_id,
                    messages=[{"role": "user", "content": request.prompt}]
                )
                
                response = await self.gateway.execute(gateway_request, provider=provider)
                
                return {
                    "content": response.content,
                    "agent": agent.name,
                    "model": model_info,
                    "tokens_used": response.tokens_total
                }
            finally:
                await self.agent_registry.record_execution_end(agent.id, success=True)
        
        return {"error": "No suitable agent found"}
    
    async def _execute_generic(
        self,
        request: AIRequest,
        plan: ExecutionPlan
    ) -> Dict[str, Any]:
        """Execute a generic request."""
        return await self._execute_chat(request, plan)
    
    async def _quality_check(
        self,
        result: Dict[str, Any],
        context: Dict[str, Any]
    ):
        """Perform quality check on result."""
        content = result.get("content", "") if isinstance(result, dict) else str(result)
        
        if not content:
            from app.services.ai.quality import QualityAssessment, QualityResult, QualityCheck
            return QualityAssessment(
                overall_score=0.0,
                passed=False,
                checks=[],
                summary="No content to check",
                recommendations=["Generate content first"]
            )
        
        return await self.quality_engine.assess(
            content=content,
            context=context
        )
    
    async def _learn_from_execution(
        self,
        request: AIRequest,
        result: Dict[str, Any],
        quality_result
    ):
        """Learn from execution for future improvement."""
        # Store performance data
        if request.id not in self.learning_data:
            self.learning_data[request.id] = {
                "request_type": request.request_type.value,
                "quality_score": quality_result.overall_score if quality_result else 0,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
    
    async def stream_chat(
        self,
        request: AIRequest
    ) -> AsyncGenerator[str, None]:
        """Stream chat response."""
        # Select model
        model = await self.router.route(task_type="chat")
        
        from app.services.ai.gateway import AIRequest as GatewayRequest
        gateway_request = GatewayRequest(
            model=f"{model.provider}:{model.model_id}",
            messages=[{"role": "user", "content": request.prompt}],
            stream=True
        )
        
        async for chunk in self.gateway.stream(gateway_request, model.provider):
            yield chunk
    
    def get_status(self) -> Dict[str, Any]:
        """Get orchestrator status."""
        return {
            "state": self.state.value,
            "active_requests": len(self.active_requests),
            "total_executions": len(self.execution_history),
            "learning_data_points": len(self.learning_data),
            "services": {
                "gateway": self.gateway is not None,
                "router": self.router is not None,
                "memory": self.memory_engine is not None,
                "prompts": self.prompt_library is not None,
                "registry": self.agent_registry is not None,
                "workflow": self.workflow_engine is not None,
                "quality": self.quality_engine is not None
            }
        }
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get orchestrator metrics."""
        if not self.execution_history:
            return {"total_executions": 0}
        
        successful = sum(1 for e in self.execution_history if e.get("success"))
        total_cost = sum(e.get("cost_usd", 0) for e in self.execution_history)
        avg_time = sum(e.get("execution_time_ms", 0) for e in self.execution_history) / len(self.execution_history)
        
        return {
            "total_executions": len(self.execution_history),
            "success_rate": successful / len(self.execution_history),
            "total_cost_usd": total_cost,
            "average_execution_time_ms": avg_time
        }


# Singleton instance
orchestrator = MasterOrchestrator()
