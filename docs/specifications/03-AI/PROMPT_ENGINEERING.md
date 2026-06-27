# AI System: PROMPT_ENGINEERING

## Purpose
Standardizes how we construct, refine, and validate prompts.

## Principles
1. **Clarity:** Explicit instructions.
2. **Context:** Include necessary brand/project info.
3. **Few-Shot:** Always provide examples for complex tasks.
4. **Structured Output:** Enforce JSON/XML output where programmatic handling is required.
5. **Chain-of-Thought:** Force the model to reason before outputting.

## Quality Metrics
- **Token Efficiency:** Minimizing context while maximizing relevance.
- **Hallucination Rate:** Frequency of false information.
- **Task Success Rate:** Percentage of outputs passing automated validation.

## Tools
- Prompt testing suite in `scripts/prompt-tester`.
- Version history of prompt outputs in `audit_logs`.
