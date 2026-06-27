# AI System: AI_AGENTS

## Purpose
AI Agents are the specialized workers of the platform, encapsulating the behavior and skills necessary to perform specific tasks within the content operations lifecycle.

## Agent List

| Agent | Mission | Primary Skill |
| :--- | :--- | :--- |
| **Trend Agent** | Identify emerging opportunities | Web scraping, Clustering |
| **Research Agent** | Gather deep context | Fact extraction, Summarization |
| **Script Agent** | Create platform-specific scripts | Creative writing, Storytelling |
| **Media Agent** | Produce multimedia assets | Prompt optimization, FFmpeg |
| **Pub Agent** | Manage content distribution | Scheduling, API interaction |

## Agent Structure
Every agent is defined by:
- **Mission:** Clear goal.
- **Inputs:** Schema defining expected input data.
- **Outputs:** Schema defining expected output data.
- **Skills (Tools):** Authorized functions the agent can call.
- **Dependencies:** Other agents required for task completion.
