"""
AI Execution Models

Defines execution tracking, history, results, and queue for the AI Orchestrator.
"""

from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Integer, Float, JSON as JSONType
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

from app.models import Base, TimestampMixin, SoftDeleteMixin


class Execution(Base, TimestampMixin, SoftDeleteMixin):
    """
    Represents a single execution of an AI task.
    
    Tracks the complete lifecycle of an AI operation.
    """
    __tablename__ = 'ai_executions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Reference
    task_id = Column(UUID(as_uuid=True), ForeignKey('ai_tasks.id'))
    agent_id = Column(UUID(as_uuid=True), ForeignKey('ai_agents.id'))
    workflow_execution_id = Column(UUID(as_uuid=True), ForeignKey('ai_workflow_executions.id'))
    
    # Execution details
    execution_type = Column(String(50), nullable=False)  # single, pipeline, parallel
    status = Column(String(50), default='pending')  # pending, queued, running, completed, failed, cancelled, timeout
    
    # Provider
    provider_id = Column(UUID(as_uuid=True), ForeignKey('ai_providers.id'))
    model_id = Column(UUID(as_uuid=True), ForeignKey('ai_model_profiles.id'))
    model_name = Column(String(255))
    
    # Request
    prompt = Column(Text)
    system_prompt = Column(Text)
    messages = Column(JSONType, default=list)  # For chat-style interactions
    tools = Column(JSONType, default=list)
    tool_choice = Column(String(50))
    
    # Response
    response = Column(JSONType)
    response_text = Column(Text)
    tool_calls = Column(JSONType, default=list)
    
    # Tokens
    tokens_input = Column(Integer, default=0)
    tokens_output = Column(Integer, default=0)
    tokens_total = Column(Integer, default=0)
    
    # Cost
    cost_usd = Column(Float, default=0.0)
    
    # Timing
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    latency_ms = Column(Float)
    time_to_first_token_ms = Column(Float)
    
    # Quality
    quality_score = Column(Float)
    quality_details = Column(JSONType, default=dict)
    
    # Context
    context = Column(JSONType, default=dict)
    metadata = Column(JSONType, default=dict)
    
    # Error
    error = Column(Text)
    error_type = Column(String(100))
    error_details = Column(JSONType)
    
    # Retry
    retry_of = Column(UUID(as_uuid=True), ForeignKey('ai_executions.id'))
    retry_count = Column(Integer, default=0)
    
    # Relationships
    task = relationship('AgentTask', back_populates='executions')
    agent = relationship('Agent', back_populates='executions')
    provider = relationship('AIProvider')
    model = relationship('ModelProfile')
    history = relationship('ExecutionHistory', back_populates='execution', cascade='all, delete-orphan')
    result = relationship('ExecutionResult', back_populates='execution', uselist=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'task_id': self.task_id,
            'agent_id': self.agent_id,
            'workflow_execution_id': self.workflow_execution_id,
            'execution_type': self.execution_type,
            'status': self.status,
            'provider_id': self.provider_id,
            'model_id': self.model_id,
            'model_name': self.model_name,
            'prompt': self.prompt,
            'system_prompt': self.system_prompt,
            'messages': self.messages,
            'tools': self.tools,
            'tool_choice': self.tool_choice,
            'response': self.response,
            'response_text': self.response_text,
            'tool_calls': self.tool_calls,
            'tokens_input': self.tokens_input,
            'tokens_output': self.tokens_output,
            'tokens_total': self.tokens_total,
            'cost_usd': self.cost_usd,
            'started_at': self.started_at,
            'completed_at': self.completed_at,
            'latency_ms': self.latency_ms,
            'time_to_first_token_ms': self.time_to_first_token_ms,
            'quality_score': self.quality_score,
            'quality_details': self.quality_details,
            'context': self.context,
            'metadata': self.metadata,
            'error': self.error,
            'error_type': self.error_type,
            'error_details': self.error_details,
            'retry_of': self.retry_of,
            'retry_count': self.retry_count,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at
        }


class ExecutionHistory(Base, TimestampMixin):
    """
    Tracks state changes during execution.
    """
    __tablename__ = 'ai_execution_history'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    execution_id = Column(UUID(as_uuid=True), ForeignKey('ai_executions.id'), nullable=False)
    
    # State change
    event_type = Column(String(50), nullable=False)  # started, progress, completed, failed, retry, timeout
    previous_status = Column(String(50))
    new_status = Column(String(50))
    
    # Details
    message = Column(Text)
    details = Column(JSONType, default=dict)
    
    # Timing
    event_time = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    # Relationships
    execution = relationship('Execution', back_populates='history')
    
    def to_dict(self):
        return {
            'id': self.id,
            'execution_id': self.execution_id,
            'event_type': self.event_type,
            'previous_status': self.previous_status,
            'new_status': self.new_status,
            'message': self.message,
            'details': self.details,
            'event_time': self.event_time,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class ExecutionResult(Base, TimestampMixin):
    """
    Stores the final result of an execution.
    """
    __tablename__ = 'ai_execution_results'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    execution_id = Column(UUID(as_uuid=True), ForeignKey('ai_executions.id'), unique=True, nullable=False)
    
    # Result
    success = Column(Boolean, nullable=False)
    output = Column(JSONType, default=dict)
    output_text = Column(Text)
    artifacts = Column(JSONType, default=list)  # URLs to generated files
    
    # Quality
    quality_score = Column(Float)
    quality_checks = Column(JSONType, default=list)
    
    # Usage
    tokens_used = Column(Integer, default=0)
    cost_usd = Column(Float, default=0.0)
    
    # Relationships
    execution = relationship('Execution', back_populates='result')
    
    def to_dict(self):
        return {
            'id': self.id,
            'execution_id': self.execution_id,
            'success': self.success,
            'output': self.output,
            'output_text': self.output_text,
            'artifacts': self.artifacts,
            'quality_score': self.quality_score,
            'quality_checks': self.quality_checks,
            'tokens_used': self.tokens_used,
            'cost_usd': self.cost_usd,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class ExecutionQueue(Base, TimestampMixin):
    """
    Queue for pending executions.
    
    Managed by the execution engine for priority-based processing.
    """
    __tablename__ = 'ai_execution_queue'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Reference
    execution_id = Column(UUID(as_uuid=True), ForeignKey('ai_executions.id'), nullable=False)
    
    # Queue management
    priority = Column(Integer, default=0)  # Higher = processed first
    status = Column(String(50), default='pending')  # pending, processing, completed, failed
    queue_name = Column(String(100), default='default')  # For separate queues
    
    # Timing
    queued_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    started_processing_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    
    # Worker
    worker_id = Column(String(100))  # ID of the worker processing this item
    
    # Retry
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    
    def to_dict(self):
        return {
            'id': self.id,
            'execution_id': self.execution_id,
            'priority': self.priority,
            'status': self.status,
            'queue_name': self.queue_name,
            'queued_at': self.queued_at,
            'started_processing_at': self.started_processing_at,
            'completed_at': self.completed_at,
            'worker_id': self.worker_id,
            'retry_count': self.retry_count,
            'max_retries': self.max_retries,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
