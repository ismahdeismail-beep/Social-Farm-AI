"""
AI Task Models

Defines tasks, dependencies, and results for the AI Orchestrator.
"""

from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Integer, Float, JSON as JSONType
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

from app.models import Base, TimestampMixin, SoftDeleteMixin


class AgentTask(Base, TimestampMixin, SoftDeleteMixin):
    """
    Represents an atomic task to be executed by an AI agent.
    
    Tasks are created by the Task Decomposer and executed by agents.
    """
    __tablename__ = 'ai_tasks'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_id = Column(UUID(as_uuid=True), ForeignKey('ai_workflows.id'))
    
    # Task definition
    name = Column(String(255), nullable=False)
    task_type = Column(String(100), nullable=False)  # research, generation, analysis, etc.
    description = Column(Text)
    
    # Input/Output
    input_data = Column(JSONType, default=dict)
    expected_output_schema = Column(JSONType)
    
    # Assignment
    assigned_agent_id = Column(UUID(as_uuid=True), ForeignKey('ai_agents.id'))
    assigned_model_id = Column(UUID(as_uuid=True), ForeignKey('ai_model_profiles.id'))
    
    # Execution
    status = Column(String(50), default='pending')  # pending, queued, running, completed, failed, cancelled
    priority = Column(Integer, default=0)
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    timeout_seconds = Column(Integer, default=300)
    
    # Timing
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    duration_ms = Column(Float)
    
    # Quality
    quality_score = Column(Float)
    confidence_score = Column(Float)
    
    # Cost
    tokens_used = Column(Integer, default=0)
    cost_usd = Column(Float, default=0.0)
    
    # Context
    context = Column(JSONType, default=dict)  # Additional context for the agent
    extra_data = Column("metadata", JSONType, default=dict)
    
    # Relationships
    workflow = relationship('Workflow', back_populates='tasks')
    agent = relationship('Agent', back_populates='tasks')
    dependencies = relationship('TaskDependency', foreign_keys='TaskDependency.task_id', back_populates='task')
    dependents = relationship('TaskDependency', foreign_keys='TaskDependency.depends_on_id', back_populates='depends_on')
    result = relationship('TaskResult', back_populates='task', uselist=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'workflow_id': self.workflow_id,
            'name': self.name,
            'task_type': self.task_type,
            'description': self.description,
            'input_data': self.input_data,
            'assigned_agent_id': self.assigned_agent_id,
            'assigned_model_id': self.assigned_model_id,
            'status': self.status,
            'priority': self.priority,
            'retry_count': self.retry_count,
            'max_retries': self.max_retries,
            'timeout_seconds': self.timeout_seconds,
            'started_at': self.started_at,
            'completed_at': self.completed_at,
            'duration_ms': self.duration_ms,
            'quality_score': self.quality_score,
            'confidence_score': self.confidence_score,
            'tokens_used': self.tokens_used,
            'cost_usd': self.cost_usd,
            'context': self.context,
            'metadata': self.extra_data,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at
        }


class TaskDependency(Base, TimestampMixin):
    """
    Defines dependencies between tasks.
    
    Used by the Dependency Resolver to determine execution order.
    """
    __tablename__ = 'ai_task_dependencies'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey('ai_tasks.id'), nullable=False)
    depends_on_id = Column(UUID(as_uuid=True), ForeignKey('ai_tasks.id'), nullable=False)
    dependency_type = Column(String(50), default='required')  # required, optional, conditional
    
    # Relationships
    task = relationship('AgentTask', foreign_keys=[task_id], back_populates='dependencies')
    depends_on = relationship('AgentTask', foreign_keys=[depends_on_id], back_populates='dependents')
    
    def to_dict(self):
        return {
            'id': self.id,
            'task_id': self.task_id,
            'depends_on_id': self.depends_on_id,
            'dependency_type': self.dependency_type,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class TaskResult(Base, TimestampMixin):
    """
    Stores the result of a completed task.
    """
    __tablename__ = 'ai_task_results'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey('ai_tasks.id'), unique=True, nullable=False)
    
    # Result
    output_data = Column(JSONType, default=dict)
    output_text = Column(Text)
    output_artifacts = Column(JSONType, default=list)  # URLs to generated files
    
    # Quality
    quality_score = Column(Float)
    quality_details = Column(JSONType, default=dict)
    
    # Metadata
    model_used = Column(String(255))
    tokens_input = Column(Integer, default=0)
    tokens_output = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)
    cost_usd = Column(Float, default=0.0)
    latency_ms = Column(Float, default=0.0)
    
    # Review
    reviewed_by_human = Column(Boolean, default=False)
    human_feedback = Column(Text)
    human_rating = Column(Integer)  # 1-5
    
    # Relationships
    task = relationship('AgentTask', back_populates='result')
    
    def to_dict(self):
        return {
            'id': self.id,
            'task_id': self.task_id,
            'output_data': self.output_data,
            'output_text': self.output_text,
            'output_artifacts': self.output_artifacts,
            'quality_score': self.quality_score,
            'quality_details': self.quality_details,
            'model_used': self.model_used,
            'tokens_input': self.tokens_input,
            'tokens_output': self.tokens_output,
            'total_tokens': self.total_tokens,
            'cost_usd': self.cost_usd,
            'latency_ms': self.latency_ms,
            'reviewed_by_human': self.reviewed_by_human,
            'human_feedback': self.human_feedback,
            'human_rating': self.human_rating,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
