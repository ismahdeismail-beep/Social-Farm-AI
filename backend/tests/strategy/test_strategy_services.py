"""
Tests for Content Strategy Agent - Backend Services
"""

import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

from app.services.strategy.strategy_engine import (
    StrategyEngine,
    StrategyInput,
    StrategyType,
    StrategyOutput,
)
from app.services.strategy.opportunity_engine import (
    OpportunityEngine,
    OpportunityType,
    DetectedOpportunity,
)
from app.services.strategy.campaign_planner import (
    CampaignPlanner,
    CampaignInput,
    CampaignType,
    CampaignOutput,
)
from app.services.strategy.calendar_generator import (
    CalendarGenerator,
    CalendarEntry,
)
from app.services.strategy.recommendation_engine import (
    RecommendationEngine,
    ContentRecommendation,
)
from app.services.strategy.forecast_engine import (
    ForecastEngine,
    PerformanceForecast,
)


# ==================== STRATEGY ENGINE TESTS ====================


class TestStrategyEngine:
    """Tests for StrategyEngine."""

    @pytest.fixture
    def engine(self):
        """Create a fresh StrategyEngine for each test."""
        engine = StrategyEngine()
        engine._initialized = False
        return engine

    @pytest.mark.asyncio
    async def test_initialization(self, engine):
        """Test engine initialization."""
        assert not engine._initialized
        await engine.initialize()
        assert engine._initialized

    @pytest.mark.asyncio
    async def test_generate_strategy(self, engine):
        """Test strategy generation."""
        await engine.initialize()

        input_data = StrategyInput(
            brand_id="test_brand",
            project_id="test_project",
            strategy_type=StrategyType.QUARTERLY,
            start_date=datetime.now(timezone.utc),
            end_date=datetime.now(timezone.utc),
            goals=["Increase brand awareness", "Drive engagement"],
            budget_usd=10000,
            target_platforms=["instagram", "tiktok"],
            target_audiences=["farmers", "agriculture_enthusiasts"],
            industry="agriculture",
            competitors=["competitor1", "competitor2"],
        )

        output = await engine.generate_strategy(input_data)

        assert output is not None
        assert output.strategy_id is not None
        assert output.name is not None
        assert output.vision is not None
        assert output.mission is not None
        assert len(output.goals) > 0
        assert len(output.kpis) > 0
        assert len(output.content_pillars) > 0
        assert output.confidence_score > 0

    @pytest.mark.asyncio
    async def test_get_strategy(self, engine):
        """Test getting a strategy by ID."""
        await engine.initialize()

        # Generate a strategy first
        input_data = StrategyInput(
            brand_id="test_brand",
            strategy_type=StrategyType.MONTHLY,
            start_date=datetime.now(timezone.utc),
            end_date=datetime.now(timezone.utc),
            goals=["Test goal"],
        )

        output = await engine.generate_strategy(input_data)

        # Get the strategy
        strategy = engine.get_strategy(output.strategy_id)

        assert strategy is not None
        assert strategy["strategy_id"] == output.strategy_id

    @pytest.mark.asyncio
    async def test_list_strategies(self, engine):
        """Test listing all strategies."""
        await engine.initialize()

        # Generate some strategies
        for i in range(3):
            input_data = StrategyInput(
                brand_id="test_brand",
                strategy_type=StrategyType.MONTHLY,
                start_date=datetime.now(timezone.utc),
                end_date=datetime.now(timezone.utc),
                goals=[f"Goal {i}"],
            )
            await engine.generate_strategy(input_data)

        strategies = engine.list_strategies()

        assert len(strategies) == 3

    @pytest.mark.asyncio
    async def test_approve_strategy(self, engine):
        """Test approving a strategy."""
        await engine.initialize()

        # Generate a strategy
        input_data = StrategyInput(
            brand_id="test_brand",
            strategy_type=StrategyType.MONTHLY,
            start_date=datetime.now(timezone.utc),
            end_date=datetime.now(timezone.utc),
            goals=["Test goal"],
        )

        output = await engine.generate_strategy(input_data)

        # Approve the strategy
        success = await engine.approve_strategy(output.strategy_id)

        assert success is True

    @pytest.mark.asyncio
    async def test_delete_strategy(self, engine):
        """Test deleting a strategy."""
        await engine.initialize()

        # Generate a strategy
        input_data = StrategyInput(
            brand_id="test_brand",
            strategy_type=StrategyType.MONTHLY,
            start_date=datetime.now(timezone.utc),
            end_date=datetime.now(timezone.utc),
            goals=["Test goal"],
        )

        output = await engine.generate_strategy(input_data)

        # Delete the strategy
        success = engine.delete_strategy(output.strategy_id)

        assert success is True

        # Verify it's deleted
        strategy = engine.get_strategy(output.strategy_id)
        assert strategy is None


