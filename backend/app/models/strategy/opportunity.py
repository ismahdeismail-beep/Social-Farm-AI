"""
Content Opportunity Models

Detects and tracks content opportunities.
"""

from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Integer, Float, JSON as JSONType
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

from app.models import Base, TimestampMixin, SoftDeleteMixin


class ContentOpportunity(Base, TimestampMixin, SoftDeleteMixin):
    """
    Represents a detected content opportunity.
    """
    __tablename__ = 'content_opportunities'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_id = Column(UUID(as_uuid=True), ForeignKey('content_strategies.id'), nullable=False)
    
    # Opportunity details
    title = Column(String(255), nullable=False)
    description = Column(Text)
    opportunity_type = Column(String(100), nullable=False)  # trend, gap, seasonal, competitor, evergreen
    
    # Source
    source_type = Column(String(50))  # trend_engine, research, competitor, manual
    source_id = Column(UUID(as_uuid=True))
    source_url = Column(String(500))
    
    # Scoring
    priority_score = Column(Float, default=0.5)  # 0.0 to 1.0
    virality_potential = Column(Float, default=0.5)
    audience_relevance = Column(Float, default=0.5)
    brand_alignment = Column(Float, default=0.5)
    competition_level = Column(Float, default=0.5)  # 0 = low, 1 = high
    roi_estimate = Column(Float, default=0.0)
    
    # Timing
    detected_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime(timezone=True))
    optimal_posting_window = Column(JSONType)  # {start: datetime, end: datetime}
    
    # Content suggestions
    suggested_formats = Column(JSONType, default=list)
    suggested_platforms = Column(JSONType, default=list)
    suggested_hooks = Column(JSONType, default=list)
    suggested_angles = Column(JSONType, default=list)
    
    # Keywords and topics
    keywords = Column(JSONType, default=list)
    topics = Column(JSONType, default=list)
    hashtags = Column(JSONType, default=list)
    
    # Status
    status = Column(String(50), default='detected')  # detected, reviewed, accepted, rejected, expired
    reviewed_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    review_notes = Column(Text)
    
    # Relationships
    strategy = relationship('ContentStrategy', back_populates='opportunities')
    
    def to_dict(self):
        return {
            'id': self.id,
            'strategy_id': self.strategy_id,
            'title': self.title,
            'description': self.description,
            'opportunity_type': self.opportunity_type,
            'source_type': self.source_type,
            'source_id': self.source_id,
            'source_url': self.source_url,
            'priority_score': self.priority_score,
            'virality_potential': self.virality_potential,
            'audience_relevance': self.audience_relevance,
            'brand_alignment': self.brand_alignment,
            'competition_level': self.competition_level,
            'roi_estimate': self.roi_estimate,
            'detected_at': self.detected_at.isoformat() if self.detected_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'optimal_posting_window': self.optimal_posting_window,
            'suggested_formats': self.suggested_formats,
            'suggested_platforms': self.suggested_platforms,
            'suggested_hooks': self.suggested_hooks,
            'suggested_angles': self.suggested_angles,
            'keywords': self.keywords,
            'topics': self.topics,
            'hashtags': self.hashtags,
            'status': self.status,
            'reviewed_by': self.reviewed_by,
            'review_notes': self.review_notes,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at
        }


class ContentGap(Base, TimestampMixin):
    """
    Identified gaps in content coverage.
    """
    __tablename__ = 'content_gaps'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_id = Column(UUID(as_uuid=True), ForeignKey('content_strategies.id'), nullable=False)
    
    # Gap details
    title = Column(String(255), nullable=False)
    description = Column(Text)
    gap_type = Column(String(100), nullable=False)  # topic, format, platform, audience, timing
    
    # Analysis
    current_coverage = Column(Float, default=0.0)  # 0-100%
    target_coverage = Column(Float, default=100.0)
    gap_size = Column(Float, default=0.0)
    
    # Impact
    potential_impact = Column(Float, default=0.5)  # 0.0 to 1.0
    effort_required = Column(Float, default=0.5)  # 0.0 to 1.0
    priority = Column(Integer, default=0)
    
    # Recommendations
    recommended_actions = Column(JSONType, default=list)
    recommended_content_types = Column(JSONType, default=list)
    recommended_platforms = Column(JSONType, default=list)
    
    # Status
    status = Column(String(50), default='identified')  # identified, in_progress, resolved
    resolved_at = Column(DateTime(timezone=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'strategy_id': self.strategy_id,
            'title': self.title,
            'description': self.description,
            'gap_type': self.gap_type,
            'current_coverage': self.current_coverage,
            'target_coverage': self.target_coverage,
            'gap_size': self.gap_size,
            'potential_impact': self.potential_impact,
            'effort_required': self.effort_required,
            'priority': self.priority,
            'recommended_actions': self.recommended_actions,
            'recommended_content_types': self.recommended_content_types,
            'recommended_platforms': self.recommended_platforms,
            'status': self.status,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
