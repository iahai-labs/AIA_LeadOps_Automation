# AIA LeadOps Automation

Production-minded lead workflow automation for SMBs.

## Phase 1 — Lead Intake Foundation

- FastAPI lead intake API
- PostgreSQL persistence
- duplicate detection
- validation
- repository/service separation
- health endpoint
- pytest + Ruff
- GitHub Actions CI
- Dependabot
- Docker Compose

## API

`POST /api/v1/leads`

```json
{
  "name": "Sarah Miller",
  "email": "sarah@example.com",
  "company": "Bright Dental",
  "message": "We need a new website and want to launch next month."
}
```

Response:

```json
{
  "id": 1,
  "status": "received",
  "duplicate": false
}
```

## Roadmap

- v0.1.0 — Lead intake foundation
- v0.2.0 — AI qualification
- v0.3.0 — Lead scoring
- v0.4.0 — n8n / Telegram / follow-up automation
- v0.5.0 — Reliability, audit and demo
- v1.0.0 — Portfolio release
