"""
Content Theme & Series Models

Content themes and series planning.
"""

from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Integer, Float, JSON as JSONType
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

from app.models import Base, TimestampMixin, SoftDeleteMixin


class ContentTheme(Base, TimestampMixin, SoftDeleteMixin):
    """
    Content theme definition.
    """
    __tablename__ = 'content_themes'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_id = Column(UUID(as_uuid=True), ForeignKey('content_strategies.id'), nullable=False)
    
    # Theme definition
    name = Column(String(255), nullable=False)
    description = Column(Text)
    theme_type = Column(String(100), nullable=False)  # evergreen, trending, seasonal, campaign
    
    # Content
    keywords = Column(JSONType, default=list)
    topics = Column(JSONType, default=list)
    hashtags = Column(JSONType, default=list)
    
    # Pillars
    content_pillar = Column(String(100))  # Which pillar this theme belongs to
    
    # Performance
    historical_performance = Column(JSONType, default=dict)
    predicted_performance = Column(Float, default=0.5)
    
    # Timing
    best_posting_times = Column(JSONType, default=list)
    seasonality = Column(JSONType)  # {months: [1, 6, 12], events: [...]}
    
    # Platforms
    applicable_platforms = Column(JSONType, default=list)
    platform_specific_angles = Column(JSONType, default=dict)
    
    # Status
    is_active = Column(Boolean, default=True)
    priority = Column(Integer, default=0)
    
    # Relationships
    strategy = relationship('ContentStrategy', back_populates='themes')
    series = relationship('ContentSeries', back_populates='theme', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'strategy_id': self.strategy_id,
            'name': self.name,
            'description': self.description,
            'theme_type': self.theme_type,
            'keywords': self.keywords,
            'topics': self.topics,
            'hashtags': self.hashtags,
            'content_pillar': self.content_pillar,
            'historical_performance': self.historical_performance,
            'predicted_performance': self.predicted_performance,
            'best_posting_times': self.best_posting_times,
            'seasonality': self.seasonality,
            'applicable_platforms': self.applicable_platforms,
            'platform_specific_angles': self.platform_specific_angles,
            'is_active': self.is_active,
            'priority': self.priority,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at
        }


class ContentSeries(Base, TimestampMixin, SoftDeleteMixin):
    """
    Content series within a theme.
    """
    __tablename__ = 'content_series'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    theme_id = Column(UUID(as_uuid=True), ForeignKey('content_themes.id'), nullable=False)
    
    # Series definition
    name = Column(String(255), nullable=False)
    description = Column(Text)
    series_type = Column(String(100))  # tutorial, tips, behind_scenes, case_study, interview
    
    # Structure
    episode_count = Column(Integer, default=0)
    current_episode = Column(Integer, default=0)
    episode_format = Column(JSONType, default=dict)
    
    # Content
    topics = Column(JSONType, default=list)
    key_messages = Column(JSONType, default=list)
    
    # Timing
    frequency = Column(String(50))  # daily, weekly, biweekly, monthly
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    
    # Performance
    avg_engagement = Column(Float, default=0.0)
    total_reach = Column(Integer, default=0)
    
    # Status
    status = Column(String(50), default='planned')  # planned, active, completed, paused
    
    # Relationships
    theme = relationship('ContentTheme', back_populates='series')
    
    def to_dict(self):
        return {
            'id': self.id,
            'theme_id': self.theme_id,
            'name': self.name,
            'description': self.description,
            'series_type': self.series_type,
            'episode_count': self.episode_count,
            'current_episode': self.current_episode,
            'episode_format': self.episode_format,
            'topics': self.topics,
            'key_messages': self.key_messages,
            'frequency': self.frequency,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'avg_engagement': self.avg_engagement,
            'total_reach': self.total_reach,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at
        }
