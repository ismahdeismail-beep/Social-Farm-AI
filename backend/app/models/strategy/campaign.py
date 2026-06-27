"""
Campaign Strategy Models

Campaign planning and management.
"""

from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Integer, Float, JSON as JSONType
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

from app.models import Base, TimestampMixin, SoftDeleteMixin


class CampaignStrategy(Base, TimestampMixin, SoftDeleteMixin):
    """
    Campaign strategy definition.
    """
    __tablename__ = 'campaign_strategies'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_id = Column(UUID(as_uuid=True), ForeignKey('content_strategies.id'), nullable=False)
    
    # Campaign definition
    name = Column(String(255), nullable=False)
    description = Column(Text)
    campaign_type = Column(String(100), nullable=False)  # product_launch, awareness, sales, seasonal, etc.
    
    # Timeline
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    launch_date = Column(DateTime(timezone=True))
    
    # Goals
    objectives = Column(JSONType, default=list)  # List of CampaignObjective references
    target_metrics = Column(JSONType, default=dict)
    success_criteria = Column(JSONType, default=list)
    
    # Budget
    budget_usd = Column(Float, default=0.0)
    budget_breakdown = Column(JSONType, default=dict)
    
    # Audience
    target_audiences = Column(JSONType, default=list)
    audience_segments = Column(JSONType, default=list)
    
    # Platforms
    platforms = Column(JSONType, default=list)
    platform_specific_strategy = Column(JSONType, default=dict)
    
    # Content
    content_themes = Column(JSONType, default=list)
    key_messages = Column(JSONType, default=list)
    hashtags = Column(JSONType, default=list)
    visual_guidelines = Column(JSONType, default=dict)
    
    # Status
    status = Column(String(50), default='planned')  # planned, active, paused, completed, cancelled
    progress_percentage = Column(Float, default=0.0)
    
    # Performance
    actual_metrics = Column(JSONType, default=dict)
    roi = Column(Float, default=0.0)
    
    # Relationships
    strategy = relationship('ContentStrategy', back_populates='campaigns')
    objectives_list = relationship('CampaignObjective', back_populates='campaign', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'strategy_id': self.strategy_id,
            'name': self.name,
            'description': self.description,
            'campaign_type': self.campaign_type,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'launch_date': self.launch_date.isoformat() if self.launch_date else None,
            'objectives': self.objectives,
            'target_metrics': self.target_metrics,
            'success_criteria': self.success_criteria,
            'budget_usd': self.budget_usd,
            'budget_breakdown': self.budget_breakdown,
            'target_audiences': self.target_audiences,
            'audience_segments': self.audience_segments,
            'platforms': self.platforms,
            'platform_specific_strategy': self.platform_specific_strategy,
            'content_themes': self.content_themes,
            'key_messages': self.key_messages,
            'hashtags': self.hashtags,
            'visual_guidelines': self.visual_guidelines,
            'status': self.status,
            'progress_percentage': self.progress_percentage,
            'actual_metrics': self.actual_metrics,
            'roi': self.roi,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at
        }


class CampaignObjective(Base, TimestampMixin):
    """
    Specific objectives for a campaign.
    """
    __tablename__ = 'campaign_objectives'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    campaign_id = Column(UUID(as_uuid=True), ForeignKey('campaign_strategies.id'), nullable=False)
    
    # Objective
    name = Column(String(255), nullable=False)
    description = Column(Text)
    objective_type = Column(String(100), nullable=False)  # awareness, engagement, conversion, retention
    
    # Target
    target_value = Column(Float, nullable=False)
    current_value = Column(Float, default=0.0)
    unit = Column(String(50))  # impressions, clicks, conversions, etc.
    
    # Timeline
    target_date = Column(DateTime(timezone=True))
    
    # Status
    status = Column(String(50), default='active')  # active, achieved, missed
    achieved_at = Column(DateTime(timezone=True))
    
    # Relationships
    campaign = relationship('CampaignStrategy', back_populates='objectives_list')
    
    def to_dict(self):
        return {
            'id': self.id,
            'campaign_id': self.campaign_id,
            'name': self.name,
            'description': self.description,
            'objective_type': self.objective_type,
            'target_value': self.target_value,
            'current_value': self.current_value,
            'unit': self.unit,
            'target_date': self.target_date.isoformat() if self.target_date else None,
            'status': self.status,
            'achieved_at': self.achieved_at.isoformat() if self.achieved_at else None,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
