"""
Strategy Metrics & Feedback Models

Metrics tracking and feedback collection.
"""

from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Integer, Float, JSON as JSONType
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

from app.models import Base, TimestampMixin, SoftDeleteMixin


class StrategyMetrics(Base, TimestampMixin):
    """
    Performance metrics for content strategy.
    """
    __tablename__ = 'strategy_metrics'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_id = Column(UUID(as_uuid=True), ForeignKey('content_strategies.id'), nullable=False)
    
    # Metric
    metric_name = Column(String(255), nullable=False)
    metric_type = Column(String(100), nullable=False)  # engagement, reach, growth, revenue, efficiency
    
    # Value
    target_value = Column(Float, default=0.0)
    actual_value = Column(Float, default=0.0)
    variance = Column(Float, default=0.0)
    variance_percentage = Column(Float, default=0.0)
    
    # Timeframe
    period_start = Column(DateTime(timezone=True))
    period_end = Column(DateTime(timezone=True))
    
    # Breakdown
    by_platform = Column(JSONType, default=dict)
    by_content_type = Column(JSONType, default=dict)
    by_audience = Column(JSONType, default=dict)
    
    # Trend
    trend = Column(String(50))  # improving, stable, declining
    change_rate = Column(Float, default=0.0)
    
    # Benchmark
    industry_benchmark = Column(Float)
    competitor_benchmark = Column(Float)
    
    def to_dict(self):
        return {
            'id': self.id,
            'strategy_id': self.strategy_id,
            'metric_name': self.metric_name,
            'metric_type': self.metric_type,
            'target_value': self.target_value,
            'actual_value': self.actual_value,
            'variance': self.variance,
            'variance_percentage': self.variance_percentage,
            'period_start': self.period_start.isoformat() if self.period_start else None,
            'period_end': self.period_end.isoformat() if self.period_end else None,
            'by_platform': self.by_platform,
            'by_content_type': self.by_content_type,
            'by_audience': self.by_audience,
            'trend': self.trend,
            'change_rate': self.change_rate,
            'industry_benchmark': self.industry_benchmark,
            'competitor_benchmark': self.competitor_benchmark,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class StrategyFeedback(Base, TimestampMixin):
    """
    Feedback on content strategy.
    """
    __tablename__ = 'strategy_feedback'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_id = Column(UUID(as_uuid=True), ForeignKey('content_strategies.id'), nullable=False)
    
    # Feedback
    feedback_type = Column(String(50), nullable=False)  # internal, external, ai_generated
    category = Column(String(100))  # content, timing, targeting, budget,创意
    
    # Rating
    rating = Column(Integer)  # 1-5
    sentiment = Column(String(50))  # positive, neutral, negative
    
    # Content
    feedback_text = Column(Text)
    suggested_improvements = Column(JSONType, default=list)
    
    # Source
    source = Column(String(100))  # team_member, client, audience, ai
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    
    # Status
    status = Column(String(50), default='new')  # new, reviewed, implemented, dismissed
    implemented_at = Column(DateTime(timezone=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'strategy_id': self.strategy_id,
            'feedback_type': self.feedback_type,
            'category': self.category,
            'rating': self.rating,
            'sentiment': self.sentiment,
            'feedback_text': self.feedback_text,
            'suggested_improvements': self.suggested_improvements,
            'source': self.source,
            'user_id': self.user_id,
            'status': self.status,
            'implemented_at': self.implemented_at.isoformat() if self.implemented_at else None,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
