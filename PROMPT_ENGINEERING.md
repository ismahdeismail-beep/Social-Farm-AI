# Prompt Engineering — Social Farm AI OS

## Overview

This document covers prompt engineering best practices for Social Farm AI OS, including template design, system prompts, and AI workflows.

## Prompt Structure

### 1. System Prompt

Sets the AI's behavior and context:

```python
system_prompt = """
You are Social Farm AI, an intelligent content operations assistant.

## Role
- Help users create high-quality social media content
- Provide data-driven insights and recommendations
- Assist with content strategy and planning

## Capabilities
- Content generation and editing
- Trend analysis and research
- Campaign planning and optimization
- Performance forecasting

## Guidelines
- Be helpful, accurate, and professional
- Use data to support recommendations
- Maintain brand consistency
- Follow platform best practices

## Output Format
- Use clear, concise language
- Structure responses with headers when appropriate
- Include actionable recommendations
- Provide confidence levels for predictions
"""
```

### 2. User Prompt

The actual request from the user:

```python
user_prompt = """
Create a social media post for Instagram about our new organic fertilizer product.

## Product Details
- Name: EcoGrow Organic Fertilizer
- Key Benefits: 100% organic, improves soil health, eco-friendly
- Target Audience: Organic farmers, home gardeners
- Tone: Professional yet approachable

## Requirements
- Include 3-5 relevant hashtags
- Suggest best posting time
- Include a call-to-action
- Keep under 2200 characters
"""
```

### 3. Context Window

Structured context for the AI:

```python
context = {
    "brand": {
        "name": "Social Farm AI",
        "industry": "Agriculture",
        "tone": "Professional, friendly, innovative"
    },
    "platform": {
        "name": "Instagram",
        "best_times": ["9 AM", "12 PM", "6 PM"],
        "character_limit": 2200,
        "hashtag_limit": 30
    },
    "audience": {
        "demographics": "Farmers, gardeners, 25-55 age range",
        "interests": ["organic farming", "sustainability", "agriculture"],
        "pain_points": ["soil degradation", "chemical fertilizers"]
    }
}
```

## Prompt Templates

### Content Generation

```python
CONTENT_GENERATION_PROMPT = """
Create {content_type} for {platform} about {topic}.

## Requirements
- Tone: {tone}
- Target Audience: {audience}
- Key Message: {key_message}
- Call-to-Action: {cta}

## Brand Guidelines
- Brand Voice: {brand_voice}
- Hashtags: {hashtags}
- Character Limit: {char_limit}

## Output Format
1. Main content
2. Hashtags
3. Best posting time
4. Engagement prediction
"""
```

### Research Analysis

```python
RESEARCH_ANALYSIS_PROMPT = """
Analyze the following research data and provide insights:

## Data
{research_data}

## Analysis Requirements
1. Identify key trends
2. Highlight opportunities
3. Provide actionable recommendations
4. Estimate confidence levels

## Output Format
- Executive Summary (2-3 sentences)
- Key Findings (bullet points)
- Opportunities (numbered list)
- Recommendations (prioritized)
- Confidence Score (0-100%)
"""
```

### Campaign Planning

```python
CAMPAIGN_PLANNING_PROMPT = """
Create a {campaign_type} campaign for {brand}.

## Campaign Details
- Duration: {duration}
- Budget: {budget}
- Platforms: {platforms}
- Goals: {goals}

## Audience
- Demographics: {demographics}
- Interests: {interests}
- Behaviors: {behaviors}

## Output Format
1. Campaign Overview
2. Content Strategy
3. Posting Schedule
4. Budget Allocation
5. KPIs and Metrics
6. Risk Assessment
"""
```

## Best Practices

### 1. Be Specific

```python
# ❌ Bad: Vague prompt
prompt = "Write a social media post"

# ✅ Good: Specific prompt
prompt = """
Write an Instagram post for EcoGrow Organic Fertilizer targeting home gardeners.

Key points to include:
- 100% organic ingredients
- Improves soil health
- Eco-friendly packaging
- 20% off first purchase

Tone: Friendly, encouraging
Length: Under 2200 characters
Include: 3-5 relevant hashtags
"""
```

### 2. Provide Context

