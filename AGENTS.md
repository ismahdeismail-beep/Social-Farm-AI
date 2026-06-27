# Multi-Agent System — Routing & Workflow

## Agent Assignments

| Agent | Model | Role |
|-------|-------|------|
| Orchestrator | `openai/gpt-5.5` | Master router, task analysis, result consolidation |
| Research | `google/gemini-2.5-pro` | Deep research, analysis, factual queries |
| Coding | `openrouter/deepseek/deepseek-chat-v3-0324` | Code generation, debugging, architecture |
| Review | `openai/gpt-5.5` | Code review, security audit, quality |
| Documentation | `google/gemini-2.5-pro` | Docs, guides, API documentation |
| Web Intelligence | `xai/grok-3` | Real-time web, scraping, news |
| Utility | `nvidia/llama-3.3-70b-instruct` | Fast tasks, calculations, formatting |

## Task Classification

### Route to CODING agent when:
- User asks to write/modify code
- Bug fixes, refactoring, new features
- Architecture decisions
- File creation/editing
- Shell commands, scripts, build systems
- Keywords: code, write, implement, fix, refactor, function, class, module, build

### Route to RESEARCH agent when:
- Factual questions, comparisons, analysis
- "What is...", "Compare...", "How does X work"
- Data gathering, literature review
- Technical explanations
- Keywords: research, analyze, explain, compare, evaluate, investigate

### Route to REVIEW agent when:
- User asks to review code
- Security audits
- Performance analysis
- Quality checks before deployment
- Keywords: review, audit, check, validate, security, performance

### Route to DOC agent when:
- Writing documentation, READMEs, guides
- API documentation
- Explanations of existing code
- Changelog, commit messages
- Keywords: document, docs, readme, guide, explain, comment

### Route to WEB agent when:
- Real-time information needed
- Web scraping, URL fetching
- Current events, news, trends
- External API queries
- Keywords: web, scrape, fetch, news, trending, current

### Route to UTILITY agent when:
- Quick calculations, conversions
- Simple text formatting
- Quick lookups
- Boilerplate generation
- Any fast, low-complexity task

## Collaboration Patterns

### Parallel Execution
For independent subtasks, dispatch multiple agents simultaneously:
```
Task → Orchestrator
  ├── Research Agent (parallel)
  ├── Coding Agent (parallel)
  └── Web Agent (parallel)
→ Consolidate results → Final answer
```

### Sequential Pipeline
For dependent tasks, chain agents:
```
Task → Research Agent (gather info)
  → Coding Agent (implement)
    → Review Agent (validate)
      → Doc Agent (document)
        → Final answer
```

### Expert Escalation
When an agent's output needs validation:
```
Coding Agent (implementation)
  → Review Agent (audit)
    → Orchestrator (final decision)
```

## Shared Memory

### Context Store
- Decisions and rationale stored per session
- Previous agent outputs cached for reuse
- Key findings persisted across turns

### Memory Triggers
Save to memory when:
- Architecture decisions are made
- Bug root cause identified
- Significant code changes committed
- Research findings summarized
- Configuration choices documented

## Automatic Model Selection Rules

1. **Default**: Use the model assigned to the routed agent
2. **Fallback**: If agent's model is unavailable, use `openai/gpt-5.5`
3. **Cost Optimization**: Use `nvidia/llama-3.3-70b-instruct` for simple tasks
4. **Quality Gate**: Critical code always goes through Review Agent
5. **Speed Priority**: Utility agent for anything under 100 tokens output

## Output Format

All agents return results in this format:
```
[AGENT_NAME] Result:
- Summary: One-line summary
- Details: Full response
- Confidence: High/Medium/Low
- Next Steps: If any follow-up needed
```