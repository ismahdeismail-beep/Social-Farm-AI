"""
Content Recommendation Models

AI-generated content recommendations.
"""

from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Integer, Float, JSON as JSONType
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

from app.models import Base, TimestampMixin, SoftDeleteMixin


class ContentRecommendation(Base, TimestampMixin, SoftDeleteMixin):
    """
    AI-generated content recommendation.
    """
    __tablename__ = 'content_recommendations'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_id = Column(UUID(as_uuid=True), ForeignKey('content_strategies.id'), nullable=False)
    
    # Recommendation
    title = Column(String(255), nullable=False)
    description = Column(Text)
    recommendation_type = Column(String(100), nullable=False)  # content, campaign, theme, format, timing
    
    # Content details
    content_idea = Column(Text)
    hook = Column(Text)
    key_points = Column(JSONType, default=list)
    call_to_action = Column(Text)
    
    # Targeting
    target_audience = Column(JSONType, default=list)
    target_platforms = Column(JSONType, default=list)
    target_timing = Column(JSONType)
    
    # Scoring
    relevance_score = Column(Float, default=0.5)
    confidence_score = Column(Float, default=0.5)
    expected_performance = Column(JSONType, default=dict)
    
    # AI metadata
    generated_by = Column(String(100))  # agent name
    model_used = Column(String(100))
    reasoning = Column(Text)
    
    # Status
    status = Column(String(50), default='new')  # new, reviewed, accepted, rejected, implemented
    implemented_at = Column(DateTime(timezone=True))
    
    # Downstream
    content_plan_id = Column(UUID(as_uuid=True), ForeignKey('content_plans.id'))
    
    def to_dict(self):
        return {
            'id': self.id,
            'strategy_id': self.strategy_id,
            'title': self.title,
            'description': self.description,
            'recommendation_type': self.recommendation_type,
            'content_idea': self.content_idea,
            'hook': self.hook,
            'key_points': self.key_points,
            'call_to_action': self.call_to_action,
            'target_audience': self.target_audience,
            'target_platforms': self.target_platforms,
            'target_timing': self.target_timing,
            'relevance_score': self.relevance_score,
            'confidence_score': self.confidence_score,
            'expected_performance': self.expected_performance,
            'generated_by': self.generated_by,
            'model_used': self.model_used,
            'reasoning': self.reasoning,
            'status': self.status,
            'implemented_at': self.implemented_at.isoformat() if self.implemented_at else None,
            'content_plan_id': self.content_plan_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at
        }


class ContentPriority(Base, TimestampMixin):
    """
    Priority scoring for content items.
    """
    __tablename__ = 'content_priorities'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Reference
    content_type = Column(String(50), nullable=False)  # recommendation, opportunity, calendar_entry
    content_id = Column(UUID(as_uuid=True), nullable=False)
    
    # Priority scoring
    overall_priority = Column(Float, default=0.5)  # 0.0 to 1.0
    
    # Factor scores
    urgency_score = Column(Float, default=0.5)
    impact_score = Column(Float, default=0.5)
    effort_score = Column(Float, default=0.5)
    trend_score = Column(Float, default=0.5)
    audience_score = Column(Float, default=0.5)
    brand_score = Column(Float, default=0.5)
    
    # Context
    scoring_reasons = Column(JSONType, default=list)
    scoring_model = Column(String(100))
    
    # Status
    is_current = Column(Boolean, default=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'content_type': self.content_type,
            'content_id': self.content_id,
            'overall_priority': self.overall_priority,
            'urgency_score': self.urgency_score,
            'impact_score': self.impact_score,
            'effort_score': self.effort_score,
            'trend_score': self.trend_score,
            'audience_score': self.audience_score,
            'brand_score': self.brand_score,
            'scoring_reasons': self.scoring_reasons,
            'scoring_model': self.scoring_model,
            'is_current': self.is_current,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
