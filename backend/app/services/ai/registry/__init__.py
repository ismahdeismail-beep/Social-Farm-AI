"""
Agent Registry Service

Manages AI agent registration, capabilities, health monitoring, and fallback chains.
"""

from typing import Optional, Dict, Any, List, Callable
from datetime import datetime, timezone
from dataclasses import dataclass, field
from enum import Enum
import logging
import asyncio

logger = logging.getLogger(__name__)


class AgentStatus(Enum):
    """Agent health status."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    OFFLINE = "offline"


@dataclass
class AgentInfo:
    """Information about a registered agent."""
    id: str
    name: str
    display_name: str
    description: str
    agent_type: str
    supported_tasks: List[str]
    preferred_models: List[str]
    max_context_tokens: int
    cost_per_1k_tokens: float
    average_latency_ms: float
    priority: int
    fallback_agent_id: Optional[str]
    max_concurrent_executions: int
    timeout_seconds: int
    config: Dict[str, Any]
    is_active: bool = True
    current_load: float = 0.0
    active_executions: int = 0
    health_status: AgentStatus = AgentStatus.HEALTHY
    success_rate: float = 1.0


@dataclass
class AgentCapability:
    """Agent capability definition."""
    name: str
    type: str
    proficiency_level: int
    supported_input_types: List[str]
    supported_output_types: List[str]


class AgentRegistry:
    """
    Registry for AI agents.
    
    Manages:
    - Agent registration and discovery
    - Capability-based agent selection
    - Health monitoring
    - Fallback agent chains
    - Load balancing
    """
    
    def __init__(self):
        self.agents: Dict[str, AgentInfo] = {}
        self.capabilities: Dict[str, List[AgentCapability]] = {}
        self.health_history: Dict[str, List[Dict[str, Any]]] = {}
        self._initialized = False
    
    async def initialize(self):
        """Initialize agent registry."""
        if self._initialized:
            return
        
        await self._register_default_agents()
        self._initialized = True
        logger.info("Agent Registry initialized with %d agents", len(self.agents))
    
    async def _register_default_agents(self):
        """Register default system agents."""
        default_agents = [
            AgentInfo(
                id="trend_agent",
                name="trend_agent",
                display_name="Trend Agent",
                description="Discovers and analyzes trending content and topics",
                agent_type="trend",
                supported_tasks=["trend_discovery", "trend_analysis", "trend_scoring"],
                preferred_models=["gemini-2.0-flash", "gpt-4o-mini"],
                max_context_tokens=100000,
                cost_per_1k_tokens=0.0001,
                average_latency_ms=1000,
                priority=10,
                fallback_agent_id=None,
                max_concurrent_executions=5,
                timeout_seconds=120,
                config={"crawlers": ["tiktok", "instagram", "twitter"]}
            ),
            AgentInfo(
                id="research_agent",
                name="research_agent",
                display_name="Research Agent",
                description="Conducts research on topics and sources",
                agent_type="research",
                supported_tasks=["research", "source_discovery", "fact_checking"],
                preferred_models=["gemini-2.5-pro", "gpt-4o"],
                max_context_tokens=200000,
                cost_per_1k_tokens=0.001,
                average_latency_ms=2000,
                priority=10,
                fallback_agent_id=None,
                max_concurrent_executions=3,
                timeout_seconds=180,
                config={"search_engines": ["tavily", "serpapi"]}
            ),
            AgentInfo(
                id="script_agent",
                name="script_agent",
                display_name="Script Agent",
                description="Creates scripts for video and audio content",
                agent_type="script",
                supported_tasks=["script_writing", "dialogue", "narration"],
                preferred_models=["claude-sonnet-4-20250514", "gpt-4o"],
                max_context_tokens=100000,
                cost_per_1k_tokens=0.003,
                average_latency_ms=1500,
                priority=10,
                fallback_agent_id=None,
                max_concurrent_executions=3,
                timeout_seconds=120,
                config={"creativity_level": "high"}
            ),
            AgentInfo(
                id="media_agent",
                name="media_agent",
                display_name="Media Agent",
                description="Generates images, thumbnails, and media assets",
                agent_type="media",
                supported_tasks=["image_generation", "thumbnail", "video_editing"],
                preferred_models=["dall-e-3", "stable-diffusion"],
                max_context_tokens=10000,
                cost_per_1k_tokens=0.04,
                average_latency_ms=5000,
                priority=10,
                fallback_agent_id=None,
                max_concurrent_executions=2,
                timeout_seconds=300,
                config={"quality": "high"}
            ),
            AgentInfo(
                id="publishing_agent",
                name="publishing_agent",
                display_name="Publishing Agent",
                description="Manages content publishing across platforms",
                agent_type="publishing",
                supported_tasks=["scheduling", "publishing", "cross_posting"],
                preferred_models=["gpt-4o-mini"],
                max_context_tokens=10000,
                cost_per_1k_tokens=0.00015,
                average_latency_ms=500,
                priority=10,
                fallback_agent_id=None,
                max_concurrent_executions=10,
                timeout_seconds=60,
                config={"platforms": ["tiktok", "instagram", "youtube"]}
            ),
            AgentInfo(
                id="analytics_agent",
                name="analytics_agent",
                display_name="Analytics Agent",
                description="Analyzes performance metrics and provides insights",
                agent_type="analytics",
                supported_tasks=["analytics", "reporting", "optimization"],
                preferred_models=["gpt-4o-mini", "gemini-2.0-flash"],
                max_context_tokens=50000,
                cost_per_1k_tokens=0.00015,
                average_latency_ms=1000,
                priority=10,
                fallback_agent_id=None,
                max_concurrent_executions=5,
                timeout_seconds=120,
                config={"report_formats": ["json", "markdown"]}
            ),
            AgentInfo(
                id="quality_agent",
                name="quality_agent",
                display_name="Quality Agent",
                description="Reviews and validates AI outputs for quality",
                agent_type="quality",
                supported_tasks=["quality_review", "validation", "feedback"],
                preferred_models=["claude-sonnet-4-20250514", "gpt-4o"],
                max_context_tokens=100000,
                cost_per_1k_tokens=0.003,
                average_latency_ms=1000,
                priority=15,  # Higher priority for quality checks
                fallback_agent_id=None,
                max_concurrent_executions=5,
                timeout_seconds=120,
                config={"strict_mode": False}
            ),
            AgentInfo(
                id="orchestrator_agent",
                name="orchestrator_agent",
                display_name="Master Orchestrator",
                description="Coordinates all agents and manages complex workflows",
                agent_type="orchestrator",
                supported_tasks=["planning", "delegation", "monitoring"],
                preferred_models=["gpt-4o", "claude-sonnet-4-20250514"],
                max_context_tokens=200000,
                cost_per_1k_tokens=0.005,
                average_latency_ms=500,
                priority=20,  # Highest priority
                fallback_agent_id=None,
                max_concurrent_executions=1,
                timeout_seconds=600,
                config={"max_workflow_depth": 10}
            ),
        ]
        
        for agent in default_agents:
            self.agents[agent.id] = agent
            self.capabilities[agent.id] = []
            self.health_history[agent.id] = []
    
    async def register_agent(
        self,
        agent_info: AgentInfo,
        capabilities: Optional[List[AgentCapability]] = None
    ) -> bool:
        """Register a new agent."""
        if agent_info.id in self.agents:
            logger.warning(f"Agent {agent_info.id} already registered, updating")
        
        self.agents[agent_info.id] = agent_info
        self.capabilities[agent_info.id] = capabilities or []
        self.health_history[agent_info.id] = []
        
        logger.info(f"Registered agent: {agent_info.name} ({agent_info.id})")
        return True
    
    async def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an agent."""
        if agent_id not in self.agents:
            return False
        
        agent = self.agents[agent_id]
        if agent.is_active and agent.active_executions > 0:
            logger.warning(f"Cannot unregister agent {agent_id} with active executions")
            return False
        
        del self.agents[agent_id]
        self.capabilities.pop(agent_id, None)
        self.health_history.pop(agent_id, None)
        
        logger.info(f"Unregistered agent: {agent_id}")
        return True
    
    async def get_agent(self, agent_id: str) -> Optional[AgentInfo]:
        """Get agent by ID."""
        return self.agents.get(agent_id)
    
    async def select_agent(
        self,
        task_type: str,
        exclude_agents: Optional[List[str]] = None,
        require_healthy: bool = True
    ) -> Optional[AgentInfo]:
        """
        Select the best agent for a task type.
        
        Selection criteria:
        1. Agent supports the task type
        2. Agent is active and healthy
        3. Agent has capacity
        4. Higher priority preferred
        5. Lower load preferred
        """
        candidates = []
        
        for agent in self.agents.values():
            # Check exclusions
            if exclude_agents and agent.id in exclude_agents:
                continue
            
            # Check if agent supports task
            if task_type not in agent.supported_tasks:
                continue
            
            # Check health
            if require_healthy and agent.health_status != AgentStatus.HEALTHY:
                continue
            
            # Check capacity
            if agent.active_executions >= agent.max_concurrent_executions:
                continue
            
            candidates.append(agent)
        
        if not candidates:
            return None
        
        # Sort by priority (desc) and load (asc)
        candidates.sort(
            key=lambda a: (-a.priority, a.current_load)
        )
        
        return candidates[0]
    
    async def get_fallback_chain(self, agent_id: str) -> List[str]:
        """Get fallback chain for an agent."""
        chain = []
        visited = set()
        
        current_id = agent_id
        while current_id and current_id not in visited:
            visited.add(current_id)
            agent = self.agents.get(current_id)
            if agent:
                chain.append(current_id)
                current_id = agent.fallback_agent_id
            else:
                break
        
        return chain
    
    async def update_health(
        self,
        agent_id: str,
        status: AgentStatus,
        success_rate: Optional[float] = None
    ):
        """Update agent health status."""
        if agent_id not in self.agents:
            return
        
        agent = self.agents[agent_id]
        agent.health_status = status
        
        if success_rate is not None:
            agent.success_rate = success_rate
        
        # Record health history
        self.health_history[agent_id].append({
            "status": status.value,
            "success_rate": agent.success_rate,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        
        # Keep only last 100 entries
        if len(self.health_history[agent_id]) > 100:
            self.health_history[agent_id] = self.health_history[agent_id][-100:]
    
    async def record_execution_start(self, agent_id: str):
        """Record execution start."""
        if agent_id in self.agents:
            agent = self.agents[agent_id]
            agent.active_executions += 1
            agent.current_load = agent.active_executions / max(agent.max_concurrent_executions, 1)
    
    async def record_execution_end(self, agent_id: str, success: bool):
        """Record execution end."""
        if agent_id in self.agents:
            agent = self.agents[agent_id]
            agent.active_executions = max(0, agent.active_executions - 1)
            agent.current_load = agent.active_executions / max(agent.max_concurrent_executions, 1)
    
    def get_registry_stats(self) -> Dict[str, Any]:
        """Get registry statistics."""
        active_agents = sum(1 for a in self.agents.values() if a.is_active)
        healthy_agents = sum(1 for a in self.agents.values() if a.health_status == AgentStatus.HEALTHY)
        total_executions = sum(a.active_executions for a in self.agents.values())
        
        return {
            "total_agents": len(self.agents),
            "active_agents": active_agents,
            "healthy_agents": healthy_agents,
            "total_active_executions": total_executions,
            "agents_by_type": {
                agent_type: sum(1 for a in self.agents.values() if a.agent_type == agent_type)
                for agent_type in set(a.agent_type for a in self.agents.values())
            }
        }


# Singleton instance
agent_registry = AgentRegistry()
