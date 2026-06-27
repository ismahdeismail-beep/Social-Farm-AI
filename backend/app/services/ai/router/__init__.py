"""
Model Router Service

Intelligent model routing based on task, cost, latency, and quality.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime, timezone
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class RoutingStrategy(Enum):
    """Model routing strategies."""
    COST_OPTIMIZED = "cost_optimized"
    LATENCY_OPTIMIZED = "latency_optimized"
    QUALITY_OPTIMIZED = "quality_optimized"
    BALANCED = "balanced"
    CAPABILITY = "capability"


@dataclass
class ModelCandidate:
    """A candidate model for routing."""
    provider: str
    model_id: str
    model_name: str
    cost_per_1k_tokens: float
    average_latency_ms: float
    quality_score: float
    context_window: int
    capabilities: List[str]
    is_available: bool = True
    health_score: float = 1.0


class ModelRouter:
    """
    Intelligent model router for AI requests.
    
    Selects the best model based on:
    - Task requirements
    - Cost constraints
    - Latency requirements
    - Quality needs
    - Provider health
    """
    
    def __init__(self):
        self.models: Dict[str, ModelCandidate] = {}
        self.routing_history: List[Dict[str, Any]] = []
        self._initialized = False
    
    async def initialize(self):
        """Initialize router with available models."""
        if self._initialized:
            return
        
        await self._load_models()
        self._initialized = True
        logger.info("Model Router initialized")
    
    async def _load_models(self):
        """Load available models from database, falling back to hardcoded defaults."""
        # Try loading from database first
        try:
            from app.db.session import SessionLocal
            from app.models.ai.provider import AIProvider, ModelProfile
            
            db = SessionLocal()
            try:
                providers = db.query(AIProvider).filter(
                    AIProvider.is_active == True
                ).all()
                
                for provider in providers:
                    profiles = db.query(ModelProfile).filter(
                        ModelProfile.provider_id == provider.id,
                        ModelProfile.is_active == True
                    ).all()
                    
                    for profile in profiles:
                        key = f"{provider.name}:{profile.model_id}"
                        self.models[key] = ModelCandidate(
                            provider=provider.name,
                            model_id=profile.model_id,
                            model_name=profile.display_name or profile.model_id,
                            cost_per_1k_tokens=profile.cost_per_1k_tokens or 0.001,
                            average_latency_ms=profile.average_latency_ms or 1000,
                            quality_score=profile.quality_score or 0.8,
                            context_window=profile.context_window or 8192,
                            capabilities=profile.capabilities or ["chat"],
                            is_available=profile.status == "active",
                            health_score=getattr(profile, 'health_score', 1.0) or 1.0,
                        )
                
                if self.models:
                    logger.info(f"Loaded {len(self.models)} models from database")
                    return
            finally:
                db.close()
        except Exception as e:
            logger.warning(f"Could not load models from database: {e}")
        
        logger.info("Using default model configurations")
        # Placeholder models (fallback)
            ModelCandidate(
                provider="openai",
                model_id="gpt-4o",
                model_name="GPT-4o",
                cost_per_1k_tokens=0.005,
                average_latency_ms=1500,
                quality_score=0.95,
                context_window=128000,
                capabilities=["chat", "reasoning", "code", "analysis"]
            ),
            ModelCandidate(
                provider="openai",
                model_id="gpt-4o-mini",
                model_name="GPT-4o Mini",
                cost_per_1k_tokens=0.00015,
                average_latency_ms=800,
                quality_score=0.85,
                context_window=128000,
                capabilities=["chat", "reasoning", "code"]
            ),
            ModelCandidate(
                provider="anthropic",
                model_id="claude-sonnet-4-20250514",
                model_name="Claude Sonnet",
                cost_per_1k_tokens=0.003,
                average_latency_ms=1200,
                quality_score=0.93,
                context_window=200000,
                capabilities=["chat", "reasoning", "code", "analysis", "creative"]
            ),
            ModelCandidate(
                provider="google",
                model_id="gemini-2.0-flash",
                model_name="Gemini 2.0 Flash",
                cost_per_1k_tokens=0.0001,
                average_latency_ms=600,
                quality_score=0.88,
                context_window=1000000,
                capabilities=["chat", "reasoning", "code", "vision"]
            ),
            ModelCandidate(
                provider="google",
                model_id="gemini-2.5-pro",
                model_name="Gemini 2.5 Pro",
                cost_per_1k_tokens=0.00125,
                average_latency_ms=1000,
                quality_score=0.92,
                context_window=1000000,
                capabilities=["chat", "reasoning", "code", "analysis", "vision"]
            ),
        ]
        
        for model in default_models:
            key = f"{model.provider}:{model.model_id}"
            self.models[key] = model
    
    async def route(
        self,
        task_type: str,
        requirements: Optional[Dict[str, Any]] = None,
        strategy: RoutingStrategy = RoutingStrategy.BALANCED,
        budget_limit: Optional[float] = None,
        latency_limit_ms: Optional[int] = None,
        exclude_models: Optional[List[str]] = None
    ) -> ModelCandidate:
        """
        Route to the best model for the given task.
        
        Args:
            task_type: Type of task (chat, code, analysis, creative, etc.)
            requirements: Additional requirements
            strategy: Routing strategy
            budget_limit: Maximum cost per 1k tokens
            latency_limit_ms: Maximum latency in milliseconds
            exclude_models: Models to exclude from consideration
            
        Returns:
            Best model candidate
        """
        if not self._initialized:
            await self.initialize()
        
        # Filter candidates
        candidates = await self._filter_candidates(
            task_type=task_type,
            requirements=requirements,
            budget_limit=budget_limit,
            latency_limit_ms=latency_limit_ms,
            exclude_models=exclude_models
        )
        
        if not candidates:
            raise Exception(f"No suitable model found for task type: {task_type}")
        
        # Score and rank candidates
        scored_candidates = self._score_candidates(candidates, strategy, requirements)
        
        # Select best
        best = scored_candidates[0]
        
        # Log routing decision
        self.routing_history.append({
            "task_type": task_type,
            "strategy": strategy.value,
            "selected_model": f"{best.provider}:{best.model_id}",
            "score": scored_candidates[0][1] if isinstance(scored_candidates[0], tuple) else best.quality_score,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        
        return best
    
    async def _filter_candidates(
        self,
        task_type: str,
        requirements: Optional[Dict[str, Any]],
        budget_limit: Optional[float],
        latency_limit_ms: Optional[int],
        exclude_models: Optional[List[str]]
    ) -> List[ModelCandidate]:
        """Filter models based on requirements."""
        candidates = []
        
        for key, model in self.models.items():
            # Check availability
            if not model.is_available or model.health_score < 0.5:
                continue
            
            # Check exclusions
            if exclude_models and key in exclude_models:
                continue
            
            # Check budget
            if budget_limit and model.cost_per_1k_tokens > budget_limit:
                continue
            
            # Check latency
            if latency_limit_ms and model.average_latency_ms > latency_limit_ms:
                continue
            
            # Check capabilities
            if task_type not in model.capabilities and "chat" not in model.capabilities:
                continue
            
            candidates.append(model)
        
        return candidates
    
    def _score_candidates(
        self,
        candidates: List[ModelCandidate],
        strategy: RoutingStrategy,
        requirements: Optional[Dict[str, Any]]
    ) -> List[ModelCandidate]:
        """Score and rank candidates based on strategy."""
        scored = []
        
        for model in candidates:
            score = self._calculate_score(model, strategy, requirements)
            scored.append((model, score))
        
        # Sort by score (descending)
        scored.sort(key=lambda x: x[1], reverse=True)
        
        return [model for model, score in scored]
    
    def _calculate_score(
        self,
        model: ModelCandidate,
        strategy: RoutingStrategy,
        requirements: Optional[Dict[str, Any]]
    ) -> float:
        """Calculate score for a model based on strategy."""
        if strategy == RoutingStrategy.COST_OPTIMIZED:
            # Lower cost = higher score
            cost_score = 1.0 - min(model.cost_per_1k_tokens / 0.01, 1.0)
            return cost_score * 0.7 + model.quality_score * 0.3
        
        elif strategy == RoutingStrategy.LATENCY_OPTIMIZED:
            # Lower latency = higher score
            latency_score = 1.0 - min(model.average_latency_ms / 2000, 1.0)
            return latency_score * 0.7 + model.quality_score * 0.3
        
        elif strategy == RoutingStrategy.QUALITY_OPTIMIZED:
            return model.quality_score
        
        elif strategy == RoutingStrategy.CAPABILITY:
            # Check specific capabilities
            required = requirements.get("capabilities", []) if requirements else []
            if not required:
                return model.quality_score
            matched = len(set(required) & set(model.capabilities))
            return matched / len(required) if required else 0
        
        else:  # BALANCED
            cost_score = 1.0 - min(model.cost_per_1k_tokens / 0.01, 1.0)
            latency_score = 1.0 - min(model.average_latency_ms / 2000, 1.0)
            return (
                model.quality_score * 0.4 +
                cost_score * 0.3 +
                latency_score * 0.3
            )
    
    def get_model_info(self, provider: str, model_id: str) -> Optional[ModelCandidate]:
        """Get information about a specific model."""
        key = f"{provider}:{model_id}"
        return self.models.get(key)
    
    def get_routing_stats(self) -> Dict[str, Any]:
        """Get routing statistics."""
        return {
            "total_models": len(self.models),
            "available_models": sum(1 for m in self.models.values() if m.is_available),
            "routing_history_count": len(self.routing_history),
            "recent_routes": self.routing_history[-10:] if self.routing_history else []
        }


# Singleton instance
router = ModelRouter()