# ==================== OPPORTUNITY ENGINE TESTS ====================


class TestOpportunityEngine:
    """Tests for OpportunityEngine."""

    @pytest.fixture
    def engine(self):
        """Create a fresh OpportunityEngine for each test."""
        engine = OpportunityEngine()
        engine._initialized = False
        return engine

    @pytest.mark.asyncio
    async def test_initialization(self, engine):
        """Test engine initialization."""
        assert not engine._initialized
        await engine.initialize()
        assert engine._initialized

    @pytest.mark.asyncio
    async def test_detect_opportunities(self, engine):
        """Test opportunity detection."""
        await engine.initialize()

        opportunities = await engine.detect_opportunities(
            brand_id="test_brand",
            industry="agriculture",
            platforms=["instagram", "tiktok"],
        )

        assert len(opportunities) > 0
        assert all(isinstance(opp, DetectedOpportunity) for opp in opportunities)
        assert all(opp.title is not None for opp in opportunities)
        assert all(opp.description is not None for opp in opportunities)
        assert all(0 <= opp.priority_score <= 1 for opp in opportunities)

    @pytest.mark.asyncio
    async def test_opportunity_types(self, engine):
        """Test that different opportunity types are detected."""
        await engine.initialize()

        opportunities = await engine.detect_opportunities(
            brand_id="test_brand",
            industry="agriculture",
            platforms=["instagram", "tiktok", "youtube"],
        )

        opportunity_types = {opp.opportunity_type for opp in opportunities}

        # Should have at least some of these types
        expected_types = {
            OpportunityType.TREND,
            OpportunityType.SEASONAL,
            OpportunityType.COMPETITOR_GAP,
            OpportunityType.AUDIENCE_INSIGHT,
            OpportunityType.CONTENT_GAP,
        }

        assert len(opportunity_types.intersection(expected_types)) > 0


# ==================== CAMPAIGN PLANNER TESTS ====================


class TestCampaignPlanner:
    """Tests for CampaignPlanner."""

    @pytest.fixture
    def planner(self):
        """Create a fresh CampaignPlanner for each test."""
        planner = CampaignPlanner()
        planner._initialized = False
        return planner

    @pytest.mark.asyncio
    async def test_initialization(self, planner):
        """Test planner initialization."""
        assert not planner._initialized
        await planner.initialize()
        assert planner._initialized

    @pytest.mark.asyncio
    async def test_create_campaign(self, planner):
        """Test campaign creation."""
        await planner.initialize()

        input_data = CampaignInput(
            name="Summer Harvest Campaign",
            campaign_type=CampaignType.PRODUCT_LAUNCH,
            start_date=datetime.now(timezone.utc),
            end_date=datetime.now(timezone.utc),
            objectives=[
                {"type": "awareness", "target": 100000, "metric": "impressions"},
                {"type": "engagement", "target": 5000, "metric": "likes"},
            ],
            budget_usd=5000,
            target_audiences=["farmers", "agriculture_enthusiasts"],
            platforms=["instagram", "tiktok"],
            brand_id="test_brand",
        )

        output = await planner.create_campaign(input_data)

        assert output is not None
        assert output.campaign_id is not None
        assert output.name == "Summer Harvest Campaign"
        assert output.campaign_type == CampaignType.PRODUCT_LAUNCH
        assert len(output.objectives) == 2
        assert len(output.timeline) > 0
        assert len(output.budget_allocation) > 0

    @pytest.mark.asyncio
    async def test_list_campaigns(self, planner):
        """Test listing campaigns."""
        await planner.initialize()

        # Create some campaigns
        for i in range(3):
            input_data = CampaignInput(
                name=f"Campaign {i}",
                campaign_type=CampaignType.SEASONAL,
                start_date=datetime.now(timezone.utc),
                end_date=datetime.now(timezone.utc),
                objectives=[],
                brand_id="test_brand",
            )
            await planner.create_campaign(input_data)

        campaigns = planner.list_campaigns()

        assert len(campaigns) == 3


