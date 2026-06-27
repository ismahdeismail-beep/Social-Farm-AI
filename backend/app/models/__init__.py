"""
Core domain models for Social Farm AI.

Re-exports Base, mixins, and all model classes for convenience.
"""

from app.models.base import Base, TimestampMixin, SoftDeleteMixin
from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, UUID as SQLUUID, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from typing import Optional
import uuid

# Re-export database session dependency for convenience
from app.db import get_db

# Import AI models
from app.models.ai import (
    Agent, AgentCapability, AgentHealth,
    AgentTask, TaskDependency, TaskResult,
    Workflow, WorkflowStep, WorkflowExecution,
    Execution, ExecutionHistory, ExecutionResult, ExecutionQueue,
    MemoryReference, MemoryEntry, MemoryType,
    PromptTemplate, PromptVersion, PromptUsage,
    AIProvider, ModelProfile, ProviderHealth,
    PerformanceMetric, CostRecord, ReasoningTrace, DecisionLog,
    AgentFeedback, SystemHealth, AuditEvent
)
from app.models.research import (
    ResearchSource, ResearchQuery, ResearchDocument, ResearchCollection,
    ResearchTopic, ResearchSummary, ResearchCitation, ResearchInsight,
    ResearchFact, ResearchKeyword, ResearchEntity, ResearchRelationship,
    ResearchScore, ResearchSnapshot, ResearchCache, ResearchJob,
    ResearchHistory, ResearchBookmark, ResearchFolder, ResearchTag,
    ResearchReport, ResearchAlert, ResearchFeedback,
    ResearchQueryDocument, ResearchDocumentTag, ResearchEntityDocument,
    ResearchReportDocument
)


class Organization(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'organizations'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False)
    description = Column(Text)
    logo_url = Column(String(500))
    website = Column(String(500))
    industry = Column(String(100))
    owner_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    status = Column(String(50), default='active')  # active, inactive, deleted

    members = relationship('OrganizationMember', back_populates='organization', cascade='all, delete-orphan')
    workspaces = relationship('Workspace', back_populates='organization', cascade='all, delete-orphan')
    invitations = relationship('Invitation', back_populates='organization', cascade='all, delete-orphan')
    owner = relationship('User', back_populates='owned_organizations')
    roles = relationship('Role', back_populates='organization', cascade='all, delete-orphan')
    user_roles = relationship('UserRole', back_populates='organization')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'logo_url': self.logo_url,
            'website': self.website,
            'industry': self.industry,
            'owner_id': self.owner_id,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at
        }


class Workspace(Base, TimestampMixin):
    __tablename__ = 'workspaces'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'), nullable=False)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False)
    description = Column(Text)
    timezone = Column(String(50), default='UTC')
    locale = Column(String(10), default='en')
    default_language = Column(String(10), default='en')
    status = Column(String(50), default='active')  # active, inactive

    organization = relationship('Organization', back_populates='workspaces')
    members = relationship('WorkspaceMember', back_populates='workspace', cascade='all, delete-orphan')
    invitations = relationship('Invitation', back_populates='workspace', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'organization_id': self.organization_id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'timezone': self.timezone,
            'locale': self.locale,
            'default_language': self.default_language,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class OrganizationMember(Base, TimestampMixin):
    __tablename__ = 'organization_members'

    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)
    role = Column(String(50), default='member')  # owner, admin, manager, editor, viewer
    invited_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    joined_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    status = Column(String(50), default='active')  # active, inactive, pending

    organization = relationship('Organization', back_populates='members')
    workspace_memberships = relationship('WorkspaceMember', back_populates='organization_member')
    user = relationship('User', back_populates='organization_memberships')
    inviter = relationship('User', foreign_keys=[invited_by])

    def to_dict(self):
        return {
            'organization_id': self.organization_id,
            'user_id': self.user_id,
            'role': self.role,
            'invited_by': self.invited_by,
            'joined_at': self.joined_at,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class WorkspaceMember(Base, TimestampMixin):
    __tablename__ = 'workspace_members'

    workspace_id = Column(UUID(as_uuid=True), ForeignKey('workspaces.id'), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)
    role = Column(String(50), default='member')  # member, admin
    joined_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    workspace = relationship('Workspace', back_populates='members')
    organization_member = relationship('OrganizationMember', back_populates='workspace_memberships')
    user = relationship('User', back_populates='workspace_memberships')

    def to_dict(self):
        return {
            'workspace_id': self.workspace_id,
            'user_id': self.user_id,
            'role': self.role,
            'joined_at': self.joined_at,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class Invitation(Base, TimestampMixin):
    __tablename__ = 'invitations'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), nullable=False)
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'))
    workspace_id = Column(UUID(as_uuid=True), ForeignKey('workspaces.id'))
    token = Column(String(255), unique=True, nullable=False)
    expires_at = Column(DateTime(timezone=True))
    accepted_at = Column(DateTime(timezone=True), nullable=True)
    invited_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    status = Column(String(50), default='pending')  # pending, accepted, expired, cancelled

    organization = relationship('Organization', back_populates='invitations')
    workspace = relationship('Workspace', back_populates='invitations')
    inviter = relationship('User', foreign_keys=[invited_by])

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'organization_id': self.organization_id,
            'workspace_id': self.workspace_id,
            'token': self.token,
            'expires_at': self.expires_at,
            'accepted_at': self.accepted_at,
            'invited_by': self.invited_by,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class User(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(500), nullable=False)
    full_name = Column(String(500))
    avatar_url = Column(String(500))
    role = Column(String(50), default='user')  # user, admin

    owned_organizations = relationship('Organization', back_populates='owner')
    organization_memberships = relationship('OrganizationMember', back_populates='user')
    workspace_memberships = relationship('WorkspaceMember', back_populates='user')
    invited_organizations = relationship('Organization', foreign_keys=[Organization.owner_id])
    user_roles = relationship('UserRole', back_populates='user')

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'full_name': self.full_name,
            'avatar_url': self.avatar_url,
            'role': self.role,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at
        }
