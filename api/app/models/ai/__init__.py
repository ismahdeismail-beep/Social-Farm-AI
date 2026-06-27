"""
AI Orchestrator Database Models

This module contains all database models for the Master AI Orchestrator system.
Implements agents, tasks, workflows, executions, memory, prompts, providers, and metrics.
"""

from app.models.ai.agent import Agent, AgentCapability, AgentHealth
from app.models.ai.task import AgentTask, TaskDependency, TaskResult
from app.models.ai.workflow import Workflow, WorkflowStep, WorkflowExecution
from app.models.ai.execution import Execution, ExecutionHistory, ExecutionResult, ExecutionQueue
from app.models.ai.memory import MemoryReference, MemoryEntry, MemoryType
from app.models.ai.prompt import PromptTemplate, PromptVersion, PromptUsage
from app.models.ai.provider import AIProvider, ModelProfile, ProviderHealth
from app.models.ai.metrics import (
    PerformanceMetric,
    CostRecord,
    ReasoningTrace,
    DecisionLog,
    AgentFeedback,
    SystemHealth,
    AuditEvent
)

__all__ = [
    # Agent models
    "Agent",
    "AgentCapability",
    "AgentHealth",
    
    # Task models
    "AgentTask",
    "TaskDependency",
    "TaskResult",
    
    # Workflow models
    "Workflow",
    "WorkflowStep",
    "WorkflowExecution",
    
    # Execution models
    "Execution",
    "ExecutionHistory",
    "ExecutionResult",
    "ExecutionQueue",
    
    # Memory models
    "MemoryReference",
    "MemoryEntry",
    "MemoryType",
    
    # Prompt models
    "PromptTemplate",
    "PromptVersion",
    "PromptUsage",
    
    # Provider models
    "AIProvider",
    "ModelProfile",
    "ProviderHealth",
    
    # Metrics models
    "PerformanceMetric",
    "CostRecord",
    "ReasoningTrace",
    "DecisionLog",
    "AgentFeedback",
    "SystemHealth",
    "AuditEvent",
]
