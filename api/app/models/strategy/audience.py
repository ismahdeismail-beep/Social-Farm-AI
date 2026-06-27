"""
Audience Segment Models

Audience analysis and segmentation.
"""

from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Integer, Float, JSON as JSONType
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

from app.models import Base, TimestampMixin, SoftDeleteMixin


class AudienceSegment(Base, TimestampMixin, SoftDeleteMixin):
    """
    Defined audience segment for targeting.
    """
    __tablename__ = 'audience_segments'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_id = Column(UUID(as_uuid=True), ForeignKey('content_strategies.id'), nullable=False)
    
    # Segment definition
    name = Column(String(255), nullable=False)
    description = Column(Text)
    segment_type = Column(String(100), nullable=False)  # demographic, behavioral, psychographic, interest
    
    # Demographics
    age_range = Column(JSONType)  # {min: 18, max: 35}
    gender_distribution = Column(JSONType)  # {male: 40, female: 55, other: 5}
    location = Column(JSONType)  # {countries: [...], regions: [...]}
    language = Column(JSONType, default=list)
    
    # Psychographics
    interests = Column(JSONType, default=list)
    values = Column(JSONType, default=list)
    lifestyle = Column(JSONType, default=list)
    personality_traits = Column(JSONType, default=list)
    
    # Behavior
    platform_usage = Column(JSONType, default=dict)  # {platform: hours_per_day}
    content_preferences = Column(JSONType, default=list)
    purchase_behavior = Column(JSONType, default=dict)
    engagement_patterns = Column(JSONType, default=dict)
    
    # Size and value
    estimated_size = Column(Integer, default=0)
    growth_rate = Column(Float, default=0.0)
    lifetime_value = Column(Float, default=0.0)
    acquisition_cost = Column(Float, default=0.0)
    
    # Platform preferences
    primary_platforms = Column(JSONType, default=list)
    secondary_platforms = Column(JSONType, default=list)
    
    # Content affinity
    preferred_content_types = Column(JSONType, default=list)
    preferred_formats = Column(JSONType, default=list)
    optimal_posting_times = Column(JSONType, default=dict)
    
    # Status
    is_primary = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'strategy_id': self.strategy_id,
            'name': self.name,
            'description': self.description,
            'segment_type': self.segment_type,
            'age_range': self.age_range,
            'gender_distribution': self.gender_distribution,
            'location': self.location,
            'language': self.language,
            'interests': self.interests,
            'values': self.values,
            'lifestyle': self.lifestyle,
            'personality_traits': self.personality_traits,
            'platform_usage': self.platform_usage,
            'content_preferences': self.content_preferences,
            'purchase_behavior': self.purchase_behavior,
            'engagement_patterns': self.engagement_patterns,
            'estimated_size': self.estimated_size,
            'growth_rate': self.growth_rate,
            'lifetime_value': self.lifetime_value,
            'acquisition_cost': self.acquisition_cost,
            'primary_platforms': self.primary_platforms,
            'secondary_platforms': self.secondary_platforms,
            'preferred_content_types': self.preferred_content_types,
            'preferred_formats': self.preferred_formats,
            'optimal_posting_times': self.optimal_posting_times,
            'is_primary': self.is_primary,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at
        }
