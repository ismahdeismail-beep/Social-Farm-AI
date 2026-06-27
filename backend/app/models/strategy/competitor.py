"""
Competitor Insight Models

Competitor analysis and intelligence.
"""

from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Integer, Float, JSON as JSONType
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

from app.models import Base, TimestampMixin, SoftDeleteMixin


class CompetitorInsight(Base, TimestampMixin, SoftDeleteMixin):
    """
    Competitor analysis and insights.
    """
    __tablename__ = 'competitor_insights'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_id = Column(UUID(as_uuid=True), ForeignKey('content_strategies.id'), nullable=False)
    
    # Competitor
    competitor_name = Column(String(255), nullable=False)
    competitor_handle = Column(String(255))
    competitor_url = Column(String(500))
    
    # Analysis period
    analysis_start_date = Column(DateTime(timezone=True))
    analysis_end_date = Column(DateTime(timezone=True))
    
    # Platform presence
    platforms = Column(JSONType, default=dict)  # {platform: {followers, engagement_rate, posting_frequency}}
    
    # Content analysis
    top_content_types = Column(JSONType, default=list)
    content_themes = Column(JSONType, default=list)
    posting_patterns = Column(JSONType, default=dict)
    
    # Performance metrics
    avg_engagement_rate = Column(Float, default=0.0)
    avg_reach = Column(Integer, default=0)
    avg_likes = Column(Integer, default=0)
    avg_comments = Column(Integer, default=0)
    avg_shares = Column(Integer, default=0)
    
    # Top performing content
    top_posts = Column(JSONType, default=list)  # [{title, url, engagement, ...}]
    viral_content = Column(JSONType, default=list)
    
    # Strengths and weaknesses
    strengths = Column(JSONType, default=list)
    weaknesses = Column(JSONType, default=list)
    opportunities = Column(JSONType, default=list)
    threats = Column(JSONType, default=list)
    
    # Gaps we can exploit
    content_gaps = Column(JSONType, default=list)
    audience_gaps = Column(JSONType, default=list)
    platform_gaps = Column(JSONType, default=list)
    
    # Hashtag strategy
    popular_hashtags = Column(JSONType, default=list)
    hashtag_frequency = Column(JSONType, default=dict)
    
    # Collaboration and influencer
    influencer_partnerships = Column(JSONType, default=list)
    collaboration_style = Column(Text)
    
    # Recommendations
    recommended_actions = Column(JSONType, default=list)
    threat_level = Column(String(50))  # low, medium, high, critical
    priority = Column(Integer, default=0)
    
    # Status
    is_current = Column(Boolean, default=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'strategy_id': self.strategy_id,
            'competitor_name': self.competitor_name,
            'competitor_handle': self.competitor_handle,
            'competitor_url': self.competitor_url,
            'analysis_start_date': self.analysis_start_date.isoformat() if self.analysis_start_date else None,
            'analysis_end_date': self.analysis_end_date.isoformat() if self.analysis_end_date else None,
            'platforms': self.platforms,
            'top_content_types': self.top_content_types,
            'content_themes': self.content_themes,
            'posting_patterns': self.posting_patterns,
            'avg_engagement_rate': self.avg_engagement_rate,
            'avg_reach': self.avg_reach,
            'avg_likes': self.avg_likes,
            'avg_comments': self.avg_comments,
            'avg_shares': self.avg_shares,
            'top_posts': self.top_posts,
            'viral_content': self.viral_content,
            'strengths': self.strengths,
            'weaknesses': self.weaknesses,
            'opportunities': self.opportunities,
            'threats': self.threats,
            'content_gaps': self.content_gaps,
            'audience_gaps': self.audience_gaps,
            'platform_gaps': self.platform_gaps,
            'popular_hashtags': self.popular_hashtags,
            'hashtag_frequency': self.hashtag_frequency,
            'influencer_partnerships': self.influencer_partnerships,
            'collaboration_style': self.collaboration_style,
            'recommended_actions': self.recommended_actions,
            'threat_level': self.threat_level,
            'priority': self.priority,
            'is_current': self.is_current,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at
        }
