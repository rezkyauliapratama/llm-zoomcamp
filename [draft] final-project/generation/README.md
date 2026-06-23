# Generation Layer

LLM generation with regulatory context, citation enforcement, and two system prompt variants for evaluation.

## System Prompts

### V1 — Strict Citation (Baseline)
Instructs LLM to answer **only** from provided context. Rejects questions if context is insufficient. Every claim must cite `[Sumber: {document}, {pasal}]`.

### V2 — Structured Response
Adds numbered-point format with explicit per-point citations. Ends with consolidated reference list. Same citation rule as V1.

## LLM Options

| Provider | Notes |
|----------|-------|
| OpenAI GPT-4o | Highest quality; citation-following |
| Groq (llama3-70b) | Fast inference; low latency |
| Ollama (local) | Air-gapped; no API cost |
| AWS Bedrock | Enterprise; Anthropic Claude or Amazon Titan |

Set in `.env` via `OPENAI_API_KEY` or `GROQ_API_KEY`.