```python
# ❌ Bad: No context
prompt = "Write a blog post about farming"

# ✅ Good: With context
prompt = """
Write a blog post for Social Farm AI's audience of modern farmers.

Context:
- Audience: Tech-savvy farmers interested in AI
- Goal: Educate about AI benefits in agriculture
- Tone: Professional but accessible
- Length: 800-1000 words

Include:
- Real-world examples
- Data points
- Actionable tips
- Internal links to our product
"""
```

### 3. Use Structured Output

```python
# ❌ Bad: Unstructured output
prompt = "Analyze this data"

# ✅ Good: Structured output
prompt = """
Analyze the following engagement data and provide insights.

## Data
{engagement_data}

## Output Format
### Executive Summary
[2-3 sentences]

### Key Findings
1. [Finding 1]
2. [Finding 2]
3. [Finding 3]

### Recommendations
1. [Recommendation 1] - Priority: High
2. [Recommendation 2] - Priority: Medium
3. [Recommendation 3] - Priority: Low

### Confidence Score
[0-100%]
"""
```

### 4. Include Examples

```python
# ❌ Bad: No examples
prompt = "Write a tweet about our product"

# ✅ Good: With examples
prompt = """
Write a tweet about our new EcoGrow fertilizer.

Example tweets:
1. "🌱 Boost your garden's health naturally with EcoGrow Organic Fertilizer! 100% organic, 100% effective. Shop now and save 20%! #OrganicGardening #SustainableFarming"
2. " tired of chemical fertilizers? Try EcoGrow! 🌿 Our organic formula improves soil health while being eco-friendly. Link in bio! #GreenAgriculture #FarmSmart"

Create a similar tweet that:
- Highlights a unique benefit
- Includes a call-to-action
- Uses 2-3 relevant hashtags
- Stays under 280 characters
"""
```

## AI Workflows

### Content Creation Workflow

```python
CONTENT_WORKFLOW = {
    "steps": [
        {
            "name": "research",
            "prompt": RESEARCH_PROMPT,
            "model": "gpt-4",
            "temperature": 0.3
        },
        {
            "name": "outline",
            "prompt": OUTLINE_PROMPT,
            "model": "gpt-4",
            "temperature": 0.5
        },
        {
            "name": "draft",
            "prompt": DRAFT_PROMPT,
            "model": "gpt-4-turbo",
            "temperature": 0.7
        },
        {
            "name": "edit",
            "prompt": EDIT_PROMPT,
            "model": "gpt-4",
            "temperature": 0.3
        },
        {
            "name": "optimize",
            "prompt": OPTIMIZE_PROMPT,
            "model": "gpt-3.5-turbo",
            "temperature": 0.5
        }
    ],
    "quality_checks": [
        "grammar",
        "brand_voice",
        "platform_guidelines",
        "engagement_prediction"
    ]
}
```

### Research Workflow

```python
RESEARCH_WORKFLOW = {
    "steps": [
        {
            "name": "data_collection",
            "prompt": COLLECTION_PROMPT,
            "model": "gpt-3.5-turbo",
            "temperature": 0.2
        },
        {
            "name": "analysis",
            "prompt": ANALYSIS_PROMPT,
            "model": "gpt-4",
            "temperature": 0.3
        },
        {
            "name": "insights",
            "prompt": INSIGHTS_PROMPT,
            "model": "gpt-4",
            "temperature": 0.5
        },
        {
            "name": "recommendations",
            "prompt": RECOMMENDATIONS_PROMPT,
            "model": "gpt-4",
            "temperature": 0.4
        }
    ],
    "validation": [
        "fact_check",
        "data_accuracy",
        "relevance_score"
    ]
}
```

## Prompt Optimization

### Temperature Settings

| Task Type | Temperature | Use Case |
|-----------|-------------|----------|
| Factual | 0.1-0.3 | Research, analysis |
| Creative | 0.7-0.9 | Content creation, brainstorming |
| Balanced | 0.4-0.6 | General tasks, planning |

### Token Management

