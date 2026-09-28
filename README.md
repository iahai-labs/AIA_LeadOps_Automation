# AIA LeadOps Automation

[![CI](https://github.com/iahai-labs/AIA_LeadOps_Automation/actions/workflows/ci.yml/badge.svg)](https://github.com/iahai-labs/AIA_LeadOps_Automation/actions/workflows/ci.yml)

Production-minded AI lead operations and workflow automation for SMBs.

AIA LeadOps turns an inbound lead into a structured, explainable, and automation-ready
business workflow:

```text
Lead Intake
  -> AI Qualification
  -> Explainable Lead Scoring
  -> Follow-up Draft
  -> Persistence
  -> n8n Webhook
  -> Telegram / CRM / Email Workflow
  -> Audit Trail
```

## Why this project exists

Many small businesses capture leads through website forms but still rely on manual review,
manual prioritization, and inconsistent follow-up.

This project demonstrates how AI can be used inside a deterministic business workflow
without making the workflow itself opaque or fragile.

## Key engineering decisions

### AI extracts signals; business rules own the score

The LLM produces structured fields such as service type, intent, urgency, summary, and
language. The actual lead score is calculated by explicit, testable rules.

That makes the result explainable and auditable.

### AI failure does not break lead intake

If the configured AI provider is unavailable or an API key is missing, the application
uses a safe deterministic fallback and records the qualification source.

### Automation failure does not lose the lead

Webhook delivery happens after the lead is persisted. n8n failures use bounded retries,
and the final automation state, attempts, and error are stored.

### Duplicate submissions are idempotent

A deterministic fingerprint prevents the same lead payload from creating duplicate
business records.

## Features

- FastAPI REST API
- PostgreSQL persistence
- SQLAlchemy data layer
- Pydantic input validation
- deterministic duplicate detection
- structured AI qualification
- OpenAI-compatible provider abstraction
- Groq-compatible default configuration
- safe AI fallback
- explainable 0–100 lead scoring
- hot / warm / cold lead tiers
- recommended next action
- deterministic follow-up draft
- n8n outbound webhook
- webhook secret support
- Telegram recommendation flag for hot leads
- bounded retry policy
- automation status tracking
- audit trail
- lead detail and audit endpoints
- Docker Compose
- pytest
- Ruff
- GitHub Actions CI
- Dependabot and repository security controls

## Example result

```json
{
  "id": 42,
  "status": "received",
  "duplicate": false,
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
  },
  "automation": {
    "status": "sent",
    "attempts": 1,
    "followup_draft": "Hi Sarah, ...",
    "last_error": null
  }
}
```

## API

### Create a lead

`POST /api/v1/leads`

### Inspect a lead

`GET /api/v1/leads/{lead_id}`

### Inspect the audit trail

`GET /api/v1/leads/{lead_id}/audit`

### Health

`GET /health`

Interactive API documentation is available at `/docs`.

## Local quality gate

```bash
python -m ruff check .
python -m pytest -q
```

The same checks run automatically in GitHub Actions for pushes and pull requests.

## Environment

Copy `.env.example` to `.env` and configure values as needed.

Never commit real API keys, webhook secrets, or production credentials.

## Demo scenarios

1. **Hot lead** — clear service request + urgency + timeline
2. **Cold lead** — low-signal price inquiry
3. **Duplicate lead** — identical payload submitted twice
4. **AI unavailable** — deterministic fallback
5. **n8n unavailable** — lead persists, retry is bounded, failure is audited

See [`docs/architecture.md`](docs/architecture.md) for the system design and
[`docs/portfolio-case-study.md`](docs/portfolio-case-study.md) for the engineering case study.

## Release history

- `v0.1.0` — Lead intake foundation
- `v0.2.0` — Structured AI qualification
- `v0.3.0` — Explainable lead scoring
- `v0.4.0` — Automation integrations
- `v0.5.0` — Reliability, audit, and demo endpoints
- `v1.0.0` — Portfolio-ready release