# ==================== CALENDAR GENERATOR TESTS ====================


class TestCalendarGenerator:
    """Tests for CalendarGenerator."""

    @pytest.fixture
    def generator(self):
        """Create a fresh CalendarGenerator for each test."""
        generator = CalendarGenerator()
        generator._initialized = False
        return generator

    @pytest.mark.asyncio
    async def test_initialization(self, generator):
        """Test generator initialization."""
        assert not generator._initialized
        await generator.initialize()
        assert generator._initialized

    @pytest.mark.asyncio
    async def test_generate_calendar(self, generator):
        """Test calendar generation."""
        await generator.initialize()

        start_date = datetime(2026, 7, 1, tzinfo=timezone.utc)
        end_date = datetime(2026, 7, 31, tzinfo=timezone.utc)

        themes = [
            {"name": "Sustainability", "keywords": ["eco", "green", "organic"]},
            {"name": "Harvest", "keywords": ["harvest", "crop", "yield"]},
        ]

        entries = await generator.generate_calendar(
            strategy_id="test_strategy",
            start_date=start_date,
            end_date=end_date,
            platforms=["instagram", "tiktok"],
            content_mix={"short-form-video": 40, "images": 30, "carousels": 30},
            themes=themes,
        )

        assert len(entries) > 0
        assert all(isinstance(entry, CalendarEntry) for entry in entries)
        assert all(entry.date is not None for entry in entries)
        assert all(entry.platform is not None for entry in entries)

    @pytest.mark.asyncio
    async def test_get_calendar(self, generator):
        """Test getting a calendar."""
        await generator.initialize()

        # Generate a calendar first
        start_date = datetime(2026, 7, 1, tzinfo=timezone.utc)
        end_date = datetime(2026, 7, 31, tzinfo=timezone.utc)

        await generator.generate_calendar(
            strategy_id="test_strategy",
            start_date=start_date,
            end_date=end_date,
            platforms=["instagram"],
            content_mix={"images": 100},
            themes=[{"name": "General", "keywords": ["content"]}],
        )

        # Get the calendar
        entries = generator.get_calendar("test_strategy")

        assert len(entries) > 0


# ==================== RECOMMENDATION ENGINE TESTS ====================


class TestRecommendationEngine:
    """Tests for RecommendationEngine."""

    @pytest.fixture
    def engine(self):
        """Create a fresh RecommendationEngine for each test."""
        engine = RecommendationEngine()
        engine._initialized = False
        return engine

    @pytest.mark.asyncio
    async def test_initialization(self, engine):
        """Test engine initialization."""
        assert not engine._initialized
        await engine.initialize()
        assert engine._initialized

    @pytest.mark.asyncio
    async def test_generate_recommendations(self, engine):
        """Test recommendation generation."""
        await engine.initialize()

        recommendations = await engine.generate_recommendations(
            brand_id="test_brand",
            context={
                "industry": "agriculture",
                "platforms": ["instagram", "tiktok"],
                "goals": ["increase engagement"],
            },
            count=5,
        )

        assert len(recommendations) > 0
        assert all(isinstance(rec, ContentRecommendation) for rec in recommendations)
        assert all(rec.title is not None for rec in recommendations)
        assert all(rec.content_idea is not None for rec in recommendations)
        assert all(rec.hook is not None for rec in recommendations)
        assert all(0 <= rec.relevance_score <= 1 for rec in recommendations)


# ==================== FORECAST ENGINE TESTS ====================


