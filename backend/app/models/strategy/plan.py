"""
Content Plan & Calendar Models

Defines content plans and calendar scheduling.
"""

from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Integer, Float, JSON as JSONType
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

from app.models import Base, TimestampMixin, SoftDeleteMixin


class ContentPlan(Base, TimestampMixin, SoftDeleteMixin):
    """
    Detailed content plan for a specific time period.
    """
    __tablename__ = 'content_plans'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_id = Column(UUID(as_uuid=True), ForeignKey('content_strategies.id'), nullable=False)
    
    # Plan definition
    name = Column(String(255), nullable=False)
    description = Column(Text)
    plan_type = Column(String(50), nullable=False)  # daily, weekly, monthly, quarterly
    
    # Timeframe
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    
    # Content targets
    target_posts = Column(Integer, default=0)
    target_reach = Column(Integer, default=0)
    target_engagement = Column(Float, default=0.0)
    
    # Content breakdown
    content_types = Column(JSONType, default=dict)  # {type: count}
    platform_distribution = Column(JSONType, default=dict)  # {platform: percentage}
    
    # Status
    status = Column(String(50), default='draft')  # draft, active, completed
    completion_percentage = Column(Float, default=0.0)
    
    # Relationships
    strategy = relationship('ContentStrategy', back_populates='plans')
    calendar_entries = relationship('ContentCalendar', back_populates='plan', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'strategy_id': self.strategy_id,
            'name': self.name,
            'description': self.description,
            'plan_type': self.plan_type,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'target_posts': self.target_posts,
            'target_reach': self.target_reach,
            'target_engagement': self.target_engagement,
            'content_types': self.content_types,
            'platform_distribution': self.platform_distribution,
            'status': self.status,
            'completion_percentage': self.completion_percentage,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at
        }


class ContentCalendar(Base, TimestampMixin):
    """
    Individual content calendar entries.
    
    Represents scheduled content pieces.
    """
    __tablename__ = 'content_calendars'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id = Column(UUID(as_uuid=True), ForeignKey('content_plans.id'), nullable=False)
    
    # Content details
    title = Column(String(255), nullable=False)
    description = Column(Text)
    content_type = Column(String(100), nullable=False)  # post, reel, story, video, carousel, etc.
    
    # Platform
    platform = Column(String(50), nullable=False)  # tiktok, instagram, youtube, etc.
    platform_format = Column(String(100))  # platform-specific format
    
    # Scheduling
    scheduled_date = Column(DateTime(timezone=True), nullable=False)
    scheduled_time = Column(String(10))  # HH:MM format
    timezone = Column(String(50), default='UTC')
    
    # Content details
    topic = Column(String(255))
    hook = Column(Text)  # Opening hook
    caption = Column(Text)
    hashtags = Column(JSONType, default=list)
    mentions = Column(JSONType, default=list)
    
    # Visual requirements
    visual_style = Column(String(100))
    color_scheme = Column(JSONType)
    text_overlay = Column(Text)
    
    # Performance targets
    target_reach = Column(Integer, default=0)
    target_engagement_rate = Column(Float, default=0.0)
    target_clicks = Column(Integer, default=0)
    
    # Status
    status = Column(String(50), default='planned')  # planned, in_progress, ready, published, archived
    priority = Column(Integer, default=0)
    
    # Downstream references
    script_id = Column(UUID(as_uuid=True))
    media_id = Column(UUID(as_uuid=True))
    publish_job_id = Column(UUID(as_uuid=True))
    
    # Relationships
    plan = relationship('ContentPlan', back_populates='calendar_entries')
    
    def to_dict(self):
        return {
            'id': self.id,
            'plan_id': self.plan_id,
            'title': self.title,
            'description': self.description,
            'content_type': self.content_type,
            'platform': self.platform,
            'platform_format': self.platform_format,
            'scheduled_date': self.scheduled_date.isoformat() if self.scheduled_date else None,
            'scheduled_time': self.scheduled_time,
            'timezone': self.timezone,
            'topic': self.topic,
            'hook': self.hook,
            'caption': self.caption,
            'hashtags': self.hashtags,
            'mentions': self.mentions,
            'visual_style': self.visual_style,
            'color_scheme': self.color_scheme,
            'text_overlay': self.text_overlay,
            'target_reach': self.target_reach,
            'target_engagement_rate': self.target_engagement_rate,
            'target_clicks': self.target_clicks,
            'status': self.status,
            'priority': self.priority,
            'script_id': self.script_id,
            'media_id': self.media_id,
            'publish_job_id': self.publish_job_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
