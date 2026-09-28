# AIA LeadOps Automation

[![CI](https://github.com/iahai-labs/AIA_LeadOps_Automation/actions/workflows/ci.yml/badge.svg)](https://github.com/iahai-labs/AIA_LeadOps_Automation/actions/workflows/ci.yml)

Production-minded AI lead operations and workflow automation for SMBs.

## Live demo

Production-safe public deployment target:

`https://ai.iradhd.ir/leadops/`

The public demo runs in a cost-safe mode:
- interactive lead processing remains available
- deterministic qualification fallback is used
- external AI calls are disabled
- external n8n delivery is disabled
- POST requests are rate limited

The codebase still supports real OpenAI-compatible AI providers and n8n automation when
enabled through private environment configuration.

## Workflow

```text
Lead Intake
  -> Qualification
  -> Explainable Scoring
  -> Recommended Action
  -> Follow-up Draft
  -> Persistence
  -> Automation Boundary
  -> Audit Trail
```

## Portfolio highlights

- FastAPI REST API
- PostgreSQL persistence
- deterministic duplicate detection
- structured AI qualification
- OpenAI-compatible provider abstraction
- safe fallback behavior
- explainable 0–100 lead scoring
- hot / warm / cold tiers
- follow-up generation
- n8n integration boundary
- bounded retry behavior
- automation state persistence
- audit trail
- responsive interactive demo UI
- demo-safe rate limiting
- Docker production deployment
- GitHub Actions CI
- pytest + Ruff
- Dependabot and repository security controls

## Local demo

```bash
uvicorn app.main:app --reload --port 8002
```

Open:

`http://127.0.0.1:8002/`

## API docs

Local:

`http://127.0.0.1:8002/docs`

Public deployment:

`https://ai.iradhd.ir/leadops/docs`

## Documentation

- [`docs/architecture.md`](docs/architecture.md)
- [`docs/portfolio-case-study.md`](docs/portfolio-case-study.md)
- [`docs/phase-8/DEPLOYMENT.md`](docs/phase-8/DEPLOYMENT.md)

## Release path

- `v0.1.0` — Lead intake foundation
- `v0.2.0` — Structured AI qualification
- `v0.3.0` — Explainable lead scoring
- `v0.4.0` — Automation integrations
- `v0.5.0` — Reliability, audit, and demo endpoints
- Demo UI — portfolio presentation layer
- Production-safe deployment — `/leadops/`
- `v1.0.0` — final portfolio release after live verification
