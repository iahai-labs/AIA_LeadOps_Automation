# AIA LeadOps Automation

Production-minded AI lead operations and workflow automation for SMBs.

## Current release: v0.2.0 — AI Qualification

### Implemented
- FastAPI lead intake API
- PostgreSQL persistence
- duplicate detection
- structured AI lead qualification
- provider abstraction for OpenAI-compatible APIs
- Groq-compatible default endpoint
- safe deterministic fallback when AI is unavailable
- normalized service type, intent, urgency, summary, and language
- pytest + Ruff
- GitHub Actions CI
- Dependabot
- Docker Compose

## AI qualification output

A lead can be enriched into structured data such as:

```json
{
  "service_type": "website_development",
  "intent": "high",
  "urgency": "high",
  "summary": "Dental clinic needs a website next month.",
  "language": "en",
  "source": "ai"
}
```

If the AI provider is unavailable or no API key is configured, the system uses a safe
fallback and marks the qualification source as `fallback`.

## API

`POST /api/v1/leads`

```json
{
  "name": "Sarah Miller",
  "email": "sarah@example.com",
  "company": "Bright Dental",
  "message": "We need a new website for our dental clinic and want to launch next month."
}
```

## AI configuration

Copy `.env.example` to `.env` and set:

```text
AI_API_KEY=your_key
AI_BASE_URL=https://api.groq.com/openai/v1
AI_MODEL=llama-3.1-8b-instant
```

The provider layer is intentionally OpenAI-compatible so another compatible provider
can be introduced without rewriting the qualification service.

## Roadmap

- v0.1.0 — Lead intake foundation ✅
- v0.2.0 — AI qualification ✅
- v0.3.0 — Lead scoring
- v0.4.0 — n8n / Telegram / follow-up automation
- v0.5.0 — Reliability, audit and demo
- v1.0.0 — Portfolio release
