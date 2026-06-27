"""
Content Risk Models

Risk assessment for content strategies.
"""

from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Integer, Float, JSON as JSONType
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

from app.models import Base, TimestampMixin, SoftDeleteMixin


class ContentRisk(Base, TimestampMixin, SoftDeleteMixin):
    """
    Identified risks in content strategy.
    """
    __tablename__ = 'content_risks'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_id = Column(UUID(as_uuid=True), ForeignKey('content_strategies.id'), nullable=False)
    
    # Risk definition
    title = Column(String(255), nullable=False)
    description = Column(Text)
    risk_type = Column(String(100), nullable=False)  # brand, legal, platform, audience, competition, technical
    
    # Severity
    likelihood = Column(Float, default=0.5)  # 0.0 to 1.0
    impact = Column(Float, default=0.5)  # 0.0 to 1.0
    risk_score = Column(Float, default=0.25)  # likelihood * impact
    
    # Category
    category = Column(String(100))  # reputation, compliance, algorithm, market, etc.
    severity = Column(String(50))  # low, medium, high, critical
    
    # Mitigation
    mitigation_strategies = Column(JSONType, default=list)
    preventive_actions = Column(JSONType, default=list)
    contingency_plan = Column(Text)
    
    # Monitoring
    early_warning_signs = Column(JSONType, default=list)
    monitoring_frequency = Column(String(50))  # daily, weekly, monthly
    
    # Status
    status = Column(String(50), default='identified')  # identified, monitoring, mitigated, realized, closed
    owner = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    last_reviewed_at = Column(DateTime(timezone=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'strategy_id': self.strategy_id,
            'title': self.title,
            'description': self.description,
            'risk_type': self.risk_type,
            'likelihood': self.likelihood,
            'impact': self.impact,
            'risk_score': self.risk_score,
            'category': self.category,
            'severity': self.severity,
            'mitigation_strategies': self.mitigation_strategies,
            'preventive_actions': self.preventive_actions,
            'contingency_plan': self.contingency_plan,
            'early_warning_signs': self.early_warning_signs,
            'monitoring_frequency': self.monitoring_frequency,
            'status': self.status,
            'owner': self.owner,
            'last_reviewed_at': self.last_reviewed_at.isoformat() if self.last_reviewed_at else None,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at
        }
