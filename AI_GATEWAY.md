# AI Gateway — Social Farm AI OS

## Overview

The AI Gateway provides a unified interface for multiple AI providers, enabling intelligent routing, failover, and cost optimization.

## Supported Providers

| Provider | Models | Status | Cost Tier |
|----------|--------|--------|-----------|
| OpenAI | GPT-4, GPT-4 Turbo, GPT-3.5 | ✅ Active | High |
| Anthropic | Claude 3 Opus, Sonnet, Haiku | ✅ Active | High |
| Google | Gemini 1.5 Pro, Flash | ✅ Active | Medium |
| xAI | Grok-3 | ✅ Active | Medium |
| DeepSeek | DeepSeek Chat V3 | ✅ Active | Low |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      AI Gateway                             │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Router    │  │  Registry   │  │   Quality   │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│         │                │                │                  │
│         ▼                ▼                ▼                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Provider Adapters                       │   │
│  ├─────────┬─────────┬─────────┬─────────┬─────────┤   │
│  │ OpenAI  │Anthropic│ Google  │  xAI    │DeepSeek │   │
│  └─────────┴─────────┴─────────┴─────────┴─────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Components

### 1. Router

Intelligent routing based on:
- **Task type** (chat, completion, embedding)
- **Cost optimization** (cheapest provider for task)
- **Latency requirements** (fastest provider)
- **Quality requirements** (best provider for task)
- **Failover** (automatic provider switching)

```python
from app.services.ai.router import AIRouter

router = AIRouter()

# Automatic routing
response = await router.chat(
    messages=[{"role": "user", "content": "Hello"}],
    task_type="chat",
    quality="high"
)

# Specific provider
response = await router.chat(
    messages=[{"role": "user", "content": "Hello"}],
    provider="openai",
    model="gpt-4"
)
```

### 2. Registry

Provider configuration and management:
- API keys and credentials
- Rate limits and quotas
- Model capabilities
- Cost tracking

```python
from app.services.ai.registry import AIRegistry

registry = AIRegistry()

# List providers
providers = registry.list_providers()

# Get provider config
config = registry.get_provider("openai")

# Update provider
registry.update_provider("openai", {
    "api_key": "new-key",
    "rate_limit": 100
})
```

### 3. Quality Engine

Output validation and filtering:
- Content moderation
- Toxicity detection
- Hallucination checking
- Format validation

```python
from app.services.ai.quality import AIQuality

quality = AIQuality()

# Validate output
result = await quality.validate(
    output="AI generated text",
    rules=["no_toxicity", "no_hallucination"]
)

if result.is_valid:
    # Use output
    pass
else:
    # Handle quality issues
    pass
```

## Provider Configuration

### OpenAI

```python
OPENAI_CONFIG = {
    "api_key": os.getenv("OPENAI_API_KEY"),
    "models": {
        "gpt-4": {"max_tokens": 8192, "cost_per_1k": 0.03},
        "gpt-4-turbo": {"max_tokens": 128000, "cost_per_1k": 0.01},
        "gpt-3.5-turbo": {"max_tokens": 4096, "cost_per_1k": 0.002},
    },
    "rate_limit": 60,  # requests per minute
    "timeout": 60,
}
```

### Anthropic

```python
ANTHROPIC_CONFIG = {
    "api_key": os.getenv("ANTHROPIC_API_KEY"),
    "models": {
        "claude-3-opus": {"max_tokens": 200000, "cost_per_1k": 0.015},
        "claude-3-sonnet": {"max_tokens": 200000, "cost_per_1k": 0.003},
        "claude-3-haiku": {"max_tokens": 200000, "cost_per_1k": 0.00025},
    },
    "rate_limit": 60,
    "timeout": 60,
}
```

### Google Gemini

```python
GEMINI_CONFIG = {
    "api_key": os.getenv("GOOGLE_API_KEY"),
    "models": {
        "gemini-1.5-pro": {"max_tokens": 1000000, "cost_per_1k": 0.00125},
        "gemini-1.5-flash": {"max_tokens": 1000000, "cost_per_1k": 0.000075},
    },
    "rate_limit": 60,
    "timeout": 60,
}
```

### xAI (Grok)

```python
XAI_CONFIG = {
    "api_key": os.getenv("XAI_API_KEY"),
    "models": {
        "grok-3": {"max_tokens": 128000, "cost_per_1k": 0.005},
    },
    "rate_limit": 60,
    "timeout": 60,
}
```

### DeepSeek

```python
DEEPSEEK_CONFIG = {
    "api_key": os.getenv("DEEPSEEK_API_KEY"),
    "models": {
        "deepseek-chat-v3": {"max_tokens": 32000, "cost_per_1k": 0.00014},
    },
    "rate_limit": 60,
    "timeout": 60,
}
```

## Routing Strategies

### 1. Cost Optimization

Selects the cheapest provider for the task:

```python
# Task: Simple chat completion
# Options: GPT-3.5 ($0.002/1k), Claude Haiku ($0.00025/1k)
# Selected: Claude Haiku (cheapest)
```

### 2. Quality Optimization

Selects the best provider for the task:

