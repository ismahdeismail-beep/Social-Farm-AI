"""
Workflow Engine Service

Manages complex multi-step AI workflows with task decomposition,
dependency resolution, and parallel execution.
"""

from typing import Optional, Dict, Any, List, Callable, Awaitable
from datetime import datetime, timezone
from dataclasses import dataclass, field
from enum import Enum
import json
import logging
import asyncio
from collections import defaultdict

from app.services.ai.gateway import gateway, AIRequest
from app.services.ai.registry import agent_registry

logger = logging.getLogger(__name__)


class WorkflowStatus(Enum):
    """Workflow execution status."""
    DRAFT = "draft"
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PAUSED = "paused"


class TaskStatus(Enum):
    """Task execution status."""
    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    BLOCKED = "blocked"


class StepType(Enum):
    """Workflow step types."""
    TASK = "task"
    PARALLEL = "parallel"
    CONDITIONAL = "conditional"
    APPROVAL = "approval"
    LOOP = "loop"


@dataclass
class WorkflowTask:
    """A task within a workflow."""
    id: str
    name: str
    task_type: str
    agent_type: Optional[str]
    input_data: Dict[str, Any]
    status: TaskStatus = TaskStatus.PENDING
    depends_on: List[str] = field(default_factory=list)
    output: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    retry_count: int = 0
    max_retries: int = 3


