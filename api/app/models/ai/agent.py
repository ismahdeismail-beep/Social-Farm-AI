"""
AI Agent Models

Defines the Agent entity and its capabilities for the AI Orchestrator.
"""

from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Integer, Float, JSON as JSONType
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

from app.models import Base, TimestampMixin, SoftDeleteMixin


class Agent(Base, TimestampMixin, SoftDeleteMixin):
    """
    Represents an AI Agent in the system.
    
    Each agent has specific capabilities, preferred models, and health status.
    The orchestrator uses this registry to select the best agent for each task.
    """
    __tablename__ = 'ai_agents'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), unique=True, nullable=False)
    display_name = Column(String(255), nullable=False)
    description = Column(Text)
    agent_type = Column(String(100), nullable=False)  # trend, research, script, media, publishing, analytics
    
    # Capabilities
    supported_tasks = Column(JSONType, default=list)  # List of task types this agent can handle
    preferred_models = Column(JSONType, default=list)  # Preferred model IDs in order
    max_context_tokens = Column(Integer, default=128000)
    
    # Cost profile
    cost_per_1k_tokens = Column(Float, default=0.0)
    average_latency_ms = Column(Float, default=0.0)
    
    # Priority and fallback
    priority = Column(Integer, default=0)  # Higher = preferred
    fallback_agent_id = Column(UUID(as_uuid=True), ForeignKey('ai_agents.id'))
    
    # Dependencies
    required_dependencies = Column(JSONType, default=list)  # Agent IDs required before this can run
    
    # Status
    is_active = Column(Boolean, default=True)
    is_system = Column(Boolean, default=False)  # System agents cannot be deleted
    
    # Configuration
    config = Column(JSONType, default=dict)  # Agent-specific configuration
    max_concurrent_executions = Column(Integer, default=1)
    timeout_seconds = Column(Integer, default=300)
    
    # Relationships
    fallback_agent = relationship('Agent', remote_side=[id], backref='fallback_for')
    capabilities = relationship('AgentCapability', back_populates='agent', cascade='all, delete-orphan')
    health = relationship('AgentHealth', back_populates='agent', uselist=False)
    tasks = relationship('AgentTask', back_populates='agent')
    executions = relationship('Execution', back_populates='agent')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'display_name': self.display_name,
            'description': self.description,
            'agent_type': self.agent_type,
            'supported_tasks': self.supported_tasks,
            'preferred_models': self.preferred_models,
            'max_context_tokens': self.max_context_tokens,
            'cost_per_1k_tokens': self.cost_per_1k_tokens,
            'average_latency_ms': self.average_latency_ms,
            'priority': self.priority,
            'fallback_agent_id': self.fallback_agent_id,
            'is_active': self.is_active,
            'is_system': self.is_system,
            'config': self.config,
            'max_concurrent_executions': self.max_concurrent_executions,
            'timeout_seconds': self.timeout_seconds,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at
        }


class AgentCapability(Base, TimestampMixin):
    """
    Defines specific capabilities of an agent.
    
    Used for capability-based agent selection.
    """
    __tablename__ = 'ai_agent_capabilities'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey('ai_agents.id'), nullable=False)
    capability_name = Column(String(255), nullable=False)
    capability_type = Column(String(100), nullable=False)  # text_generation, image_generation, video_generation, etc.
    description = Column(Text)
    proficiency_level = Column(Integer, default=5)  # 1-10, higher = better
    supported_input_types = Column(JSONType, default=list)
    supported_output_types = Column(JSONType, default=list)
    
    # Relationships
    agent = relationship('Agent', back_populates='capabilities')
    
    def to_dict(self):
        return {
            'id': self.id,
            'agent_id': self.agent_id,
            'capability_name': self.capability_name,
            'capability_type': self.capability_type,
            'description': self.description,
            'proficiency_level': self.proficiency_level,
            'supported_input_types': self.supported_input_types,
            'supported_output_types': self.supported_output_types,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class AgentHealth(Base, TimestampMixin):
    """
    Tracks real-time health status of an agent.
    
    Updated by the health monitor.
    """
    __tablename__ = 'ai_agent_health'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey('ai_agents.id'), unique=True, nullable=False)
    
    # Health metrics
    status = Column(String(50), default='healthy')  # healthy, degraded, unhealthy, offline
    success_rate = Column(Float, default=1.0)  # 0.0 to 1.0
    average_response_time_ms = Column(Float, default=0.0)
    error_count_24h = Column(Integer, default=0)
    total_executions_24h = Column(Integer, default=0)
    
    # Current state
    current_load = Column(Float, default=0.0)  # 0.0 to 1.0
    active_executions = Column(Integer, default=0)
    queue_depth = Column(Integer, default=0)
    
    # Last check
    last_health_check = Column(DateTime(timezone=True))
    last_error = Column(Text)
    last_error_time = Column(DateTime(timezone=True))
    
    # Relationships
    agent = relationship('Agent', back_populates='health')
    
    def to_dict(self):
        return {
            'id': self.id,
            'agent_id': self.agent_id,
            'status': self.status,
            'success_rate': self.success_rate,
            'average_response_time_ms': self.average_response_time_ms,
            'error_count_24h': self.error_count_24h,
            'total_executions_24h': self.total_executions_24h,
            'current_load': self.current_load,
            'active_executions': self.active_executions,
            'queue_depth': self.queue_depth,
            'last_health_check': self.last_health_check,
            'last_error': self.last_error,
            'last_error_time': self.last_error_time,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
