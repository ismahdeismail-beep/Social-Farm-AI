"""
Platform Strategy Models

Platform-specific content strategies.
"""

from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Integer, Float, JSON as JSONType
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

from app.models import Base, TimestampMixin, SoftDeleteMixin


class PlatformStrategy(Base, TimestampMixin, SoftDeleteMixin):
    """
    Platform-specific content strategy.
    """
    __tablename__ = 'platform_strategies'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_id = Column(UUID(as_uuid=True), ForeignKey('content_strategies.id'), nullable=False)
    
    # Platform
    platform = Column(String(50), nullable=False)  # tiktok, instagram, youtube, etc.
    account_handle = Column(String(255))
    
    # Goals
    follower_target = Column(Integer, default=0)
    growth_rate_target = Column(Float, default=0.0)
    engagement_rate_target = Column(Float, default=0.0)
    reach_target = Column(Integer, default=0)
    
    # Content strategy
    posting_frequency = Column(JSONType, default=dict)  # {daily: 2, weekly: 10, monthly: 40}
    content_mix = Column(JSONType, default=dict)  # {educational: 30, entertainment: 40, promotional: 30}
    optimal_times = Column(JSONType, default=list)  # [{day: 'monday', time: '18:00'}, ...]
    
    # Formats
    primary_formats = Column(JSONType, default=list)  # [reel, carousel, story]
    secondary_formats = Column(JSONType, default=list)
    format_guidelines = Column(JSONType, default=dict)
    
    # Algorithm considerations
    algorithm_factors = Column(JSONType, default=list)  # Key factors for the platform algorithm
    best_practices = Column(JSONType, default=list)
    common_mistakes = Column(JSONType, default=list)
    
    # Hashtag strategy
    hashtag_tiers = Column(JSONType, default=dict)  # {branded: [...], industry: [...], trending: [...]}
    hashtag_count = Column(Integer, default=10)
    
    # Engagement strategy
    response_strategy = Column(Text)
    community_building = Column(JSONType, default=list)
    collaboration_opportunities = Column(JSONType, default=list)
    
    # Performance benchmarks
    industry_benchmarks = Column(JSONType, default=dict)
    competitor_benchmarks = Column(JSONType, default=dict)
    
    # Status
    is_active = Column(Boolean, default=True)
    priority = Column(Integer, default=0)
    
    # Relationships
    strategy = relationship('ContentStrategy', back_populates='platform_strategies')
    
    def to_dict(self):
        return {
            'id': self.id,
            'strategy_id': self.strategy_id,
            'platform': self.platform,
            'account_handle': self.account_handle,
            'follower_target': self.follower_target,
            'growth_rate_target': self.growth_rate_target,
            'engagement_rate_target': self.engagement_rate_target,
            'reach_target': self.reach_target,
            'posting_frequency': self.posting_frequency,
            'content_mix': self.content_mix,
            'optimal_times': self.optimal_times,
            'primary_formats': self.primary_formats,
            'secondary_formats': self.secondary_formats,
            'format_guidelines': self.format_guidelines,
            'algorithm_factors': self.algorithm_factors,
            'best_practices': self.best_practices,
            'common_mistakes': self.common_mistakes,
            'hashtag_tiers': self.hashtag_tiers,
            'hashtag_count': self.hashtag_count,
            'response_strategy': self.response_strategy,
            'community_building': self.community_building,
            'collaboration_opportunities': self.collaboration_opportunities,
            'industry_benchmarks': self.industry_benchmarks,
            'competitor_benchmarks': self.competitor_benchmarks,
            'is_active': self.is_active,
            'priority': self.priority,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at
        }