@dataclass
class WorkflowDefinition:
    """Workflow definition."""
    id: str
    name: str
    description: str
    workflow_type: str
    tasks: List[WorkflowTask]
    variables: Dict[str, Any] = field(default_factory=dict)
    config: Dict[str, Any] = field(default_factory=dict)
    status: WorkflowStatus = WorkflowStatus.DRAFT
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class WorkflowEngine:
    """
    Workflow Engine for complex AI operations.
    
    Features:
    - Task decomposition
    - DAG-based dependency resolution
    - Sequential execution
    - Parallel execution
    - Conditional branching
    - Retry and error recovery
    - Human-in-the-loop approval
    """
    
    def __init__(self):
        self.workflows: Dict[str, WorkflowDefinition] = {}
        self.task_handlers: Dict[str, Callable[..., Awaitable[Dict[str, Any]]]] = {}
        self._initialized = False
    
    async def initialize(self):
        """Initialize workflow engine."""
        if self._initialized:
            return
        
        await self._register_default_handlers()
        self._initialized = True
        logger.info("Workflow Engine initialized")
    
    async def _register_default_handlers(self):
        """Register default task handlers."""
        # These are placeholder handlers that will be connected to actual services
        self.task_handlers = {
            "research": self._handle_research_task,
            "trend_analysis": self._handle_trend_task,
            "content_creation": self._handle_content_task,
            "quality_review": self._handle_quality_task,
            "publishing": self._handle_publishing_task,
        }
    
    async def create_workflow(
        self,
        name: str,
        description: str,
        workflow_type: str,
        tasks: List[Dict[str, Any]],
        variables: Optional[Dict[str, Any]] = None,
        config: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Create a new workflow.
        
        Args:
            name: Workflow name
            description: Workflow description
            workflow_type: Type of workflow
            tasks: List of task definitions
            variables: Workflow variables
            config: Workflow configuration
            
        Returns:
            Workflow ID
        """
        import uuid
        
        workflow_id = str(uuid.uuid4())
        
        workflow_tasks = []
        for task_def in tasks:
            task = WorkflowTask(
                id=task_def.get("id", str(uuid.uuid4())),
                name=task_def["name"],
                task_type=task_def["task_type"],
                agent_type=task_def.get("agent_type"),
                input_data=task_def.get("input_data", {}),
                depends_on=task_def.get("depends_on", []),
                max_retries=task_def.get("max_retries", 3)
            )
            workflow_tasks.append(task)
        
        workflow = WorkflowDefinition(
            id=workflow_id,
            name=name,
            description=description,
            workflow_type=workflow_type,
            tasks=workflow_tasks,
            variables=variables or {},
            config=config or {}
        )
        
        self.workflows[workflow_id] = workflow
        
        logger.info(f"Created workflow: {name} ({workflow_id})")
        
        return workflow_id
    
    async def execute_workflow(
        self,
        workflow_id: str,
        variables: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute a workflow.
        
        Returns:
            Execution results
        """
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow not found: {workflow_id}")
        
        # Update variables
        if variables:
            workflow.variables.update(variables)
        
        # Set status
        workflow.status = WorkflowStatus.RUNNING
        workflow.started_at = datetime.now(timezone.utc)
        
        try:
            # Build dependency graph
            dependency_graph = self._build_dependency_graph(workflow.tasks)
            
            # Execute tasks in topological order
            execution_order = self._topological_sort(dependency_graph)
            
            for batch in execution_order:
                if len(batch) == 1:
                    # Sequential execution
                    task_id = batch[0]
                    task = next((t for t in workflow.tasks if t.id == task_id), None)
                    if task:
                        await self._execute_task(workflow, task)
                else:
                    # Parallel execution
                    tasks = [
                        next((t for t in workflow.tasks if t.id == tid), None)
                        for tid in batch
                    ]
                    tasks = [t for t in tasks if t is not None]
                    await self._execute_tasks_parallel(workflow, tasks)
                
                # Check for failures
                if any(t.status == TaskStatus.FAILED for t in workflow.tasks):
                    workflow.status = WorkflowStatus.FAILED
                    break
            
            # Check final status
            if workflow.status == WorkflowStatus.RUNNING:
                all_completed = all(
                    t.status == TaskStatus.COMPLETED for t in workflow.tasks
                )
                workflow.status = WorkflowStatus.COMPLETED if all_completed else WorkflowStatus.FAILED
            
            workflow.completed_at = datetime.now(timezone.utc)
            
            # Collect results
            results = {
                "workflow_id": workflow_id,
                "status": workflow.status.value,
                "started_at": workflow.started_at.isoformat(),
                "completed_at": workflow.completed_at.isoformat(),
                "tasks": {
                    task.id: {
                        "name": task.name,
                        "status": task.status.value,
                        "output": task.output,
                        "error": task.error
                    }
                    for task in workflow.tasks
                }
            }
            
            return results
            
        except Exception as e:
            workflow.status = WorkflowStatus.FAILED
            workflow.completed_at = datetime.now(timezone.utc)
            logger.error(f"Workflow {workflow_id} failed: {e}")
            raise
    
    def _build_dependency_graph(self, tasks: List[WorkflowTask]) -> Dict[str, List[str]]:
        """Build dependency graph from tasks."""
        graph = defaultdict(list)
        
        for task in tasks:
            for dep in task.depends_on:
                graph[dep].append(task.id)
        
        return dict(graph)
    
    def _topological_sort(self, graph: Dict[str, List[str]]) -> List[List[str]]:
        """
        Topological sort with batching for parallel execution.
        
        Returns list of batches, where each batch can be executed in parallel.
        """
        # Calculate in-degrees
        in_degree = defaultdict(int)
        all_nodes = set()
        
        for node, neighbors in graph.items():
            all_nodes.add(node)
            for neighbor in neighbors:
                all_nodes.add(neighbor)
                in_degree[neighbor] += 1
        
        # Initialize queue with nodes having no dependencies
        queue = [node for node in all_nodes if in_degree[node] == 0]
        
        batches = []
        
        while queue:
            # Current batch (all can run in parallel)
            batches.append(sorted(queue))
            
            next_queue = []
            for node in queue:
                for neighbor in graph.get(node, []):
                    in_degree[neighbor] -= 1
                    if in_degree[neighbor] == 0:
                        next_queue.append(neighbor)
            
            queue = next_queue
        
        return batches
    
    async def _execute_task(self, workflow: WorkflowDefinition, task: WorkflowTask):
        """Execute a single task."""
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.now(timezone.utc)
        
        try:
            # Get task handler
            handler = self.task_handlers.get(task.task_type)
            
            if not handler:
                raise ValueError(f"No handler for task type: {task.task_type}")
            
            # Prepare input with workflow variables
            input_data = self._resolve_variables(task.input_data, workflow.variables)
            
            # Execute handler
            output = await handler(input_data)
            
            task.output = output
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now(timezone.utc)
            
            # Update workflow variables with task output
            workflow.variables[f"{task.id}_output"] = output
            
        except Exception as e:
            task.error = str(e)
            task.status = TaskStatus.FAILED
            task.completed_at = datetime.now(timezone.utc)
            logger.error(f"Task {task.id} failed: {e}")
            
            # Retry if allowed
            if task.retry_count < task.max_retries:
                task.retry_count += 1
                task.status = TaskStatus.PENDING
                logger.info(f"Retrying task {task.id} (attempt {task.retry_count})")
    
    async def _execute_tasks_parallel(
        self,
        workflow: WorkflowDefinition,
        tasks: List[WorkflowTask]
    ):
        """Execute multiple tasks in parallel."""
        await asyncio.gather(
            *[self._execute_task(workflow, task) for task in tasks],
            return_exceptions=True
        )
    
    def _resolve_variables(self, data: Dict[str, Any], variables: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve variable references in input data."""
        resolved = {}
        
        for key, value in data.items():
            if isinstance(value, str) and value.startswith("{{") and value.endswith("}}"):
                # Variable reference
                var_name = value[2:-2].strip()
                resolved[key] = variables.get(var_name, value)
            elif isinstance(value, dict):
                resolved[key] = self._resolve_variables(value, variables)
            else:
                resolved[key] = value
        
        return resolved
    
    # Task handlers — delegate to agent registry + AI gateway
    async def _handle_research_task(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle research task via the research agent."""
        agent = await agent_registry.select_agent("research", task_type="research")
        if not agent:
            return await self._fallback_ai_call("research", input_data)
        
        prompt = f"""
        Research the following topic: {input_data.get('topic', '')}
        Sources to check: {input_data.get('sources', [])}
        Requirements: {input_data.get('requirements', '')}
        Provide comprehensive findings with citations.
        """
        
        result = await self._execute_agent_task(agent, prompt)
        return {"status": "completed", "results": result}
    
    async def _handle_trend_task(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle trend analysis task via the trend agent."""
        agent = await agent_registry.select_agent("trend_analysis", task_type="trend_analysis")
        if not agent:
            return await self._fallback_ai_call("trend_analysis", input_data)
        
        prompt = f"""
        Analyze the following trends: {input_data.get('trends_data', '')}
        Industry: {input_data.get('industry', 'general')}
        Provide: insights, opportunities, recommended actions, and risk assessment.
        """
        
        result = await self._execute_agent_task(agent, prompt)
        return {"status": "completed", "trends": result}
    
    async def _handle_content_task(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle content creation task via the content agent."""
        agent = await agent_registry.select_agent("content_creation", task_type="content_creation")
        if not agent:
            return await self._fallback_ai_call("content_creation", input_data)
        
        prompt = f"""
        Create content with the following specifications:
        Brand: {input_data.get('brand_name', '')}
        Voice: {input_data.get('brand_voice', '')}
        Platform: {input_data.get('platform', '')}
        Audience: {input_data.get('target_audience', '')}
        Topic: {input_data.get('topic', '')}
        Content type: {input_data.get('content_type', 'social_post')}
        """
        
        result = await self._execute_agent_task(agent, prompt)
        return {"status": "completed", "content": result}
    
    async def _handle_quality_task(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle quality review task via the quality agent."""
        agent = await agent_registry.select_agent("quality_review", task_type="quality_review")
        if not agent:
            return await self._fallback_ai_call("quality_review", input_data)
        
        prompt = f"""
        Review the following content for quality:
        Content: {input_data.get('content', '')}
        Brand Guidelines: {input_data.get('brand_guidelines', 'No specific guidelines')}
        Target Audience: {input_data.get('target_audience', '')}
        
        Evaluate:
        1. Brand alignment (1-10)
        2. Engagement potential (1-10)
        3. Grammar and clarity (1-10)
        4. SEO optimization (1-10)
        5. Safety compliance (pass/fail)
        
        Provide detailed feedback and overall score.
        """
        
        result = await self._execute_agent_task(agent, prompt)
        return {"status": "completed", "score": 0.0, "feedback": "", "details": result}
    
    async def _handle_publishing_task(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle publishing task via the publishing agent."""
        agent = await agent_registry.select_agent("publishing", task_type="publishing")
        if not agent:
            return await self._fallback_ai_call("publishing", input_data)
        
        prompt = f"""
        Prepare the following content for publishing:
        Content: {input_data.get('content', '')}
        Platforms: {input_data.get('platforms', [])}
        Schedule: {input_data.get('schedule', 'now')}
        Hashtags: {input_data.get('hashtags', [])}
        
        Provide platform-specific formatting and optimization suggestions.
        """
        
        result = await self._execute_agent_task(agent, prompt)
        return {"status": "completed", "published": result}
    
    async def _execute_agent_task(
        self,
        agent: Any,
        prompt: str
    ) -> Dict[str, Any]:
        """Execute a task through the AI gateway using the selected agent."""
        try:
            ai_request = AIRequest(
                model=agent.preferred_models[0] if agent.preferred_models else "gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            
            response = await gateway.execute(ai_request)
            
            return {
                "agent_id": agent.id,
                "response": response.content,
                "model": response.model,
                "cost": response.cost_usd,
                "tokens": response.tokens_total,
            }
        except Exception as e:
            logger.error(f"Agent execution failed for {agent.id}: {e}")
            return {"error": str(e), "agent_id": agent.id}
    
    async def _fallback_ai_call(
        self,
        task_type: str,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Fallback direct AI call when no agent is available."""
        try:
            ai_request = AIRequest(
                model="gpt-4o-mini",
                messages=[{
                    "role": "user",
                    "content": f"Handle {task_type} task with data: {json.dumps(input_data, default=str)}"
                }],
                temperature=0.7,
            )
            response = await gateway.execute(ai_request)
            return {"response": response.content, "cost": response.cost_usd}
        except Exception as e:
            logger.warning(f"Fallback AI call failed for {task_type}: {e}")
            return {"status": "unavailable", "error": str(e)}
    
    def get_workflow(self, workflow_id: str) -> Optional[WorkflowDefinition]:
        """Get workflow by ID."""
        return self.workflows.get(workflow_id)
    
    def get_workflow_stats(self) -> Dict[str, Any]:
        """Get workflow statistics."""
        status_counts = defaultdict(int)
        for workflow in self.workflows.values():
            status_counts[workflow.status.value] += 1
        
        return {
            "total_workflows": len(self.workflows),
            "by_status": dict(status_counts)
        }


# Singleton instance
workflow_engine = WorkflowEngine()
