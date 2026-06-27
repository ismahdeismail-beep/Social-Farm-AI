"""
AI Memory Models

Defines memory references and entries for the AI Orchestrator.
"""

from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Integer, Float, JSON as JSONType, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
import enum

from app.models import Base, TimestampMixin, SoftDeleteMixin


class MemoryType(enum.Enum):
    """Types of memory in the AI system."""
    CONVERSATION = "conversation"
    BRAND = "brand"
    PROJECT = "project"
    CAMPAIGN = "campaign"
    USER = "user"
    PERFORMANCE = "performance"
    KNOWLEDGE = "knowledge"
    TOOL = "tool"


class MemoryReference(Base, TimestampMixin, SoftDeleteMixin):
    """
    References a memory entry for quick lookup.
    
    Used by the Memory Router to find relevant memories.
    """
    __tablename__ = 'ai_memory_references'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Reference
    memory_type = Column(String(50), nullable=False)
    reference_id = Column(UUID(as_uuid=True), nullable=False)  # ID of the referenced entity
    
    # Lookup
    name = Column(String(255), nullable=False)
    description = Column(Text)
    tags = Column(JSONType, default=list)
    
    # Context
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'))
    workspace_id = Column(UUID(as_uuid=True), ForeignKey('workspaces.id'))
    brand_id = Column(UUID(as_uuid=True))
    project_id = Column(UUID(as_uuid=True))
    
    # Access control
    access_level = Column(String(50), default='private')  # private, workspace, organization, public
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    
    # Usage
    access_count = Column(Integer, default=0)
    last_accessed_at = Column(DateTime(timezone=True))
    
    # Status
    is_active = Column(Boolean, default=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'memory_type': self.memory_type,
            'reference_id': self.reference_id,
            'name': self.name,
            'description': self.description,
            'tags': self.tags,
            'organization_id': self.organization_id,
            'workspace_id': self.workspace_id,
            'brand_id': self.brand_id,
            'project_id': self.project_id,
            'access_level': self.access_level,
            'created_by': self.created_by,
            'access_count': self.access_count,
            'last_accessed_at': self.last_accessed_at,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at
        }


class MemoryEntry(Base, TimestampMixin, SoftDeleteMixin):
    """
    Stores actual memory content.
    
    Supports different types of memory with varying retention and importance.
    """
    __tablename__ = 'ai_memory_entries'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reference_id = Column(UUID(as_uuid=True), ForeignKey('ai_memory_references.id'), nullable=False)
    
    # Content
    content = Column(Text, nullable=False)
    content_type = Column(String(50), default='text')  # text, json, markdown
    summary = Column(Text)  # Compressed version for long content
    
    # Importance and relevance
    importance_score = Column(Float, default=0.5)  # 0.0 to 1.0
    relevance_score = Column(Float, default=0.5)  # 0.0 to 1.0
    decay_rate = Column(Float, default=0.1)  # How fast importance decays
    
    # Embeddings (for vector search)
    embedding = Column(JSONType)  # Vector embedding for semantic search
    embedding_model = Column(String(100))
    
    # Source
    source_type = Column(String(50))  # user, ai, system, import
    source_id = Column(String(255))  # ID of the source (message ID, etc.)
    
    # Retention
    retention_policy = Column(String(50), default='default')  # default, permanent, temporary
    expires_at = Column(DateTime(timezone=True))
    compressed = Column(Boolean, default=False)
    
    # Relationships
    reference = relationship('MemoryReference', back_populates='entries')
    
    def to_dict(self):
        return {
            'id': self.id,
            'reference_id': self.reference_id,
            'content': self.content,
            'content_type': self.content_type,
            'summary': self.summary,
            'importance_score': self.importance_score,
            'relevance_score': self.relevance_score,
            'decay_rate': self.decay_rate,
            'embedding': self.embedding,
            'embedding_model': self.embedding_model,
            'source_type': self.source_type,
            'source_id': self.source_id,
            'retention_policy': self.retention_policy,
            'expires_at': self.expires_at,
            'compressed': self.compressed,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at
        }


# Add relationship to MemoryReference
MemoryReference.entries = relationship('MemoryEntry', back_populates='reference', cascade='all, delete-orphan')
