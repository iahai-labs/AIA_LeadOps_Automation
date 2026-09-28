# AIA LeadOps Automation

Production-minded AI lead operations and workflow automation for SMBs.

## Current release: v0.3.0 — Explainable Lead Scoring

### Implemented
- FastAPI lead intake API
- PostgreSQL persistence
- duplicate detection
- structured AI lead qualification
- provider abstraction for OpenAI-compatible APIs
- safe deterministic fallback when AI is unavailable
- explainable deterministic lead scoring
- hot / warm / cold lead tiers
- recommended next action per lead
- persisted scoring reasons for auditability
- pytest + Ruff
- GitHub Actions CI
- Dependabot
- Docker Compose

## Example qualification and scoring

```json
{
  "qualification": {
    "service_type": "website_development",
    "intent": "high",
    "urgency": "high",
    "summary": "Dental clinic needs a website next month.",
    "language": "en",
    "source": "ai"
  },
  "scoring": {
    "score": 100,
    "tier": "hot",
    "recommended_action": "Contact within 4 hours",
    "reasons": [
      "Intent 'high' contributed 40 points",
      "Urgency 'high' contributed 25 points",
      "Recognized service need contributed 15 points",
      "Company information contributed 5 points",
      "Detailed lead message contributed 5 points",
      "Explicit timeline signal contributed 10 points"
    ]
  }
}
```

## Why scoring is deterministic

The LLM extracts structured lead signals, but the business score is calculated by explicit
rules. This keeps the score explainable, testable, and auditable instead of asking the
model to invent an opaque number.

Current scoring signals:
- intent
- urgency
- recognized service need
- company information
- message quality
- explicit timeline signals

Scores are capped at 100.

### Tiers

- `hot` — score 75–100 — contact within 4 hours
- `warm` — score 45–74 — contact within 1 business day
- `cold` — score 0–44 — automated nurture follow-up

## Roadmap

- v0.1.0 — Lead intake foundation ✅
- v0.2.0 — AI qualification ✅
- v0.3.0 — Explainable lead scoring ✅
- v0.4.0 — n8n / Telegram / follow-up automation
- v0.5.0 — Reliability, audit and demo
- v1.0.0 — Portfolio release
