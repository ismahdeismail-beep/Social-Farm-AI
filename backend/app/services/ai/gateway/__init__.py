"""
AI Gateway Service

Central interface for all AI provider interactions.
Handles provider management, request normalization, retry logic, and cost tracking.
"""

import os
import json
from typing import Optional, Dict, Any, List, AsyncGenerator
from datetime import datetime, timezone
from dataclasses import dataclass
from enum import Enum
import asyncio
import logging
import httpx

logger = logging.getLogger(__name__)


class ProviderStatus(Enum):
    """Provider health status."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    OFFLINE = "offline"


@dataclass
class AIRequest:
    """Standardized AI request."""
    model: str
    messages: List[Dict[str, str]]
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    tools: Optional[List[Dict]] = None
    tool_choice: Optional[str] = None
    stream: bool = False
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class AIResponse:
    """Standardized AI response."""
    content: str
    model: str
    provider: str
    tokens_input: int
    tokens_output: int
    tokens_total: int
    cost_usd: float
    latency_ms: float
    tool_calls: Optional[List[Dict]] = None
    finish_reason: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class ProviderConfig:
    """Provider configuration."""
    name: str
    api_base_url: str
    api_key: str
    models: List[str]
    rate_limit: int = 60
    timeout: int = 30
    retry_attempts: int = 3


class CircuitBreaker:
    """Circuit breaker pattern for provider resilience."""
    
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time: Optional[datetime] = None
        self.state = "closed"  # closed, open, half-open
    
    def record_failure(self):
        """Record a failure."""
        self.failure_count += 1
        self.last_failure_time = datetime.now(timezone.utc)
        if self.failure_count >= self.failure_threshold:
            self.state = "open"
            logger.warning(f"Circuit breaker opened after {self.failure_count} failures")
    
    def record_success(self):
        """Record a success."""
        self.failure_count = 0
        self.state = "closed"
    
    def can_execute(self) -> bool:
        """Check if we can attempt execution."""
        if self.state == "closed":
            return True
        if self.state == "open" and self.last_failure_time:
            elapsed = (datetime.now(timezone.utc) - self.last_failure_time).total_seconds()
            if elapsed >= self.recovery_timeout:
                self.state = "half-open"
                return True
        return False
    
    def get_state(self) -> Dict[str, Any]:
        """Get circuit breaker state."""
        return {
            "state": self.state,
            "failure_count": self.failure_count,
            "last_failure_time": self.last_failure_time.isoformat() if self.last_failure_time else None,
            "threshold": self.failure_threshold,
            "recovery_timeout": self.recovery_timeout
        }


class AIGateway:
    """
    Central AI Gateway for provider management.
    
    Handles:
    - Multi-provider support
    - Request/response normalization
    - Retry with exponential backoff
    - Circuit breaker pattern
    - Cost tracking
    - Streaming support
    """
    
    def __init__(self):
        self.providers: Dict[str, ProviderConfig] = {}
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.cost_tracker: Dict[str, float] = {}
        self._initialized = False
    
    async def initialize(self):
        """Initialize the gateway with configured providers."""
        if self._initialized:
            return
        
        # Load providers from database
        await self._load_providers()
        self._initialized = True
        logger.info("AI Gateway initialized")
    
    async def _load_providers(self):
        """Load provider configurations from database or environment."""
        # Try loading from database first
        # TODO: Load from database when provider model is available
        
        # Load from environment variables
        default_providers = {}
        
        openai_key = os.getenv("OPENAI_API_KEY", "")
        if openai_key:
            default_providers["openai"] = ProviderConfig(
                name="openai",
                api_base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
                api_key=openai_key,
                models=["gpt-4o", "gpt-4o-mini", "gpt-4-turbo"],
                rate_limit=60,
                timeout=30
            )
        
        anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")
        if anthropic_key:
            default_providers["anthropic"] = ProviderConfig(
                name="anthropic",
                api_base_url=os.getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com/v1"),
                api_key=anthropic_key,
                models=["claude-sonnet-4-20250514", "claude-3-5-haiku-20241022"],
                rate_limit=60,
                timeout=30
            )
        
        google_key = os.getenv("GOOGLE_API_KEY", "")
        if google_key:
            default_providers["google"] = ProviderConfig(
                name="google",
                api_base_url=os.getenv("GOOGLE_BASE_URL", "https://generativelanguage.googleapis.com/v1beta"),
                api_key=google_key,
                models=["gemini-2.0-flash", "gemini-2.5-pro"],
                rate_limit=60,
                timeout=30
            )
        
        # Always create entries even without keys (for fallback chains)
        for name, api_key_env, base_url, models in [
            ("openai", "OPENAI_API_KEY", "https://api.openai.com/v1",
             ["gpt-4o", "gpt-4o-mini"]),
            ("anthropic", "ANTHROPIC_API_KEY", "https://api.anthropic.com/v1",
             ["claude-sonnet-4-20250514"]),
            ("google", "GOOGLE_API_KEY", "https://generativelanguage.googleapis.com/v1beta",
             ["gemini-2.0-flash", "gemini-2.5-pro"]),
        ]:
            if name not in default_providers:
                default_providers[name] = ProviderConfig(
                    name=name,
                    api_base_url=os.getenv(f"{name.upper()}_BASE_URL", base_url),
                    api_key=os.getenv(api_key_env, ""),
                    models=models,
                    rate_limit=60,
                    timeout=30
                )
        
        for name, config in default_providers.items():
            self.providers[name] = config
            self.circuit_breakers[name] = CircuitBreaker()
            self.cost_tracker[name] = 0.0
    
    async def execute(
        self,
        request: AIRequest,
        provider: Optional[str] = None,
        fallback_providers: Optional[List[str]] = None
    ) -> AIResponse:
        """
        Execute an AI request with automatic provider selection and fallback.
        
        Args:
            request: Standardized AI request
            provider: Preferred provider name
            fallback_providers: List of fallback providers
            
        Returns:
            Standardized AI response
            
        Raises:
            Exception: If all providers fail
        """
        if not self._initialized:
            await self.initialize()
        
        # Determine provider order
        provider_order = self._get_provider_order(provider, fallback_providers)
        
        last_error = None
        for provider_name in provider_order:
            if provider_name not in self.providers:
                continue
            
            circuit_breaker = self.circuit_breakers.get(provider_name)
            if circuit_breaker and not circuit_breaker.can_execute():
                logger.warning(f"Provider {provider_name} circuit breaker is open, skipping")
                continue
            
            try:
                response = await self._execute_with_provider(provider_name, request)
                
                # Record success
                if circuit_breaker:
                    circuit_breaker.record_success()
                
                # Track cost
                self.cost_tracker[provider_name] = self.cost_tracker.get(provider_name, 0) + response.cost_usd
                
                return response
                
            except Exception as e:
                last_error = e
                logger.error(f"Provider {provider_name} failed: {e}")
                
                # Record failure
                if circuit_breaker:
                    circuit_breaker.record_failure()
                
                continue
        
        raise Exception(f"All providers failed. Last error: {last_error}")
    
    async def _execute_with_provider(
        self,
        provider_name: str,
        request: AIRequest
    ) -> AIResponse:
        """Execute request with a specific provider via real HTTP calls."""
        start_time = datetime.now(timezone.utc)
        
        config = self.providers.get(provider_name)
        if not config:
            raise ValueError(f"Provider {provider_name} not configured")
        
        if not config.api_key:
            raise ValueError(f"API key not configured for provider {provider_name}")
        
        async with httpx.AsyncClient(timeout=config.timeout) as client:
            if provider_name == "openai":
                response = await self._call_openai(client, config, request)
            elif provider_name == "anthropic":
                response = await self._call_anthropic(client, config, request)
            elif provider_name == "google":
                response = await self._call_google(client, config, request)
            else:
                raise ValueError(f"Unsupported provider: {provider_name}")
        
        latency_ms = (datetime.now(timezone.utc) - start_time).total_seconds() * 1000
        
        # Calculate cost based on actual token usage
        cost_usd = self._calculate_cost(
            provider_name, request.model,
            response["tokens_input"], response["tokens_output"]
        )
        
        return AIResponse(
            content=response["content"],
            model=response.get("model", request.model),
            provider=provider_name,
            tokens_input=response["tokens_input"],
            tokens_output=response["tokens_output"],
            tokens_total=response["tokens_input"] + response["tokens_output"],
            cost_usd=cost_usd,
            latency_ms=latency_ms,
            tool_calls=response.get("tool_calls"),
            finish_reason=response.get("finish_reason", "stop"),
            metadata={"raw_response": response.get("raw_headers", {})}
        )
    
    async def _call_openai(
        self,
        client: httpx.AsyncClient,
        config: ProviderConfig,
        request: AIRequest
    ) -> Dict[str, Any]:
        """Call OpenAI-compatible API."""
        url = f"{config.api_base_url}/chat/completions"
        
        body: Dict[str, Any] = {
            "model": request.model,
            "messages": request.messages,
            "temperature": request.temperature,
        }
        if request.max_tokens:
            body["max_tokens"] = request.max_tokens
        if request.tools:
            body["tools"] = request.tools
        if request.tool_choice:
            body["tool_choice"] = request.tool_choice
        if request.stream:
            body["stream"] = True
        
        resp = await client.post(
            url,
            headers={
                "Authorization": f"Bearer {config.api_key}",
                "Content-Type": "application/json",
            },
            json=body,
        )
        resp.raise_for_status()
        data = resp.json()
        
        choice = data["choices"][0]
        message = choice.get("message", {})
        
        return {
            "content": message.get("content", "") or "",
            "model": data.get("model", request.model),
            "tokens_input": data["usage"]["prompt_tokens"],
            "tokens_output": data["usage"]["completion_tokens"],
            "finish_reason": choice.get("finish_reason", "stop"),
            "tool_calls": message.get("tool_calls"),
            "raw_headers": dict(resp.headers),
        }
    
    async def _call_anthropic(
        self,
        client: httpx.AsyncClient,
        config: ProviderConfig,
        request: AIRequest
    ) -> Dict[str, Any]:
        """Call Anthropic API."""
        url = f"{config.api_base_url}/messages"
        
        # Convert OpenAI messages to Anthropic format
        system_msg = None
        anthropic_messages = []
        for msg in request.messages:
            if msg["role"] == "system":
                system_msg = msg["content"]
            elif msg["role"] == "user":
                anthropic_messages.append({"role": "user", "content": msg["content"]})
            elif msg["role"] == "assistant":
                anthropic_messages.append({"role": "assistant", "content": msg["content"]})
        
        body: Dict[str, Any] = {
            "model": request.model,
            "messages": anthropic_messages,
            "max_tokens": request.max_tokens or 1024,
            "temperature": request.temperature,
        }
        if system_msg:
            body["system"] = system_msg
        
        resp = await client.post(
            url,
            headers={
                "x-api-key": config.api_key,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json",
            },
            json=body,
        )
        resp.raise_for_status()
        data = resp.json()
        
        content = ""
        for block in data.get("content", []):
            if block.get("type") == "text":
                content += block.get("text", "")
        
        return {
            "content": content,
            "model": data.get("model", request.model),
            "tokens_input": data["usage"]["input_tokens"],
            "tokens_output": data["usage"]["output_tokens"],
            "finish_reason": data.get("stop_reason", "end_turn"),
            "tool_calls": None,
            "raw_headers": dict(resp.headers),
        }
    
    async def _call_google(
        self,
        client: httpx.AsyncClient,
        config: ProviderConfig,
        request: AIRequest
    ) -> Dict[str, Any]:
        """Call Google Gemini API."""
        # Convert OpenAI messages to Google format
        google_contents = []
        for msg in request.messages:
            role = "model" if msg["role"] == "assistant" else msg["role"]
            google_contents.append({
                "role": role,
                "parts": [{"text": msg["content"]}]
            })
        
        url = f"{config.api_base_url}/models/{request.model}:generateContent"
        
        body = {
            "contents": google_contents,
            "generationConfig": {
                "temperature": request.temperature,
            }
        }
        if request.max_tokens:
            body["generationConfig"]["maxOutputTokens"] = request.max_tokens
        
        resp = await client.post(
            url,
            params={"key": config.api_key},
            json=body,
        )
        resp.raise_for_status()
        data = resp.json()
        
        candidate = data.get("candidates", [{}])[0]
        content_parts = candidate.get("content", {}).get("parts", [])
        content = "".join(p.get("text", "") for p in content_parts)
        
        usage = data.get("usageMetadata", {})
        
        return {
            "content": content,
            "model": request.model,
            "tokens_input": usage.get("promptTokenCount", 0),
            "tokens_output": usage.get("candidatesTokenCount", 0),
            "finish_reason": candidate.get("finishReason", "STOP"),
            "tool_calls": None,
            "raw_headers": dict(resp.headers),
        }
    
    def _calculate_cost(
        self,
        provider: str,
        model: str,
        tokens_input: int,
        tokens_output: int
    ) -> float:
        """Calculate cost based on token usage."""
        # Approximate costs per 1K tokens (in USD)
        cost_rates = {
            "openai": {
                "gpt-4o": {"input": 0.005, "output": 0.015},
                "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
                "gpt-4-turbo": {"input": 0.01, "output": 0.03},
            },
            "anthropic": {
                "claude-sonnet-4-20250514": {"input": 0.003, "output": 0.015},
                "claude-3-5-haiku-20241022": {"input": 0.0008, "output": 0.004},
            },
            "google": {
                "gemini-2.0-flash": {"input": 0.0001, "output": 0.0004},
                "gemini-2.5-pro": {"input": 0.00125, "output": 0.005},
            },
        }
        
        rates = cost_rates.get(provider, {}).get(model, {"input": 0.001, "output": 0.002})
        input_cost = (tokens_input / 1000) * rates["input"]
        output_cost = (tokens_output / 1000) * rates["output"]
        
        return round(input_cost + output_cost, 6)
    
    def _get_provider_order(
        self,
        preferred: Optional[str],
        fallbacks: Optional[List[str]]
    ) -> List[str]:
        """Get ordered list of providers to try."""
        order = []
        
        if preferred:
            order.append(preferred)
        
        if fallbacks:
            order.extend(fallbacks)
        
        # Add remaining providers
        for provider in self.providers:
            if provider not in order:
                order.append(provider)
        
        return order
    
    async def stream(
        self,
        request: AIRequest,
        provider: Optional[str] = None
    ) -> AsyncGenerator[str, None]:
        """Stream AI response from the provider."""
        provider_name = provider or "openai"
        
        config = self.providers.get(provider_name)
        if not config or not config.api_key:
            yield f"Error: Provider {provider_name} not configured"
            return
        
        # Force streaming mode
        request.stream = True
        
        async with httpx.AsyncClient(timeout=config.timeout) as client:
            try:
                if provider_name == "openai":
                    url = f"{config.api_base_url}/chat/completions"
                    body: Dict[str, Any] = {
                        "model": request.model,
                        "messages": request.messages,
                        "temperature": request.temperature,
                        "stream": True,
                    }
                    if request.max_tokens:
                        body["max_tokens"] = request.max_tokens
                    
                    async with client.stream(
                        "POST",
                        url,
                        headers={
                            "Authorization": f"Bearer {config.api_key}",
                            "Content-Type": "application/json",
                        },
                        json=body,
                    ) as resp:
                        resp.raise_for_status()
                        async for line in resp.aiter_lines():
                            if line.startswith("data: "):
                                data_str = line[6:]
                                if data_str.strip() == "[DONE]":
                                    break
                                try:
                                    chunk = json.loads(data_str)
                                    delta = chunk.get("choices", [{}])[0].get("delta", {})
                                    content = delta.get("content", "")
                                    if content:
                                        yield content
                                except json.JSONDecodeError:
                                    continue
                
                elif provider_name == "anthropic":
                    url = f"{config.api_base_url}/messages"
                    system_msg = None
                    anthropic_messages = []
                    for msg in request.messages:
                        if msg["role"] == "system":
                            system_msg = msg["content"]
                        elif msg["role"] == "user":
                            anthropic_messages.append({"role": "user", "content": msg["content"]})
                        elif msg["role"] == "assistant":
                            anthropic_messages.append({"role": "assistant", "content": msg["content"]})
                    
                    body = {
                        "model": request.model,
                        "messages": anthropic_messages,
                        "max_tokens": request.max_tokens or 1024,
                        "temperature": request.temperature,
                        "stream": True,
                    }
                    if system_msg:
                        body["system"] = system_msg
                    
                    async with client.stream(
                        "POST",
                        url,
                        headers={
                            "x-api-key": config.api_key,
                            "anthropic-version": "2023-06-01",
                            "Content-Type": "application/json",
                        },
                        json=body,
                    ) as resp:
                        resp.raise_for_status()
                        async for line in resp.aiter_lines():
                            if line.startswith("data: "):
                                data_str = line[6:]
                                try:
                                    chunk = json.loads(data_str)
                                    if chunk.get("type") == "content_block_delta":
                                        delta = chunk.get("delta", {})
                                        text = delta.get("text", "")
                                        if text:
                                            yield text
                                except json.JSONDecodeError:
                                    continue
                
                elif provider_name == "google":
                    url = f"{config.api_base_url}/models/{request.model}:streamGenerateContent"
                    google_contents = []
                    for msg in request.messages:
                        role = "model" if msg["role"] == "assistant" else msg["role"]
                        google_contents.append({
                            "role": role,
                            "parts": [{"text": msg["content"]}]
                        })
                    
                    body = {
                        "contents": google_contents,
                        "generationConfig": {"temperature": request.temperature}
                    }
                    
                    async with client.stream(
                        "POST",
                        url,
                        params={"key": config.api_key},
                        json=body,
                    ) as resp:
                        resp.raise_for_status()
                        async for line in resp.aiter_lines():
                            if line.startswith("data: "):
                                data_str = line[6:]
                                try:
                                    chunk = json.loads(data_str)
                                    parts = (chunk.get("candidates", [{}])[0]
                                             .get("content", {})
                                             .get("parts", []))
                                    for part in parts:
                                        text = part.get("text", "")
                                        if text:
                                            yield text
                                except json.JSONDecodeError:
                                    continue
                else:
                    yield f"Error: Streaming not supported for provider {provider_name}"
            
            except Exception as e:
                logger.error(f"Streaming error from {provider_name}: {e}")
                yield f"Error: {str(e)}"
    
    def get_cost_summary(self) -> Dict[str, float]:
        """Get cost summary by provider."""
        return self.cost_tracker.copy()
    
    def get_provider_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all providers."""
        status = {}
        for name, config in self.providers.items():
            circuit_breaker = self.circuit_breakers.get(name)
            status[name] = {
                "name": name,
                "models": config.models,
                "rate_limit": config.rate_limit,
                "circuit_breaker": circuit_breaker.get_state() if circuit_breaker else None,
                "total_cost": self.cost_tracker.get(name, 0.0)
            }
        return status


# Singleton instance
gateway = AIGateway()
