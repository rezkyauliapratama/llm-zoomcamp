# Module 03 — AI Orchestration with Kestra

Homework submission for [LLM Zoomcamp 2026 Cohort](https://github.com/DataTalksClub/llm-zoomcamp/tree/main/cohorts/2026/03-orchestration).

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Importing Flows](#importing-flows)
- [Homework Answers](#homework-answers)
  - [Q1 — Context Engineering](#q1--context-engineering)
  - [Q2 — RAG vs No RAG](#q2--rag-vs-no-rag)
  - [Q3 — Token Usage: Short Summary](#q3--token-usage-short-summary)
  - [Q4 — Token Usage: Long Summary](#q4--token-usage-long-summary)
  - [Q5 — Modifying a Flow](#q5--modifying-a-flow)
  - [Q6 — Best Practices](#q6--best-practices)

---

## Prerequisites

| Requirement | Details |
|-------------|---------|
| **Docker** | Docker Desktop or Docker Compose v2 |
| **Gemini API Key** | From [Google AI Studio](https://aistudio.google.com/app/apikey) — required for flows 1, 2, 4, 5, 6 and AI Copilot |
| **OpenRouter API Key** | From [OpenRouter](https://openrouter.ai/keys) — required for flow 3 |
| **Tavily API Key** | From [Tavily](https://tavily.com/) — required for web search in flows 3, 5, 6 |

> **Provider note:** Flows 1, 2, 4, 5, 6 use Gemini directly. Flow 3 (RAG with websearch) uses Kestra's native OpenRouter provider (`io.kestra.plugin.ai.provider.OpenRouter`). The AI Copilot built into Kestra's UI also requires a direct Gemini API key.

---

## Quick Start

### 1. Configure environment

```bash
cp .env.template .env
# Edit .env with your API keys
```

### 2. Start Kestra

```bash
# Source the env vars and encode secrets as base64
export GEMINI_API_KEY="your-key"
export OPENROUTER_API_KEY="your-key"
export TAVILY_API_KEY="your-key"
export SECRET_GEMINI_API_KEY=$(echo -n "$GEMINI_API_KEY" | base64)
export SECRET_OPENROUTER_API_KEY=$(echo -n "$OPENROUTER_API_KEY" | base64)
export SECRET_TAVILY_API_KEY=$(echo -n "$TAVILY_API_KEY" | base64)

# Start Kestra
docker compose up -d
```

### 3. Access Kestra UI

Open [http://localhost:8080](http://localhost:8080) and log in with:
- **Username:** `admin@kestra.io`
- **Password:** `Admin1234!`

### 4. Import flows

Via API:

```bash
for flow in flows/*.yaml; do
  curl -X POST -u 'admin@kestra.io:Admin1234!' \
    http://localhost:8080/api/v1/flows/import \
    -F "fileUpload=@$flow"
done
```

Or via UI: Navigate to **Flows** → **Import** and select each file from the `flows/` directory.

### 5. Shut down

```bash
docker compose down
```

---

## Flow Reference

| # | File | Provider | Description |
|---|------|----------|-------------|
| 1 | `1_chat_without_rag.yaml` | Gemini | Query Kestra 1.1 features without RAG |
| 2 | `2_chat_with_rag.yaml` | Gemini | Same query with RAG (ingest + retrieve) |
| 3 | `3_rag_with_websearch.yaml` | **OpenRouter** | RAG with live web search via Tavily |
| 4 | `4_simple_agent.yaml` | Gemini | Basic AI agent with controllable summary |
| 5 | `5_web_research_agent.yaml` | Gemini | Autonomous web research agent |
| 6 | `6_multi_agent_research.yaml` | Gemini | Multi-agent system for company research |

> **Flow 3 differs from the original course:** It uses Kestra's native `OpenRouter` provider instead of the original OpenAI provider. The provider type is `io.kestra.plugin.ai.provider.OpenRouter` with `baseUrl: https://openrouter.ai/api/v1` and model `openai/gpt-4o-mini`.

---

## Homework Answers

### Q1 — Context Engineering

**Experiment:** Try the same prompt in ChatGPT vs Kestra's AI Copilot:

> "Create a Kestra flow that loads NYC taxi data from CSV to BigQuery"

**Answer: AI Copilot has access to current Kestra plugin documentation.**

**Why:** ChatGPT relies on its training data, which has a knowledge cutoff. It may generate flows with:
- Outdated plugin syntax (e.g., old task types that have been renamed)
- Incorrect property names (e.g., properties that don't exist in current versions)
- Hallucinated features (e.g., tasks, triggers, or properties that never existed)

Kestra's AI Copilot solves this by injecting current plugin documentation, valid property names, and best practices directly into the model's context — so every generated flow uses correct, up-to-date syntax.

**Concept tested:** Context engineering — AI is only as good as the context provided.

---

### Q2 — RAG vs No RAG

**Experiment:** Run both `1_chat_without_rag.yaml` and `2_chat_with_rag.yaml` in Kestra UI. Compare the execution logs.

**Answer: Vague, generic, or fabricated — the model guesses from training data.**

**Why:** Without RAG, the LLM has no access to the actual Kestra 1.1 release notes. It must rely entirely on its training data, which may be outdated or incomplete. The response will likely contain:
- Generic descriptions that could apply to any release
- Features that were actually released in different versions
- Confidently stated but incorrect information (hallucination)

With RAG (Flow 2), the model retrieves the actual release blog post from GitHub, creates embeddings, and generates a response grounded in real, verifiable facts.

**Concept tested:** RAG grounds LLM responses in real data, eliminating hallucination for factual queries.

---

### Q3 — Token Usage: Short Summary

**Experiment:** Run `4_simple_agent.yaml` with `summary_length = short` (leave other inputs as defaults). Open the execution logs and find the token usage logged by the `log_token_usage` task.

**Answer: 60–100 tokens (approximate).**

Look for the `multilingual_agent` output token count in the logs:

```
Multilingual Agent:
- Input tokens: ...
- Output tokens: 60-100  ← this value
- Total tokens: ...
```

**Why short range?** A "short" summary (1–2 sentences) naturally produces a compact output. The actual value varies depending on the input text and model response, but stays within this range.

**Concept tested:** Understanding token consumption for cost monitoring and optimization.

---

### Q4 — Token Usage: Long Summary

**Experiment:** Run `4_simple_agent.yaml` again with `summary_length = long`. Compare the `multilingual_agent` output token count to your result from Q3.

**Answer: 2–5× more (approximate).**

**Why this range?** A "long" summary requests 1–3 paragraphs, which naturally expands the output by 2–5× compared to the 1–2 sentence short version. The exact multiplier depends on the input text complexity.

**Concept tested:** How prompt complexity and output length affect token usage and cost.

---

### Q5 — Modifying a Flow

**Experiment:**
1. Open `4_simple_agent.yaml` in the Kestra flow editor
2. Find the `english_brevity` task
3. Change its prompt from asking for exactly **1 sentence** to exactly **3 sentences**
4. Save the flow, then run it with `summary_length = long`
5. Compare the `english_brevity` output token count to the original 1-sentence version (also with `summary_length = long`)

**Answer: 2–4× more (approximate).**

**Why:** Changing the constraint from 1 sentence to 3 sentences directly increases the output length of the `english_brevity` task. The token count scales roughly linearly with the number of sentences requested.

**Concept tested:** How task parameters influence token consumption and the importance of setting appropriate constraints.

---

### Q6 — Best Practices

**Question:** For production workflows requiring deterministic, repeatable results with strict compliance requirements (e.g., financial reporting, regulated industries), which approach is most appropriate?

**Answer: Use traditional task-based workflows for predictability and auditability.**

**Why:**

| Approach | Best For |
|----------|----------|
| **Traditional workflows** | Fixed, repeatable ETL pipelines, compliance-heavy processes, financial reporting |
| **AI Copilot** | Creating and editing flows faster |
| **RAG** | Answering questions grounded in your data |
| **AI Agents** | Research and analysis tasks requiring adaptation |
| **Multi-agent systems** | Complex, multi-step objectives with specialized roles |

In regulated industries (banking, healthcare, finance), every step must be auditable, predictable, and deterministic. AI agents are excellent for supporting tasks like research and summarization, but core compliance logic must remain in traditional, auditable workflows.

**Concept tested:** Understanding when to use each approach (traditional workflows, AI Copilot, RAG, AI Agents, multi-agent systems) based on requirements for determinism, compliance, and cost.

---

## Submission

Submit your answers at:
[https://courses.datatalks.club/llm-zoomcamp-2026/homework/hw3](https://courses.datatalks.club/llm-zoomcamp-2026/homework/hw3)

Make sure to include a link to your GitHub repository containing the flow files and this README.