class TestForecastEngine:
    """Tests for ForecastEngine."""

    @pytest.fixture
    def engine(self):
        """Create a fresh ForecastEngine for each test."""
        engine = ForecastEngine()
        engine._initialized = False
        return engine

    @pytest.mark.asyncio
    async def test_initialization(self, engine):
        """Test engine initialization."""
        assert not engine._initialized
        await engine.initialize()
        assert engine._initialized

    @pytest.mark.asyncio
    async def test_generate_forecast(self, engine):
        """Test single forecast generation."""
        await engine.initialize()

        forecast = await engine.generate_forecast(
            metric_name="followers",
            current_value=10000,
            timeframe_months=3,
            growth_rate=0.05,
        )

        assert forecast is not None
        assert forecast.name == "followers"
        assert forecast.predicted_value > 0
        assert 0 <= forecast.confidence_level <= 1
        assert forecast.best_case >= forecast.predicted_value
        assert forecast.worst_case <= forecast.predicted_value

    @pytest.mark.asyncio
    async def test_generate_multi_metric_forecast(self, engine):
        """Test multi-metric forecast generation."""
        await engine.initialize()

        current_metrics = {
            "followers": 10000,
            "engagement_rate": 0.04,
            "reach": 50000,
        }

        forecasts = await engine.generate_multi_metric_forecast(
            strategy_id="test_strategy",
            timeframe_months=3,
            current_metrics=current_metrics,
        )

        assert len(forecasts) == 3
        assert all(isinstance(f, PerformanceForecast) for f in forecasts)
        assert all(f.predicted_value > 0 for f in forecasts)


# ==================== INTEGRATION TESTS ====================


class TestStrategyIntegration:
    """Integration tests for the Content Strategy Agent."""

    @pytest.mark.asyncio
    async def test_full_workflow(self):
        """Test the full strategy workflow."""
        # Initialize all engines
        strategy_engine = StrategyEngine()
        strategy_engine._initialized = False
        await strategy_engine.initialize()

        opportunity_engine = OpportunityEngine()
        opportunity_engine._initialized = False
        await opportunity_engine.initialize()

        campaign_planner = CampaignPlanner()
        campaign_planner._initialized = False
        await campaign_planner.initialize()

        calendar_generator = CalendarGenerator()
        calendar_generator._initialized = False
        await calendar_generator.initialize()

        # 1. Detect opportunities
        opportunities = await opportunity_engine.detect_opportunities(
            brand_id="test_brand",
            industry="agriculture",
            platforms=["instagram", "tiktok"],
        )
        assert len(opportunities) > 0

        # 2. Generate strategy
        strategy_input = StrategyInput(
            brand_id="test_brand",
            strategy_type=StrategyType.QUARTERLY,
            start_date=datetime.now(timezone.utc),
            end_date=datetime.now(timezone.utc),
            goals=["Increase brand awareness", "Drive engagement"],
            budget_usd=10000,
            target_platforms=["instagram", "tiktok"],
            target_audiences=["farmers"],
            industry="agriculture",
        )

        strategy_output = await strategy_engine.generate_strategy(strategy_input)
        assert strategy_output is not None

        # 3. Create campaign based on strategy
        campaign_input = CampaignInput(
            name="Q3 Awareness Campaign",
            campaign_type=CampaignType.BRAND_AWARENESS,
            start_date=strategy_input.start_date,
            end_date=strategy_input.end_date,
            objectives=[
                {"type": "awareness", "target": 100000, "metric": "impressions"}
            ],
            budget_usd=5000,
            target_audiences=["farmers"],
            platforms=["instagram", "tiktok"],
            brand_id="test_brand",
        )

        campaign_output = await campaign_planner.create_campaign(campaign_input)
        assert campaign_output is not None

        # 4. Generate calendar
        calendar_entries = await calendar_generator.generate_calendar(
            strategy_id=strategy_output.strategy_id,
            start_date=strategy_input.start_date,
            end_date=strategy_input.end_date,
            platforms=["instagram", "tiktok"],
            content_mix={"short-form-video": 40, "images": 30, "carousels": 30},
            themes=strategy_output.themes,
        )
        assert len(calendar_entries) > 0

        # Verify all pieces connect
        assert strategy_output.strategy_id is not None
        assert campaign_output.campaign_id is not None
        assert len(calendar_entries) > 0
