"""
Content Strategy Models

Core strategy models for the Content Strategy Agent.
"""

from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Integer, Float, JSON as JSONType
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

from app.models import Base, TimestampMixin, SoftDeleteMixin


class ContentStrategy(Base, TimestampMixin, SoftDeleteMixin):
    """
    Master content strategy for a brand/project.
    
    This is the central document that guides all content creation.
    """
    __tablename__ = 'content_strategies'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Ownership
    brand_id = Column(UUID(as_uuid=True), ForeignKey('brands.id'), nullable=False)
    project_id = Column(UUID(as_uuid=True))
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    
    # Strategy definition
    name = Column(String(255), nullable=False)
    description = Column(Text)
    strategy_type = Column(String(100), nullable=False)  # quarterly, monthly, campaign, always_on
    
    # Timeframe
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    
    # Vision and goals
    vision = Column(Text)
    mission = Column(Text)
    goals = Column(JSONType, default=list)  # List of strategic goals
    kpis = Column(JSONType, default=list)  # Key performance indicators
    
    # Content pillars
    content_pillars = Column(JSONType, default=list)  # Core content themes
    content_mix = Column(JSONType, default=dict)  # Percentage breakdown by content type
    
    # Budget and resources
    budget_usd = Column(Float, default=0.0)
    allocated_resources = Column(JSONType, default=dict)
    
    # Status
    status = Column(String(50), default='draft')  # draft, active, paused, completed, archived
    version = Column(Integer, default=1)
    approval_status = Column(String(50), default='pending')  # pending, approved, rejected
    
    # AI Generation metadata
    generated_by_ai = Column(Boolean, default=False)
    ai_confidence_score = Column(Float, default=0.0)
    ai_model_used = Column(String(100))
    
    # Relationships
    brand = relationship('Brand')
    creator = relationship('User', foreign_keys=[created_by])
    plans = relationship('ContentPlan', back_populates='strategy', cascade='all, delete-orphan')
    campaigns = relationship('CampaignStrategy', back_populates='strategy', cascade='all, delete-orphan')
    opportunities = relationship('ContentOpportunity', back_populates='strategy', cascade='all, delete-orphan')
    themes = relationship('ContentTheme', back_populates='strategy', cascade='all, delete-orphan')
    platform_strategies = relationship('PlatformStrategy', back_populates='strategy', cascade='all, delete-orphan')
    revisions = relationship('StrategyRevision', back_populates='strategy', cascade='all, delete-orphan')
    approvals = relationship('StrategyApproval', back_populates='strategy', cascade='all, delete-orphan')
    forecasts = relationship('ContentForecast', back_populates='strategy', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'brand_id': self.brand_id,
            'project_id': self.project_id,
            'name': self.name,
            'description': self.description,
            'strategy_type': self.strategy_type,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'vision': self.vision,
            'mission': self.mission,
            'goals': self.goals,
            'kpis': self.kpis,
            'content_pillars': self.content_pillars,
            'content_mix': self.content_mix,
            'budget_usd': self.budget_usd,
            'status': self.status,
            'version': self.version,
            'approval_status': self.approval_status,
            'generated_by_ai': self.generated_by_ai,
            'ai_confidence_score': self.ai_confidence_score,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class StrategyRevision(Base, TimestampMixin):
    """
    Tracks revisions to a content strategy.
    """
    __tablename__ = 'strategy_revisions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_id = Column(UUID(as_uuid=True), ForeignKey('content_strategies.id'), nullable=False)
    
    # Revision
    version_number = Column(Integer, nullable=False)
    changes = Column(JSONType, default=dict)
    change_summary = Column(Text)
    
    # Who
    revised_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    revision_reason = Column(String(255))
    
    # Approval
    approved = Column(Boolean, default=False)
    approved_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    approved_at = Column(DateTime(timezone=True))
    
    # Relationships
    strategy = relationship('ContentStrategy', back_populates='revisions')
    reviser = relationship('User', foreign_keys=[revised_by])
    approver = relationship('User', foreign_keys=[approved_by])
    
    def to_dict(self):
        return {
            'id': self.id,
            'strategy_id': self.strategy_id,
            'version_number': self.version_number,
            'changes': self.changes,
            'change_summary': self.change_summary,
            'revised_by': self.revised_by,
            'revision_reason': self.revision_reason,
            'approved': self.approved,
            'approved_by': self.approved_by,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class StrategyApproval(Base, TimestampMixin):
    """
    Approval workflow for strategies.
    """
    __tablename__ = 'strategy_approvals'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_id = Column(UUID(as_uuid=True), ForeignKey('content_strategies.id'), nullable=False)
    
    # Approval
    status = Column(String(50), default='pending')  # pending, approved, rejected, revision_requested
    reviewer_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    review_notes = Column(Text)
    
    # Timing
    requested_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    reviewed_at = Column(DateTime(timezone=True))
    
    # Relationships
    strategy = relationship('ContentStrategy', back_populates='approvals')
    reviewer = relationship('User', foreign_keys=[reviewer_id])
    
    def to_dict(self):
        return {
            'id': self.id,
            'strategy_id': self.strategy_id,
            'status': self.status,
            'reviewer_id': self.reviewer_id,
            'review_notes': self.review_notes,
            'requested_at': self.requested_at.isoformat() if self.requested_at else None,
            'reviewed_at': self.reviewed_at.isoformat() if self.reviewed_at else None,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
