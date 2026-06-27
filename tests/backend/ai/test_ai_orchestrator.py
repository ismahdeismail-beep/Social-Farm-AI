"""
Tests for AI Orchestrator Services

Comprehensive tests for the Master AI Orchestrator system.
"""

import pytest
import asyncio
from datetime import datetime, timezone


# ==================== GATEWAY TESTS ====================

class TestAIGateway:
    """Tests for AI Gateway service."""
    
    @pytest.mark.asyncio
    async def test_gateway_initialization(self):
        """Test gateway initialization."""
        from app.services.ai.gateway import AIGateway
        
        gateway = AIGateway()
        await gateway.initialize()
        
        assert gateway._initialized
        assert len(gateway.providers) > 0
    
    @pytest.mark.asyncio
    async def test_circuit_breaker(self):
        """Test circuit breaker pattern."""
        from app.services.ai.gateway import CircuitBreaker
        
        breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=1)
        
        # Initially closed
        assert breaker.state == "closed"
        assert breaker.can_execute()
        
        # Record failures
        for _ in range(3):
            breaker.record_failure()
        
        # Should be open now
        assert breaker.state == "open"
        assert not breaker.can_execute()
    
    @pytest.mark.asyncio
    async def test_provider_status(self):
        """Test provider status retrieval."""
        from app.services.ai.gateway import AIGateway
        
        gateway = AIGateway()
        await gateway.initialize()
        
        status = gateway.get_provider_status()
        assert len(status) > 0
        assert "openai" in status


# ==================== ROUTER TESTS ====================

class TestModelRouter:
    """Tests for Model Router service."""
    
    @pytest.mark.asyncio
    async def test_router_initialization(self):
        """Test router initialization."""
        from app.services.ai.router import ModelRouter
        
        router = ModelRouter()
        await router.initialize()
        
        assert router._initialized
        assert len(router.models) > 0
    
    @pytest.mark.asyncio
    async def test_model_routing(self):
        """Test model selection."""
        from app.services.ai.router import ModelRouter, RoutingStrategy
        
        router = ModelRouter()
        await router.initialize()
        
        model = await router.route(
            task_type="chat",
            strategy=RoutingStrategy.BALANCED
        )
        
        assert model is not None
        assert model.provider in ["openai", "anthropic", "google"]
    
    @pytest.mark.asyncio
    async def test_cost_optimized_routing(self):
        """Test cost-optimized routing."""
        from app.services.ai.router import ModelRouter, RoutingStrategy
        
        router = ModelRouter()
        await router.initialize()
        
        model = await router.route(
            task_type="chat",
            strategy=RoutingStrategy.COST_OPTIMIZED,
            budget_limit=0.001
        )
        
        assert model is not None
        assert model.cost_per_1k_tokens <= 0.001


# ==================== MEMORY TESTS ====================

class TestMemoryEngine:
    """Tests for Memory Engine service."""
    
    @pytest.mark.asyncio
    async def test_memory_initialization(self):
        """Test memory engine initialization."""
        from app.services.ai.memory import MemoryEngine
        
        engine = MemoryEngine()
        await engine.initialize()
        
        assert engine._initialized
    
    @pytest.mark.asyncio
    async def test_memory_store_and_retrieve(self):
        """Test storing and retrieving memories."""
        from app.services.ai.memory import MemoryEngine, MemoryType, MemoryQuery
        
        engine = MemoryEngine()
        await engine.initialize()
        
        # Store memory
        memory_id = await engine.store(
            memory_type=MemoryType.CONVERSATION,
            content="Test conversation content",
            tags=["test"],
            importance=0.8
        )
        
        assert memory_id is not None
        
        # Retrieve memory
        query = MemoryQuery(
            query="Test",
            memory_types=[MemoryType.CONVERSATION]
        )
        results = await engine.retrieve(query)
        
        assert len(results) > 0
    
    @pytest.mark.asyncio
    async def test_memory_stats(self):
        """Test memory statistics."""
        from app.services.ai.memory import MemoryEngine
        
        engine = MemoryEngine()
        await engine.initialize()
        
        stats = engine.get_stats()
        assert "total_memories" in stats
        assert "by_type" in stats


# ==================== PROMPT LIBRARY TESTS ====================

class TestPromptLibrary:
    """Tests for Prompt Library service."""
    
    @pytest.mark.asyncio
    async def test_library_initialization(self):
        """Test prompt library initialization."""
        from app.services.ai.prompts import PromptLibrary
        
        library = PromptLibrary()
        await library.initialize()
        
        assert library._initialized
        assert len(library.templates) > 0
    
    @pytest.mark.asyncio
    async def test_template_rendering(self):
        """Test prompt template rendering."""
        from app.services.ai.prompts import PromptLibrary
        
        library = PromptLibrary()
        await library.initialize()
        
        # Get a template with variables
        template = await library.get_template(name="content_creator")
        assert template is not None
        
        # Render template
        result = await library.render(
            template_id=template.id,
            variables={
                "brand_name": "Test Brand",
                "brand_voice": "Professional",
                "target_audience": "Young adults",
                "platform": "Instagram"
            }
        )
        
        assert "prompt" in result
        assert "Test Brand" in result["prompt"]
    
    @pytest.mark.asyncio
    async def test_library_stats(self):
        """Test library statistics."""
        from app.services.ai.prompts import PromptLibrary
        
        library = PromptLibrary()
        await library.initialize()
        
        stats = library.get_stats()
        assert "total_templates" in stats
        assert "active_templates" in stats


