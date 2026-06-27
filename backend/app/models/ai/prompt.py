"""
AI Prompt Models

Defines prompt templates, versions, and usage tracking.
"""

from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Integer, Float, JSON as JSONType
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

from app.models import Base, TimestampMixin, SoftDeleteMixin


class PromptTemplate(Base, TimestampMixin, SoftDeleteMixin):
    """
    Stores prompt templates for the AI system.
    
    Templates support variable interpolation and versioning.
    """
    __tablename__ = 'ai_prompt_templates'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Definition
    name = Column(String(255), unique=True, nullable=False)
    display_name = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Category
    category = Column(String(100), nullable=False)  # system, task, workflow, quality
    tags = Column(JSONType, default=list)
    
    # Template content
    template = Column(Text, nullable=False)  # The prompt template with {{variables}}
    system_prompt = Column(Text)
    
    # Variables
    variables = Column(JSONType, default=list)  # List of variable definitions
    required_variables = Column(JSONType, default=list)
    
    # Usage context
    agent_types = Column(JSONType, default=list)  # Agent types that use this template
    task_types = Column(JSONType, default=list)  # Task types that use this template
    
    # Quality
    avg_quality_score = Column(Float, default=0.0)
    usage_count = Column(Integer, default=0)
    success_rate = Column(Float, default=1.0)
    
    # Versioning
    current_version = Column(Integer, default=1)
    
    # Ownership
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'))
    
    # Status
    is_active = Column(Boolean, default=True)
    is_system = Column(Boolean, default=False)  # System templates cannot be deleted
    
    # Relationships
    versions = relationship('PromptVersion', back_populates='template', cascade='all, delete-orphan')
    usage_history = relationship('PromptUsage', back_populates='template')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'display_name': self.display_name,
            'description': self.description,
            'category': self.category,
            'tags': self.tags,
            'template': self.template,
            'system_prompt': self.system_prompt,
            'variables': self.variables,
            'required_variables': self.required_variables,
            'agent_types': self.agent_types,
            'task_types': self.task_types,
            'avg_quality_score': self.avg_quality_score,
            'usage_count': self.usage_count,
            'success_rate': self.success_rate,
            'current_version': self.current_version,
            'created_by': self.created_by,
            'organization_id': self.organization_id,
            'is_active': self.is_active,
            'is_system': self.is_system,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at
        }


class PromptVersion(Base, TimestampMixin):
    """
    Tracks versions of prompt templates.
    
    Enables A/B testing and rollback capabilities.
    """
    __tablename__ = 'ai_prompt_versions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    template_id = Column(UUID(as_uuid=True), ForeignKey('ai_prompt_templates.id'), nullable=False)
    
    # Version
    version_number = Column(Integer, nullable=False)
    
    # Content
    template = Column(Text, nullable=False)
    system_prompt = Column(Text)
    variables = Column(JSONType, default=list)
    
    # Changes
    changelog = Column(Text)
    change_type = Column(String(50))  # major, minor, patch, experiment
    
    # Testing
    is_experiment = Column(Boolean, default=False)
    experiment_group = Column(String(100))
    
    # Quality
    quality_score = Column(Float)
    usage_count = Column(Integer, default=0)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Relationships
    template = relationship('PromptTemplate', back_populates='versions')
    
    def to_dict(self):
        return {
            'id': self.id,
            'template_id': self.template_id,
            'version_number': self.version_number,
            'template': self.template,
            'system_prompt': self.system_prompt,
            'variables': self.variables,
            'changelog': self.changelog,
            'change_type': self.change_type,
            'is_experiment': self.is_experiment,
            'experiment_group': self.experiment_group,
            'quality_score': self.quality_score,
            'usage_count': self.usage_count,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class PromptUsage(Base, TimestampMixin):
    """
    Tracks usage of prompt templates.
    
    Used for performance analysis and optimization.
    """
    __tablename__ = 'ai_prompt_usage'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    template_id = Column(UUID(as_uuid=True), ForeignKey('ai_prompt_templates.id'), nullable=False)
    version_id = Column(UUID(as_uuid=True), ForeignKey('ai_prompt_versions.id'))
    
    # Execution context
    execution_id = Column(UUID(as_uuid=True), ForeignKey('ai_executions.id'))
    agent_id = Column(UUID(as_uuid=True), ForeignKey('ai_agents.id'))
    task_id = Column(UUID(as_uuid=True), ForeignKey('ai_tasks.id'))
    
    # Input
    variables_used = Column(JSONType, default=dict)
    
    # Output
    success = Column(Boolean, nullable=False)
    quality_score = Column(Float)
    tokens_used = Column(Integer, default=0)
    latency_ms = Column(Float, default=0.0)
    cost_usd = Column(Float, default=0.0)
    
    # Relationships
    template = relationship('PromptTemplate', back_populates='usage_history')
    
    def to_dict(self):
        return {
            'id': self.id,
            'template_id': self.template_id,
            'version_id': self.version_id,
            'execution_id': self.execution_id,
            'agent_id': self.agent_id,
            'task_id': self.task_id,
            'variables_used': self.variables_used,
            'success': self.success,
            'quality_score': self.quality_score,
            'tokens_used': self.tokens_used,
            'latency_ms': self.latency_ms,
            'cost_usd': self.cost_usd,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
