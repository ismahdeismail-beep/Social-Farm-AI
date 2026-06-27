"""
Content Strategy API Endpoints

REST API for the Content Strategy Agent.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import uuid

from app.core.security import verify_token

router = APIRouter(prefix="/strategy", tags=["Content Strategy"])


# ==================== REQUEST MODELS ====================

class StrategyGenerateRequest(BaseModel):
    """Request to generate a new strategy."""
    brand_id: str
    project_id: Optional[str] = None
    strategy_type: str = Field(..., description="quarterly, monthly, campaign, always_on")
    start_date: datetime
    end_date: datetime
    goals: List[str] = Field(default_factory=list)
    budget_usd: float = 0.0
    target_platforms: List[str] = Field(default_factory=list)
    target_audiences: List[str] = Field(default_factory=list)
    industry: Optional[str] = None
    competitors: Optional[List[str]] = None


class CampaignCreateRequest(BaseModel):
    """Request to create a campaign."""
    name: str
    campaign_type: str
    start_date: datetime
    end_date: datetime
    objectives: List[Dict[str, Any]] = Field(default_factory=list)
    budget_usd: float = 0.0
    target_audiences: List[str] = Field(default_factory=list)
    platforms: List[str] = Field(default_factory=list)


class OpportunityUpdateRequest(BaseModel):
    """Request to update opportunity status."""
    status: str
    review_notes: Optional[str] = None


class StrategyApprovalRequest(BaseModel):
    """Request to approve a strategy."""
    approved: bool
    notes: Optional[str] = None


# ==================== RESPONSE MODELS ====================

class StrategyResponse(BaseModel):
    """Strategy response."""
    strategy_id: str
    name: str
    vision: str
    mission: str
    goals: List[Dict[str, Any]]
    kpis: List[Dict[str, Any]]
    content_pillars: List[Dict[str, Any]]
    content_mix: Dict[str, float]
    platform_strategies: List[Dict[str, Any]]
    audience_segments: List[Dict[str, Any]]
    themes: List[Dict[str, Any]]
    recommendations: List[Dict[str, Any]]
    confidence_score: float


class CampaignResponse(BaseModel):
    """Campaign response."""
    campaign_id: str
    name: str
    campaign_type: str
    objectives: List[Dict[str, Any]]
    content_plan: Dict[str, Any]
    platform_strategy: Dict[str, Any]
    timeline: List[Dict[str, Any]]
    budget_allocation: Dict[str, float]
    kpis: List[Dict[str, Any]]


class OpportunityResponse(BaseModel):
    """Opportunity response."""
    id: str
    title: str
    description: str
    opportunity_type: str
    priority_score: float
    suggested_formats: List[str]
    suggested_platforms: List[str]


class CalendarResponse(BaseModel):
    """Calendar response."""
    entries: List[Dict[str, Any]]
    total_count: int
    date_range: Dict[str, str]


class RecommendationResponse(BaseModel):
    """Recommendation response."""
    id: str
    title: str
    description: str
    recommendation_type: str
    content_idea: str
    hook: str
    target_platforms: List[str]
    relevance_score: float


class ForecastResponse(BaseModel):
    """Forecast response."""
    id: str
    name: str
    forecast_type: str
    predicted_value: float
    confidence_level: float
    best_case: float
    worst_case: float


# ==================== ENDPOINTS ====================

@router.post("/generate", response_model=StrategyResponse)
async def generate_strategy(
    request: StrategyGenerateRequest,
    current_user_id: str = Depends(verify_token)
):
    """
    Generate a comprehensive content strategy.
    
    This is the main endpoint for strategy generation.
    It analyzes brand, audience, competitors, and trends to create
    a complete content strategy with pillars, themes, and recommendations.
    """
    from app.services.strategy.strategy_engine import strategy_engine, StrategyInput, StrategyType
    
    await strategy_engine.initialize()
    
    input_data = StrategyInput(
        brand_id=request.brand_id,
        project_id=request.project_id,
        strategy_type=StrategyType(request.strategy_type),
        start_date=request.start_date,
        end_date=request.end_date,
        goals=request.goals,
        budget_usd=request.budget_usd,
        target_platforms=request.target_platforms,
        target_audiences=request.target_audiences,
        industry=request.industry,
        competitors=request.competitors
    )
    
    output = await strategy_engine.generate_strategy(input_data)
    
    return StrategyResponse(
        strategy_id=output.strategy_id,
        name=output.name,
        vision=output.vision,
        mission=output.mission,
        goals=output.goals,
        kpis=output.kpis,
        content_pillars=output.content_pillars,
        content_mix=output.content_mix,
        platform_strategies=output.platform_strategies,
        audience_segments=output.audience_segments,
        themes=output.themes,
        recommendations=output.recommendations,
        confidence_score=output.confidence_score
    )


@router.get("/", response_model=List[Dict[str, Any]])
async def list_strategies(
    current_user_id: str = Depends(verify_token)
):
    """
    List all content strategies.
    """
    from app.services.strategy.strategy_engine import strategy_engine
    
    await strategy_engine.initialize()
    
    return strategy_engine.list_strategies()


@router.get("/{strategy_id}", response_model=StrategyResponse)
async def get_strategy(
    strategy_id: str,
    current_user_id: str = Depends(verify_token)
):
    """
    Get a specific strategy by ID.
    """
    from app.services.strategy.strategy_engine import strategy_engine
    
    await strategy_engine.initialize()
    
    strategy = strategy_engine.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Strategy not found"
        )
    
    return strategy


@router.get("/calendar", response_model=CalendarResponse)
async def get_calendar(
    strategy_id: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user_id: str = Depends(verify_token)
):
    """
    Get content calendar.
    """
    from app.services.strategy.calendar_generator import calendar_generator
    
    await calendar_generator.initialize()
    
    # Default to current month if no dates provided
    if not start_date:
        start_date = datetime.now(timezone.utc).replace(day=1)
    if not end_date:
        end_date = datetime.now(timezone.utc).replace(day=28)
    
    # Generate or retrieve calendar
    calendar_id = strategy_id or "default"
    entries = calendar_generator.get_calendar(calendar_id)
    
    if not entries:
        # Generate a sample calendar
        entries = await calendar_generator.generate_calendar(
            strategy_id=calendar_id,
            start_date=start_date,
            end_date=end_date,
            platforms=["instagram", "tiktok", "linkedin"],
            content_mix={"short-form-video": 40, "images": 30, "carousels": 30},
            themes=[{"name": "General", "keywords": ["content"]}]
        )
    
    return CalendarResponse(
        entries=[e.__dict__ for e in entries] if entries else [],
        total_count=len(entries) if entries else 0,
        date_range={
            "start": start_date.isoformat(),
            "end": end_date.isoformat()
        }
    )


@router.get("/opportunities", response_model=List[OpportunityResponse])
async def get_opportunities(
    brand_id: str,
    industry: str = "general",
    current_user_id: str = Depends(verify_token)
):
    """
    Get content opportunities.
    """
    from app.services.strategy.opportunity_engine import opportunity_engine
    
    await opportunity_engine.initialize()
    
    opportunities = await opportunity_engine.detect_opportunities(
        brand_id=brand_id,
        industry=industry,
        platforms=["instagram", "tiktok", "youtube"]
    )
    
    return [
        OpportunityResponse(
            id=opp.id,
            title=opp.title,
            description=opp.description,
            opportunity_type=opp.opportunity_type.value,
            priority_score=opp.priority_score,
            suggested_formats=opp.suggested_formats,
            suggested_platforms=opp.suggested_platforms
        )
        for opp in opportunities
    ]


@router.get("/themes", response_model=List[Dict[str, Any]])
async def get_themes(
    strategy_id: str,
    current_user_id: str = Depends(verify_token)
):
    """
    Get content themes for a strategy.
    """
    from app.services.strategy.strategy_engine import strategy_engine
    
    await strategy_engine.initialize()
    
    strategy = strategy_engine.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Strategy not found"
        )
    
    return strategy.get("themes", [])


@router.get("/campaigns", response_model=List[Dict[str, Any]])
async def list_campaigns(
    current_user_id: str = Depends(verify_token)
):
    """
    List all campaigns.
    """
    from app.services.strategy.campaign_planner import campaign_planner
    
    await campaign_planner.initialize()
    
    return campaign_planner.list_campaigns()


@router.post("/campaigns", response_model=CampaignResponse)
async def create_campaign(
    request: CampaignCreateRequest,
    current_user_id: str = Depends(verify_token)
):
    """
    Create a new campaign.
    """
    from app.services.strategy.campaign_planner import campaign_planner, CampaignInput, CampaignType
    
    await campaign_planner.initialize()
    
    input_data = CampaignInput(
        name=request.name,
        campaign_type=CampaignType(request.campaign_type),
        start_date=request.start_date,
        end_date=request.end_date,
        objectives=request.objectives,
        budget_usd=request.budget_usd,
        target_audiences=request.target_audiences,
        platforms=request.platforms,
        brand_id="current_brand"  # TODO: Get from context
    )
    
    output = await campaign_planner.create_campaign(input_data)
    
    return CampaignResponse(
        campaign_id=output.campaign_id,
        name=output.name,
        campaign_type=output.campaign_type.value,
        objectives=output.objectives,
        content_plan=output.content_plan,
        platform_strategy=output.platform_strategy,
        timeline=output.timeline,
        budget_allocation=output.budget_allocation,
        kpis=output.kpis
    )


@router.get("/recommendations", response_model=List[RecommendationResponse])
async def get_recommendations(
    brand_id: str,
    count: int = 10,
    current_user_id: str = Depends(verify_token)
):
    """
    Get AI-powered content recommendations.
    """
    from app.services.strategy.recommendation_engine import recommendation_engine
    
    await recommendation_engine.initialize()
    
    recommendations = await recommendation_engine.generate_recommendations(
        brand_id=brand_id,
        context={},
        count=count
    )
    
    return [
        RecommendationResponse(
            id=rec.id,
            title=rec.title,
            description=rec.description,
            recommendation_type=rec.recommendation_type,
            content_idea=rec.content_idea,
            hook=rec.hook,
            target_platforms=rec.target_platforms,
            relevance_score=rec.relevance_score
        )
        for rec in recommendations
    ]


@router.get("/forecasts", response_model=List[ForecastResponse])
async def get_forecasts(
    strategy_id: str,
    timeframe_months: int = 3,
    current_user_id: str = Depends(verify_token)
):
    """
    Get performance forecasts.
    """
    from app.services.strategy.forecast_engine import forecast_engine
    
    await forecast_engine.initialize()
    
    forecasts = await forecast_engine.generate_multi_metric_forecast(
        strategy_id=strategy_id,
        timeframe_months=timeframe_months,
        current_metrics={
            "followers": 10000,
            "engagement_rate": 0.04,
            "reach": 50000
        }
    )
    
    return [
        ForecastResponse(
            id=f.id,
            name=f.name,
            forecast_type=f.forecast_type,
            predicted_value=f.predicted_value,
            confidence_level=f.confidence_level,
            best_case=f.best_case,
            worst_case=f.worst_case
        )
        for f in forecasts
    ]


@router.post("/approve")
async def approve_strategy(
    request: StrategyApprovalRequest,
    strategy_id: str,
    current_user_id: str = Depends(verify_token)
):
    """
    Approve or reject a strategy.
    """
    from app.services.strategy.strategy_engine import strategy_engine
    
    await strategy_engine.initialize()
    
    if request.approved:
        success = await strategy_engine.approve_strategy(strategy_id)
    else:
        # TODO: Handle rejection
        success = True
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Strategy not found"
        )
    
    return {"status": "approved" if request.approved else "rejected"}


@router.post("/regenerate")
async def regenerate_strategy(
    strategy_id: str,
    current_user_id: str = Depends(verify_token)
):
    """
    Regenerate a strategy with fresh analysis.
    """
    from app.services.strategy.strategy_engine import strategy_engine
    
    await strategy_engine.initialize()
    
    strategy = strategy_engine.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Strategy not found"
        )
    
    # TODO: Regenerate with updated context
    return {"status": "regenerating", "strategy_id": strategy_id}
