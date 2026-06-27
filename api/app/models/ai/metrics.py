"""
AI Metrics Models

Defines performance metrics, cost records, reasoning traces, decision logs,
feedback, system health, and audit events.
"""

from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Integer, Float, JSON as JSONType
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

from app.models import Base, TimestampMixin, SoftDeleteMixin


class PerformanceMetric(Base, TimestampMixin):
    """
    Tracks performance metrics for AI operations.
    """
    __tablename__ = 'ai_performance_metrics'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Dimension
    metric_name = Column(String(255), nullable=False)
    metric_type = Column(String(100), nullable=False)  # latency, throughput, quality, cost
    dimension = Column(String(100))  # agent, model, provider, task_type
    
    # Value
    value = Column(Float, nullable=False)
    unit = Column(String(50))  # ms, tokens, usd, score
    count = Column(Integer, default=1)
    
    # Context
    agent_id = Column(UUID(as_uuid=True), ForeignKey('ai_agents.id'))
    model_id = Column(UUID(as_uuid=True), ForeignKey('ai_model_profiles.id'))
    provider_id = Column(UUID(as_uuid=True), ForeignKey('ai_providers.id'))
    task_type = Column(String(100))
    
    # Time window
    recorded_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    period_start = Column(DateTime(timezone=True))
    period_end = Column(DateTime(timezone=True))
    
    # Aggregation
    min_value = Column(Float)
    max_value = Column(Float)
    avg_value = Column(Float)
    p50_value = Column(Float)
    p95_value = Column(Float)
    p99_value = Column(Float)
    
    def to_dict(self):
        return {
            'id': self.id,
            'metric_name': self.metric_name,
            'metric_type': self.metric_type,
            'dimension': self.dimension,
            'value': self.value,
            'unit': self.unit,
            'count': self.count,
            'agent_id': self.agent_id,
            'model_id': self.model_id,
            'provider_id': self.provider_id,
            'task_type': self.task_type,
            'recorded_at': self.recorded_at,
            'period_start': self.period_start,
            'period_end': self.period_end,
            'min_value': self.min_value,
            'max_value': self.max_value,
            'avg_value': self.avg_value,
            'p50_value': self.p50_value,
            'p95_value': self.p95_value,
            'p99_value': self.p99_value,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class CostRecord(Base, TimestampMixin):
    """
    Tracks cost records for AI operations.
    """
    __tablename__ = 'ai_cost_records'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Reference
    execution_id = Column(UUID(as_uuid=True), ForeignKey('ai_executions.id'))
    task_id = Column(UUID(as_uuid=True), ForeignKey('ai_tasks.id'))
    workflow_id = Column(UUID(as_uuid=True), ForeignKey('ai_workflows.id'))
    
    # Provider
    provider_id = Column(UUID(as_uuid=True), ForeignKey('ai_providers.id'))
    model_id = Column(UUID(as_uuid=True), ForeignKey('ai_model_profiles.id'))
    
    # Cost breakdown
    input_cost_usd = Column(Float, default=0.0)
    output_cost_usd = Column(Float, default=0.0)
    total_cost_usd = Column(Float, default=0.0)
    
    # Tokens
    input_tokens = Column(Integer, default=0)
    output_tokens = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)
    
    # Context
    task_type = Column(String(100))
    agent_type = Column(String(100))
    
    # Ownership
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'))
    workspace_id = Column(UUID(as_uuid=True), ForeignKey('workspaces.id'))
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    
    def to_dict(self):
        return {
            'id': self.id,
            'execution_id': self.execution_id,
            'task_id': self.task_id,
            'workflow_id': self.workflow_id,
            'provider_id': self.provider_id,
            'model_id': self.model_id,
            'input_cost_usd': self.input_cost_usd,
            'output_cost_usd': self.output_cost_usd,
            'total_cost_usd': self.total_cost_usd,
            'input_tokens': self.input_tokens,
            'output_tokens': self.output_tokens,
            'total_tokens': self.total_tokens,
            'task_type': self.task_type,
            'agent_type': self.agent_type,
            'organization_id': self.organization_id,
            'workspace_id': self.workspace_id,
            'user_id': self.user_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class ReasoningTrace(Base, TimestampMixin):
    """
    Records the reasoning process of AI decisions.
    
    Used for debugging, optimization, and self-reflection.
    """
    __tablename__ = 'ai_reasoning_traces'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Reference
    execution_id = Column(UUID(as_uuid=True), ForeignKey('ai_executions.id'))
    task_id = Column(UUID(as_uuid=True), ForeignKey('ai_tasks.id'))
    
    # Reasoning
    goal = Column(Text, nullable=False)
    context_summary = Column(Text)
    reasoning_steps = Column(JSONType, default=list)  # List of reasoning steps
    alternatives_considered = Column(JSONType, default=list)
    decision = Column(Text)
    decision_rationale = Column(Text)
    
    # Confidence
    confidence_score = Column(Float, default=0.5)
    certainty_level = Column(String(50))  # certain, confident, uncertain, guessing
    
    # Learning
    was_correct = Column(Boolean)
    actual_outcome = Column(Text)
    lesson_learned = Column(Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'execution_id': self.execution_id,
            'task_id': self.task_id,
            'goal': self.goal,
            'context_summary': self.context_summary,
            'reasoning_steps': self.reasoning_steps,
            'alternatives_considered': self.alternatives_considered,
            'decision': self.decision,
            'decision_rationale': self.decision_rationale,
            'confidence_score': self.confidence_score,
            'certainty_level': self.certainty_level,
            'was_correct': self.was_correct,
            'actual_outcome': self.actual_outcome,
            'lesson_learned': self.lesson_learned,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class DecisionLog(Base, TimestampMixin):
    """
    Logs key decisions made by the AI orchestrator.
    """
    __tablename__ = 'ai_decision_logs'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Decision
    decision_type = Column(String(100), nullable=False)  # agent_selection, model_routing, workflow, retry, fallback
    decision = Column(Text, nullable=False)
    alternatives = Column(JSONType, default=list)
    
    # Context
    context = Column(JSONType, default=dict)
    input_data = Column(JSONType, default=dict)
    
    # Reasoning
    reasoning = Column(Text)
    factors = Column(JSONType, default=list)  # Factors that influenced the decision
    weight = Column(JSONType, default=dict)  # Weight of each factor
    
    # Outcome
    outcome = Column(String(50))  # success, failure, partial
    outcome_details = Column(Text)
    
    # Metrics
    confidence = Column(Float, default=0.5)
    execution_time_ms = Column(Float)
    
    # Relationships
    execution = relationship('Execution')
    
    def to_dict(self):
        return {
            'id': self.id,
            'decision_type': self.decision_type,
            'decision': self.decision,
            'alternatives': self.alternatives,
            'context': self.context,
            'input_data': self.input_data,
            'reasoning': self.reasoning,
            'factors': self.factors,
            'weight': self.weight,
            'outcome': self.outcome,
            'outcome_details': self.outcome_details,
            'confidence': self.confidence,
            'execution_time_ms': self.execution_time_ms,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class AgentFeedback(Base, TimestampMixin):
    """
    Stores feedback on AI agent performance.
    """
    __tablename__ = 'ai_agent_feedback'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Reference
    agent_id = Column(UUID(as_uuid=True), ForeignKey('ai_agents.id'), nullable=False)
    execution_id = Column(UUID(as_uuid=True), ForeignKey('ai_executions.id'))
    task_id = Column(UUID(as_uuid=True), ForeignKey('ai_tasks.id'))
    
    # Feedback
    feedback_type = Column(String(50), nullable=False)  # rating, comment, correction, suggestion
    rating = Column(Integer)  # 1-5
    comment = Column(Text)
    correction = Column(JSONType)
    
    # Source
    source = Column(String(50), nullable=False)  # user, system, automated
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    
    # Impact
    applied = Column(Boolean, default=False)
    applied_at = Column(DateTime(timezone=True))
    impact_score = Column(Float)
    
    def to_dict(self):
        return {
            'id': self.id,
            'agent_id': self.agent_id,
            'execution_id': self.execution_id,
            'task_id': self.task_id,
            'feedback_type': self.feedback_type,
            'rating': self.rating,
            'comment': self.comment,
            'correction': self.correction,
            'source': self.source,
            'user_id': self.user_id,
            'applied': self.applied,
            'applied_at': self.applied_at,
            'impact_score': self.impact_score,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class SystemHealth(Base, TimestampMixin):
    """
    Tracks overall system health metrics.
    """
    __tablename__ = 'ai_system_health'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Component
    component = Column(String(100), nullable=False)  # gateway, router, orchestrator, queue, memory
    status = Column(String(50), nullable=False)  # healthy, degraded, unhealthy, offline
    
    # Metrics
    cpu_usage = Column(Float)
    memory_usage = Column(Float)
    disk_usage = Column(Float)
    network_latency_ms = Column(Float)
    
    # Performance
    requests_per_second = Column(Float)
    average_response_time_ms = Column(Float)
    error_rate = Column(Float, default=0.0)
    throughput = Column(Float)
    
    # Details
    details = Column(JSONType, default=dict)
    error_message = Column(Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'component': self.component,
            'status': self.status,
            'cpu_usage': self.cpu_usage,
            'memory_usage': self.memory_usage,
            'disk_usage': self.disk_usage,
            'network_latency_ms': self.network_latency_ms,
            'requests_per_second': self.requests_per_second,
            'average_response_time_ms': self.average_response_time_ms,
            'error_rate': self.error_rate,
            'throughput': self.throughput,
            'details': self.details,
            'error_message': self.error_message,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class AuditEvent(Base, TimestampMixin, SoftDeleteMixin):
    """
    Audit events for AI operations.
    """
    __tablename__ = 'ai_audit_events'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Event
    event_type = Column(String(100), nullable=False)  # execution, error, security, configuration
    event_action = Column(String(100), nullable=False)  # create, read, update, delete, execute, fail
    
    # Resource
    resource_type = Column(String(100))  # agent, workflow, task, provider, model
    resource_id = Column(UUID(as_uuid=True))
    
    # Actor
    actor_type = Column(String(50))  # user, system, agent
    actor_id = Column(UUID(as_uuid=True))
    
    # Details
    details = Column(JSONType, default=dict)
    old_value = Column(JSONType)
    new_value = Column(JSONType)
    
    # Context
    ip_address = Column(String(45))
    user_agent = Column(Text)
    request_id = Column(String(255))
    
    # Outcome
    success = Column(Boolean, default=True)
    error_message = Column(Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'event_type': self.event_type,
            'event_action': self.event_action,
            'resource_type': self.resource_type,
            'resource_id': self.resource_id,
            'actor_type': self.actor_type,
            'actor_id': self.actor_id,
            'details': self.details,
            'old_value': self.old_value,
            'new_value': self.new_value,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'request_id': self.request_id,
            'success': self.success,
            'error_message': self.error_message,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at
        }
