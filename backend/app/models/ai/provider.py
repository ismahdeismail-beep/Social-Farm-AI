"""
AI Provider Models

Defines AI providers, model profiles, and health tracking.
"""

from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Integer, Float, JSON as JSONType, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

from app.models import Base, TimestampMixin, SoftDeleteMixin


class AIProvider(Base, TimestampMixin, SoftDeleteMixin):
    """
    Represents an AI provider (OpenAI, Anthropic, Google, etc.).
    
    Manages provider configuration, credentials, and health.
    """
    __tablename__ = 'ai_providers'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Identity
    name = Column(String(255), unique=True, nullable=False)
    display_name = Column(String(255), nullable=False)
    description = Column(Text)
    provider_type = Column(String(100), nullable=False)  # openai, anthropic, google, grok, openrouter, ollama
    
    # Configuration
    api_base_url = Column(String(500))
    api_key_env_var = Column(String(255))  # Environment variable name for API key
    config = Column(JSONType, default=dict)
    
    # Capabilities
    supported_features = Column(JSONType, default=list)  # chat, completion, embedding, image, audio, video
    supported_modalities = Column(JSONType, default=list)  # text, image, audio
    
    # Rate limits
    requests_per_minute = Column(Integer, default=60)
    tokens_per_minute = Column(Integer, default=100000)
    daily_cost_limit_usd = Column(Float, default=100.0)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_primary = Column(Boolean, default=False)  # Primary provider for fallback
    
    # Health
    health_status = Column(String(50), default='healthy')  # healthy, degraded, unhealthy, offline
    last_health_check = Column(DateTime(timezone=True))
    error_rate = Column(Float, default=0.0)
    
    # Relationships
    models = relationship('ModelProfile', back_populates='provider', cascade='all, delete-orphan')
    health_history = relationship('ProviderHealth', back_populates='provider', cascade='all, delete-orphan')
    executions = relationship('Execution', back_populates='provider')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'display_name': self.display_name,
            'description': self.description,
            'provider_type': self.provider_type,
            'api_base_url': self.api_base_url,
            'api_key_env_var': self.api_key_env_var,
            'config': self.config,
            'supported_features': self.supported_features,
            'supported_modalities': self.supported_modalities,
            'requests_per_minute': self.requests_per_minute,
            'tokens_per_minute': self.tokens_per_minute,
            'daily_cost_limit_usd': self.daily_cost_limit_usd,
            'is_active': self.is_active,
            'is_primary': self.is_primary,
            'health_status': self.health_status,
            'last_health_check': self.last_health_check,
            'error_rate': self.error_rate,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at
        }


class ModelProfile(Base, TimestampMixin, SoftDeleteMixin):
    """
    Represents a specific model from a provider.
    
    Contains model capabilities, pricing, and performance characteristics.
    """
    __tablename__ = 'ai_model_profiles'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    provider_id = Column(UUID(as_uuid=True), ForeignKey('ai_providers.id'), nullable=False)
    
    # Identity
    model_id = Column(String(255), nullable=False)  # Provider-specific model ID (e.g., gpt-4o)
    display_name = Column(String(255), nullable=False)
    description = Column(Text)
    model_type = Column(String(100), nullable=False)  # chat, completion, embedding, image, audio
    
    # Capabilities
    context_window = Column(Integer, default=4096)
    max_output_tokens = Column(Integer, default=4096)
    supports_streaming = Column(Boolean, default=True)
    supports_tools = Column(Boolean, default=False)
    supports_vision = Column(Boolean, default=False)
    supports_audio = Column(Boolean, default=False)
    
    # Pricing (per 1M tokens)
    input_cost_usd = Column(Float, default=0.0)
    output_cost_usd = Column(Float, default=0.0)
    
    # Performance
    average_latency_ms = Column(Float, default=0.0)
    average_quality_score = Column(Float, default=0.5)
    
    # Capabilities for routing
    reasoning_capability = Column(Integer, default=5)  # 1-10
    creativity_capability = Column(Integer, default=5)  # 1-10
    code_capability = Column(Integer, default=5)  # 1-10
    analysis_capability = Column(Integer, default=5)  # 1-10
    
    # Usage
    total_executions = Column(Integer, default=0)
    success_rate = Column(Float, default=1.0)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_default = Column(Boolean, default=False)  # Default model for its type
    
    # Relationships
    provider = relationship('AIProvider', back_populates='models')
    executions = relationship('Execution', back_populates='model')
    
    __table_args__ = (
        UniqueConstraint('provider_id', 'model_id', name='uq_model_profile_provider_model'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'provider_id': self.provider_id,
            'model_id': self.model_id,
            'display_name': self.display_name,
            'description': self.description,
            'model_type': self.model_type,
            'context_window': self.context_window,
            'max_output_tokens': self.max_output_tokens,
            'supports_streaming': self.supports_streaming,
            'supports_tools': self.supports_tools,
            'supports_vision': self.supports_vision,
            'supports_audio': self.supports_audio,
            'input_cost_usd': self.input_cost_usd,
            'output_cost_usd': self.output_cost_usd,
            'average_latency_ms': self.average_latency_ms,
            'average_quality_score': self.average_quality_score,
            'reasoning_capability': self.reasoning_capability,
            'creativity_capability': self.creativity_capability,
            'code_capability': self.code_capability,
            'analysis_capability': self.analysis_capability,
            'total_executions': self.total_executions,
            'success_rate': self.success_rate,
            'is_active': self.is_active,
            'is_default': self.is_default,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at
        }


class ProviderHealth(Base, TimestampMixin):
    """
    Tracks health history for AI providers.
    """
    __tablename__ = 'ai_provider_health'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    provider_id = Column(UUID(as_uuid=True), ForeignKey('ai_providers.id'), nullable=False)
    
    # Health metrics
    status = Column(String(50), nullable=False)  # healthy, degraded, unhealthy, offline
    response_time_ms = Column(Float)
    error_rate = Column(Float, default=0.0)
    success_rate = Column(Float, default=1.0)
    
    # Availability
    uptime_percentage = Column(Float, default=100.0)
    
    # Details
    check_type = Column(String(50))  # ping, test_request, live
    error_message = Column(Text)
    details = Column(JSONType, default=dict)
    
    # Relationships
    provider = relationship('AIProvider', back_populates='health_history')
    
    def to_dict(self):
        return {
            'id': self.id,
            'provider_id': self.provider_id,
            'status': self.status,
            'response_time_ms': self.response_time_ms,
            'error_rate': self.error_rate,
            'success_rate': self.success_rate,
            'uptime_percentage': self.uptime_percentage,
            'check_type': self.check_type,
            'error_message': self.error_message,
            'details': self.details,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
