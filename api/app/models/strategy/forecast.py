"""
Content Forecast Models

Performance forecasting and predictions.
"""

from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Integer, Float, JSON as JSONType
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

from app.models import Base, TimestampMixin, SoftDeleteMixin


class ContentForecast(Base, TimestampMixin, SoftDeleteMixin):
    """
    Performance forecast for content strategy.
    """
    __tablename__ = 'content_forecasts'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_id = Column(UUID(as_uuid=True), ForeignKey('content_strategies.id'), nullable=False)
    
    # Forecast definition
    name = Column(String(255), nullable=False)
    description = Column(Text)
    forecast_type = Column(String(100), nullable=False)  # growth, engagement, reach, revenue
    
    # Timeframe
    forecast_period = Column(String(50))  # weekly, monthly, quarterly, annual
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    
    # Predictions
    predicted_value = Column(Float, nullable=False)
    confidence_interval = Column(JSONType)  # {low: x, high: y}
    confidence_level = Column(Float, default=0.8)
    
    # Factors
    growth_factors = Column(JSONType, default=list)
    risk_factors = Column(JSONType, default=list)
    assumptions = Column(JSONType, default=list)
    
    # Scenarios
    best_case = Column(Float)
    worst_case = Column(Float)
    most_likely = Column(Float)
    
    # Model
    model_used = Column(String(100))
    model_version = Column(String(50))
    training_data_period = Column(JSONType)
    
    # Actual (for comparison)
    actual_value = Column(Float)
    variance = Column(Float)
    
    # Status
    status = Column(String(50), default='draft')  # draft, active, validated, archived
    
    # Relationships
    strategy = relationship('ContentStrategy', back_populates='forecasts')
    
    def to_dict(self):
        return {
            'id': self.id,
            'strategy_id': self.strategy_id,
            'name': self.name,
            'description': self.description,
            'forecast_type': self.forecast_type,
            'forecast_period': self.forecast_period,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'predicted_value': self.predicted_value,
            'confidence_interval': self.confidence_interval,
            'confidence_level': self.confidence_level,
            'growth_factors': self.growth_factors,
            'risk_factors': self.risk_factors,
            'assumptions': self.assumptions,
            'best_case': self.best_case,
            'worst_case': self.worst_case,
            'most_likely': self.most_likely,
            'model_used': self.model_used,
            'model_version': self.model_version,
            'training_data_period': self.training_data_period,
            'actual_value': self.actual_value,
            'variance': self.variance,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at
        }
