# AIA LeadOps Automation

[![CI](https://github.com/iahai-labs/AIA_LeadOps_Automation/actions/workflows/ci.yml/badge.svg)](https://github.com/iahai-labs/AIA_LeadOps_Automation/actions/workflows/ci.yml)

Production-minded AI lead operations and workflow automation for SMBs.

## Interactive demo UI

The repository now includes a lightweight, responsive demo interface at:

```text
http://127.0.0.1:8000/
```

The UI demonstrates the end-to-end workflow:

```text
Lead Intake
  -> AI Qualification
  -> Explainable Lead Scoring
  -> Recommended Action
  -> Follow-up Draft
  -> Automation Status
  -> Audit Trail
```

Built-in demo presets include:
- Hot lead
- Cold lead
- Duplicate submission

The UI is intentionally dependency-light and is served directly by FastAPI, keeping the
portfolio demo easy to run and deploy.

## Run locally

```bash
uvicorn app.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/
```

Interactive API documentation remains available at:

```text
http://127.0.0.1:8000/docs
```

## Engineering highlights

- FastAPI REST API
- PostgreSQL persistence
- deterministic duplicate detection
- structured AI qualification
- OpenAI-compatible provider abstraction
- safe AI fallback
- explainable 0–100 lead scoring
- hot / warm / cold lead tiers
- recommended next action
- follow-up draft generation
- n8n outbound webhook integration
- webhook secret support
- bounded retry policy
- automation status tracking
- audit trail
- responsive recruiter-friendly demo UI
- Docker Compose
- pytest
- Ruff
- GitHub Actions CI
- Dependabot and repository security controls

## Architecture

See [`docs/architecture.md`](docs/architecture.md).

## Portfolio case study

See [`docs/portfolio-case-study.md`](docs/portfolio-case-study.md).

## Release path

- `v0.1.0` — Lead intake foundation
- `v0.2.0` — Structured AI qualification
- `v0.3.0` — Explainable lead scoring
- `v0.4.0` — Automation integrations
- `v0.5.0` — Reliability, audit, and demo endpoints
- Demo UI — portfolio presentation layer
- `v1.0.0` — final live portfolio release after production-safe deployment