```python
# Task: Complex reasoning
# Options: GPT-4, Claude Opus, Gemini Pro
# Selected: Claude Opus (best for reasoning)
```

### 3. Latency Optimization

Selects the fastest provider:

```python
# Task: Real-time chat
# Options: GPT-3.5, Gemini Flash
# Selected: Gemini Flash (fastest)
```

### 4. Failover

Automatic provider switching on failure:

```python
# Primary: OpenAI GPT-4
# Fallback 1: Anthropic Claude Opus
# Fallback 2: Google Gemini Pro
# Fallback 3: DeepSeek Chat V3
```

## Usage Examples

### Basic Chat

```python
from app.services.ai.gateway import AIGateway

gateway = AIGateway()

# Simple chat
response = await gateway.chat(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"}
    ]
)

print(response.content)  # "The capital of France is Paris."
```

### Task-Specific Routing

```python
# Creative writing
response = await gateway.chat(
    messages=[...],
    task_type="creative",
    # Automatically routes to best creative model
)

# Code generation
response = await gateway.chat(
    messages=[...],
    task_type="code",
    # Automatically routes to best code model
)

# Analysis
response = await gateway.chat(
    messages=[...],
    task_type="analysis",
    # Automatically routes to best analysis model
)
```

### With Quality Checks

```python
response = await gateway.chat(
    messages=[...],
    quality_checks=["toxicity", "hallucination", "format"]
)

if response.quality_passed:
    # Use response
    pass
else:
    # Handle quality issues
    print(response.quality_issues)
```

## Error Handling

### Provider Errors

```python
from app.services.ai.gateway import AIGateway, ProviderError

gateway = AIGateway()

try:
    response = await gateway.chat(messages=[...])
except ProviderError as e:
    if e.error_type == "rate_limit":
        # Wait and retry
        await asyncio.sleep(e.retry_after)
        response = await gateway.chat(messages=[...])
    elif e.error_type == "auth":
        # Check API key
        pass
    elif e.error_type == "model_unavailable":
        # Try fallback model
        pass
```

### Quality Errors

```python
from app.services.ai.quality import QualityError

try:
    response = await gateway.chat(
        messages=[...],
        quality_checks=["toxicity"]
    )
except QualityError as e:
    if e.issue == "toxicity":
        # Refuse response
        pass
    elif e.issue == "hallucination":
        # Request clarification
        pass
```

## Monitoring

### Metrics

```python
# Track usage
metrics = {
    "provider": "openai",
    "model": "gpt-4",
    "tokens_used": 150,
    "cost": 0.0045,
    "latency_ms": 1200,
    "quality_score": 0.95,
}
```

### Dashboards

- **Provider Usage:** Requests per provider, model
- **Cost Tracking:** Daily, monthly costs
- **Latency:** Average, p95, p99 latency
- **Quality:** Quality scores, rejection rates
- **Errors:** Error rates by provider

## Best Practices

### 1. Use Appropriate Models

```python
# ❌ Bad: Using GPT-4 for simple tasks
response = await gateway.chat(
    messages=[...],
    model="gpt-4"
)

# ✅ Good: Route based on task complexity
response = await gateway.chat(
    messages=[...],
    task_type="simple_chat"  # Routes to cheaper model
)
```

### 2. Implement Caching

```python
# Cache responses for repeated queries
cache_key = hash_messages(messages)
cached = await redis.get(f"ai_cache:{cache_key}")

if cached:
    return json.loads(cached)

response = await gateway.chat(messages=[...])
await redis.setex(f"ai_cache:{cache_key}", 3600, json.dumps(response))
```

### 3. Handle Failures Gracefully

```python
# Always have fallback options
response = await gateway.chat(
    messages=[...],
    fallback_providers=["anthropic", "google", "deepseek"]
)
```

### 4. Monitor Costs

```python
# Track and limit costs
daily_cost = await get_daily_cost()
if daily_cost > DAILY_LIMIT:
    raise CostLimitExceeded()
```

## Configuration

### Environment Variables

```bash
# Provider API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...
XAI_API_KEY=...
DEEPSEEK_API_KEY=...

# Gateway Settings
AI_GATEWAY_LOG_LEVEL=info
AI_GATEWAY_TIMEOUT=60
AI_GATEWAY_MAX_RETRIES=3

# Rate Limits
OPENAI_RATE_LIMIT=60
ANTHROPIC_RATE_LIMIT=60
GEMINI_RATE_LIMIT=60
XAI_RATE_LIMIT=60
DEEPSEEK_RATE_LIMIT=60
```

## Troubleshooting

### Common Issues

#### API Key Errors
```bash
# Check API keys
echo $OPENAI_API_KEY
echo $ANTHROPIC_API_KEY
```

#### Rate Limiting
```python
# Implement exponential backoff
import asyncio
import random

async def retry_with_backoff(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await func()
        except RateLimitError:
            wait_time = (2 ** attempt) + random.uniform(0, 1)
            await asyncio.sleep(wait_time)
    raise MaxRetriesExceeded()
```

#### Quality Issues
```python
# Adjust quality thresholds
gateway = AIGateway(
    quality_threshold=0.8,  # Lower threshold
    max_retries=2
)
```