# ==================== AGENT REGISTRY TESTS ====================

class TestAgentRegistry:
    """Tests for Agent Registry service."""
    
    @pytest.mark.asyncio
    async def test_registry_initialization(self):
        """Test registry initialization."""
        from app.services.ai.registry import AgentRegistry
        
        registry = AgentRegistry()
        await registry.initialize()
        
        assert registry._initialized
        assert len(registry.agents) > 0
    
    @pytest.mark.asyncio
    async def test_agent_selection(self):
        """Test agent selection for task type."""
        from app.services.ai.registry import AgentRegistry
        
        registry = AgentRegistry()
        await registry.initialize()
        
        agent = await registry.select_agent(task_type="trend_analysis")
        assert agent is not None
        assert "trend_analysis" in agent.supported_tasks
    
    @pytest.mark.asyncio
    async def test_registry_stats(self):
        """Test registry statistics."""
        from app.services.ai.registry import AgentRegistry
        
        registry = AgentRegistry()
        await registry.initialize()
        
        stats = registry.get_registry_stats()
        assert "total_agents" in stats
        assert "active_agents" in stats


# ==================== WORKFLOW ENGINE TESTS ====================

class TestWorkflowEngine:
    """Tests for Workflow Engine service."""
    
    @pytest.mark.asyncio
    async def test_engine_initialization(self):
        """Test workflow engine initialization."""
        from app.services.ai.workflow import WorkflowEngine
        
        engine = WorkflowEngine()
        await engine.initialize()
        
        assert engine._initialized
    
    @pytest.mark.asyncio
    async def test_workflow_creation(self):
        """Test workflow creation."""
        from app.services.ai.workflow import WorkflowEngine
        
        engine = WorkflowEngine()
        await engine.initialize()
        
        workflow_id = await engine.create_workflow(
            name="Test Workflow",
            description="A test workflow",
            workflow_type="test",
            tasks=[
                {
                    "id": "task1",
                    "name": "First Task",
                    "task_type": "research"
                },
                {
                    "id": "task2",
                    "name": "Second Task",
                    "task_type": "content_creation",
                    "depends_on": ["task1"]
                }
            ]
        )
        
        assert workflow_id is not None
        assert workflow_id in engine.workflows


# ==================== QUALITY ENGINE TESTS ====================

class TestQualityEngine:
    """Tests for Quality Engine service."""
    
    @pytest.mark.asyncio
    async def test_engine_initialization(self):
        """Test quality engine initialization."""
        from app.services.ai.quality import QualityEngine
        
        engine = QualityEngine()
        await engine.initialize()
        
        assert engine._initialized
    
    @pytest.mark.asyncio
    async def test_quality_assessment(self):
        """Test quality assessment."""
        from app.services.ai.quality import QualityEngine
        
        engine = QualityEngine()
        await engine.initialize()
        
        assessment = await engine.assess(
            content="This is a test content for quality assessment.",
            context={"min_length": 10}
        )
        
        assert assessment is not None
        assert 0 <= assessment.overall_score <= 1
        assert len(assessment.checks) > 0
    
    @pytest.mark.asyncio
    async def test_quality_stats(self):
        """Test quality statistics."""
        from app.services.ai.quality import QualityEngine
        
        engine = QualityEngine()
        await engine.initialize()
        
        stats = engine.get_quality_stats()
        assert "total_assessments" in stats


# ==================== ORCHESTRATOR TESTS ====================

class TestMasterOrchestrator:
    """Tests for Master Orchestrator service."""
    
    @pytest.mark.asyncio
    async def test_orchestrator_initialization(self):
        """Test orchestrator initialization."""
        from app.services.ai.orchestrator import MasterOrchestrator
        
        orchestrator = MasterOrchestrator()
        await orchestrator.initialize()
        
        assert orchestrator._initialized
        assert orchestrator.gateway is not None
        assert orchestrator.router is not None
        assert orchestrator.memory_engine is not None
    
    @pytest.mark.asyncio
    async def test_orchestrator_status(self):
        """Test orchestrator status."""
        from app.services.ai.orchestrator import MasterOrchestrator
        
        orchestrator = MasterOrchestrator()
        await orchestrator.initialize()
        
        status = orchestrator.get_status()
        assert "state" in status
        assert "active_requests" in status
        assert "services" in status
    
    @pytest.mark.asyncio
    async def test_orchestrator_metrics(self):
        """Test orchestrator metrics."""
        from app.services.ai.orchestrator import MasterOrchestrator
        
        orchestrator = MasterOrchestrator()
        await orchestrator.initialize()
        
        metrics = orchestrator.get_metrics()
        assert "total_executions" in metrics


# ==================== INTEGRATION TESTS ====================

class TestIntegration:
    """Integration tests for the AI system."""
    
    @pytest.mark.asyncio
    async def test_full_pipeline(self):
        """Test full request processing pipeline."""
        from app.services.ai.orchestrator import MasterOrchestrator, AIRequest, RequestType
        
        orchestrator = MasterOrchestrator()
        await orchestrator.initialize()
        
        request = AIRequest(
            id="test-001",
            request_type=RequestType.CHAT,
            user_id="user-001",
            organization_id=None,
            workspace_id=None,
            prompt="Hello, how are you?",
            context={},
            constraints={},
            metadata={}
        )
        
        response = await orchestrator.process_request(request)
        
        assert response is not None
        assert response.request_id == "test-001"
        assert response.execution_time_ms > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
