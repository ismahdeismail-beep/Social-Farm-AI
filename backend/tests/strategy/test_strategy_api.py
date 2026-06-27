"""
Tests for Content Strategy API Endpoints
"""

import pytest
from datetime import datetime, timezone
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from app.main import app


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


@pytest.fixture
def mock_token():
    """Mock authentication token."""
    return "test_token_123"


@pytest.fixture
def headers(mock_token):
    """Create authentication headers."""
    return {"Authorization": f"Bearer {mock_token}"}


# ==================== STRATEGY ENDPOINTS ====================


class TestStrategyEndpoints:
    """Tests for strategy endpoints."""

    @pytest.mark.asyncio
    async def test_generate_strategy(self, client, headers):
        """Test generating a strategy."""
        with patch("app.api.strategy.verify_token", return_value="test_user"):
            response = client.post(
                "/api/strategy/generate",
                json={
                    "brand_id": "test_brand",
                    "strategy_type": "quarterly",
                    "start_date": datetime.now(timezone.utc).isoformat(),
                    "end_date": datetime.now(timezone.utc).isoformat(),
                    "goals": ["Increase brand awareness"],
                    "budget_usd": 10000,
                    "target_platforms": ["instagram", "tiktok"],
                    "industry": "agriculture",
                },
                headers=headers,
            )

            assert response.status_code == 200
            data = response.json()
            assert "strategy_id" in data
            assert "name" in data
            assert "vision" in data
            assert "goals" in data
            assert "kpis" in data
            assert "content_pillars" in data

    @pytest.mark.asyncio
    async def test_list_strategies(self, client, headers):
        """Test listing strategies."""
        with patch("app.api.strategy.verify_token", return_value="test_user"):
            response = client.get("/api/strategy/", headers=headers)

            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_strategy(self, client, headers):
        """Test getting a strategy by ID."""
        with patch("app.api.strategy.verify_token", return_value="test_user"):
            # First generate a strategy
            generate_response = client.post(
                "/api/strategy/generate",
                json={
                    "brand_id": "test_brand",
                    "strategy_type": "monthly",
                    "start_date": datetime.now(timezone.utc).isoformat(),
                    "end_date": datetime.now(timezone.utc).isoformat(),
                    "goals": ["Test goal"],
                },
                headers=headers,
            )

            strategy_id = generate_response.json()["strategy_id"]

            # Then get it
            response = client.get(f"/api/strategy/{strategy_id}", headers=headers)

            assert response.status_code == 200
            data = response.json()
            assert data["strategy_id"] == strategy_id

    @pytest.mark.asyncio
    async def test_get_calendar(self, client, headers):
        """Test getting the calendar."""
        with patch("app.api.strategy.verify_token", return_value="test_user"):
            response = client.get("/api/strategy/calendar", headers=headers)

            assert response.status_code == 200
            data = response.json()
            assert "entries" in data
            assert "total_count" in data
            assert "date_range" in data

    @pytest.mark.asyncio
    async def test_get_opportunities(self, client, headers):
        """Test getting opportunities."""
        with patch("app.api.strategy.verify_token", return_value="test_user"):
            response = client.get(
                "/api/strategy/opportunities?brand_id=test_brand&industry=agriculture",
                headers=headers,
            )

            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            assert len(data) > 0
            assert "id" in data[0]
            assert "title" in data[0]
            assert "priority_score" in data[0]

    @pytest.mark.asyncio
    async def test_get_recommendations(self, client, headers):
        """Test getting recommendations."""
        with patch("app.api.strategy.verify_token", return_value="test_user"):
            response = client.get(
                "/api/strategy/recommendations?brand_id=test_brand&count=5",
                headers=headers,
            )

            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            assert len(data) > 0
            assert "id" in data[0]
            assert "title" in data[0]
            assert "content_idea" in data[0]

    @pytest.mark.asyncio
    async def test_get_forecasts(self, client, headers):
        """Test getting forecasts."""
        with patch("app.api.strategy.verify_token", return_value="test_user"):
            # First generate a strategy
            generate_response = client.post(
                "/api/strategy/generate",
                json={
                    "brand_id": "test_brand",
                    "strategy_type": "monthly",
                    "start_date": datetime.now(timezone.utc).isoformat(),
                    "end_date": datetime.now(timezone.utc).isoformat(),
                    "goals": ["Test goal"],
                },
                headers=headers,
            )

            strategy_id = generate_response.json()["strategy_id"]

            # Then get forecasts
            response = client.get(
                f"/api/strategy/forecasts?strategy_id={strategy_id}&timeframe_months=3",
                headers=headers,
            )

            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            assert len(data) > 0
            assert "id" in data[0]
            assert "predicted_value" in data[0]

    @pytest.mark.asyncio
    async def test_approve_strategy(self, client, headers):
        """Test approving a strategy."""
        with patch("app.api.strategy.verify_token", return_value="test_user"):
            # First generate a strategy
            generate_response = client.post(
                "/api/strategy/generate",
                json={
                    "brand_id": "test_brand",
                    "strategy_type": "monthly",
                    "start_date": datetime.now(timezone.utc).isoformat(),
                    "end_date": datetime.now(timezone.utc).isoformat(),
                    "goals": ["Test goal"],
                },
                headers=headers,
            )

            strategy_id = generate_response.json()["strategy_id"]

            # Then approve it
            response = client.post(
                f"/api/strategy/approve?strategy_id={strategy_id}",
                json={"approved": True, "notes": "Looks good"},
                headers=headers,
            )

            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "approved"


# ==================== CAMPAIGN ENDPOINTS ====================


class TestCampaignEndpoints:
    """Tests for campaign endpoints."""

    @pytest.mark.asyncio
    async def test_create_campaign(self, client, headers):
        """Test creating a campaign."""
        with patch("app.api.strategy.verify_token", return_value="test_user"):
            response = client.post(
                "/api/strategy/campaigns",
                json={
                    "name": "Summer Campaign",
                    "campaign_type": "product_launch",
                    "start_date": datetime.now(timezone.utc).isoformat(),
                    "end_date": datetime.now(timezone.utc).isoformat(),
                    "objectives": [
                        {"type": "awareness", "target": 100000, "metric": "impressions"}
                    ],
                    "budget_usd": 5000,
                    "target_audiences": ["farmers"],
                    "platforms": ["instagram", "tiktok"],
                },
                headers=headers,
            )

            assert response.status_code == 200
            data = response.json()
            assert "campaign_id" in data
            assert data["name"] == "Summer Campaign"
            assert "timeline" in data
            assert "budget_allocation" in data

    @pytest.mark.asyncio
    async def test_list_campaigns(self, client, headers):
        """Test listing campaigns."""
        with patch("app.api.strategy.verify_token", return_value="test_user"):
            response = client.get("/api/strategy/campaigns", headers=headers)

            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)


# ==================== ERROR HANDLING ====================


class TestErrorHandling:
    """Tests for error handling."""

    @pytest.mark.asyncio
    async def test_get_nonexistent_strategy(self, client, headers):
        """Test getting a strategy that doesn't exist."""
        with patch("app.api.strategy.verify_token", return_value="test_user"):
            response = client.get(
                "/api/strategy/nonexistent_id", headers=headers
            )

            assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_unauthorized_access(self, client):
        """Test unauthorized access."""
        response = client.get("/api/strategy/")

        assert response.status_code == 401 or response.status_code == 403