```python
# Estimate token count
def estimate_tokens(text: str) -> int:
    return len(text) // 4  # Approximate

# Optimize prompt for token limit
def optimize_prompt(prompt: str, max_tokens: int = 4000) -> str:
    tokens = estimate_tokens(prompt)
    if tokens > max_tokens:
        # Truncate or summarize
        return truncate_prompt(prompt, max_tokens)
    return prompt
```

### Model Selection

```python
# Select model based on task
def select_model(task_type: str, quality: str) -> str:
    if task_type == "creative" and quality == "high":
        return "gpt-4-turbo"
    elif task_type == "factual":
        return "gpt-4"
    elif task_type == "simple":
        return "gpt-3.5-turbo"
    else:
        return "gpt-4"
```

## Quality Assurance

### Validation Checks

```python
VALIDATION_CHECKS = {
    "grammar": {
        "model": "gpt-3.5-turbo",
        "prompt": "Check grammar and spelling in: {text}",
        "threshold": 0.9
    },
    "brand_voice": {
        "model": "gpt-4",
        "prompt": "Evaluate brand voice consistency: {text} against {brand_guidelines}",
        "threshold": 0.8
    },
    "engagement": {
        "model": "gpt-4",
        "prompt": "Predict engagement potential: {text} on {platform}",
        "threshold": 0.7
    },
    "toxicity": {
        "model": "gpt-3.5-turbo",
        "prompt": "Check for toxicity in: {text}",
        "threshold": 0.95
    }
}
```

### A/B Testing

```python
# Test different prompts
async def ab_test_prompts(
    base_prompt: str,
    variants: List[str],
    test_cases: List[dict]
) -> dict:
    results = {}
    
    for variant in variants:
        variant_results = []
        for test_case in test_cases:
            response = await generate(
                prompt=variant.format(**test_case)
            )
            variant_results.append(response)
        
        results[variant] = analyze_results(variant_results)
    
    return select_best_variant(results)
```

## Version Control

### Prompt Versioning

```python
PROMPT_VERSIONS = {
    "content_generation": {
        "v1.0": {
            "system": "You are a content creator...",
            "user": "Create content about {topic}...",
            "created_at": "2026-01-15",
            "author": "team"
        },
        "v1.1": {
            "system": "You are an expert content creator...",
            "user": "Create engaging content about {topic}...",
            "created_at": "2026-01-20",
            "author": "team",
            "changes": "Improved tone instructions"
        }
    }
}
```

### Prompt Registry

```python
class PromptRegistry:
    def __init__(self):
        self.prompts = {}
    
    def register(self, name: str, version: str, prompt: dict):
        if name not in self.prompts:
            self.prompts[name] = {}
        self.prompts[name][version] = prompt
    
    def get(self, name: str, version: str = "latest") -> dict:
        if version == "latest":
            return list(self.prompts[name].values())[-1]
        return self.prompts[name][version]
```

## Monitoring

### Metrics

```python
PROMPT_METRICS = {
    "accuracy": "How accurate are the outputs?",
    "relevance": "How relevant to the request?",
    "engagement": "Predicted engagement score",
    "quality": "Overall quality rating",
    "cost": "Token usage and cost",
    "latency": "Response time"
}
```

### Logging

```python
# Log prompt usage
log_entry = {
    "prompt_id": "content_generation_v1.1",
    "model": "gpt-4",
    "tokens_used": 1500,
    "cost": 0.045,
    "latency_ms": 1200,
    "quality_score": 0.92,
    "user_id": "user_123",
    "timestamp": datetime.utcnow()
}
```

## Best Practices Summary

### Do's

✅ **Be specific** about requirements
✅ **Provide context** and examples
✅ **Use structured output** formats
✅ **Version control** prompts
✅ **Test and iterate** on prompts
✅ **Monitor quality** and costs

### Don'ts

❌ **Don't be vague** or ambiguous
❌ **Don't ignore** token limits
❌ **Don't skip** quality checks
❌ **Don't use** one prompt for all tasks
❌ **Don't forget** to log usage
❌ **Don't neglect** cost optimization

## Resources

- [OpenAI Prompt Engineering](https://platform.openai.com/docs/guides/prompt-engineering)
- [Anthropic Prompt Engineering](https://docs.anthropic.com/claude/docs/prompt-engineering)
- [Google Gemini Prompting](https://ai.google.dev/docs/prompting-intro)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)