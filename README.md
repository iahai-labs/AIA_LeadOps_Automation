# AIA LeadOps Automation

Production-minded AI lead operations and workflow automation for SMBs.

## Current release: v0.5.0 — Reliability, Audit & Demo

### Implemented
- FastAPI lead intake API
- PostgreSQL persistence
- duplicate detection
- structured AI qualification
- safe AI fallback
- explainable deterministic lead scoring
- follow-up draft generation
- outbound n8n webhook integration
- bounded webhook retry policy
- automation status / attempts / error persistence
- audit trail for lead and automation events
- lead detail endpoint
- lead audit endpoint
- pytest + Ruff
- GitHub Actions CI
- Dependabot
- Docker Compose

## Reliability behavior

Webhook delivery is intentionally non-blocking for the business flow:
- lead creation succeeds even if n8n is unavailable
- delivery is retried up to a bounded maximum
- final automation state is persisted
- errors are stored for diagnosis
- audit events record what happened

## Demo API

### Create lead

`POST /api/v1/leads`

### Inspect lead

`GET /api/v1/leads/{lead_id}`

### Inspect audit trail

`GET /api/v1/leads/{lead_id}/audit`

## Suggested demo scenarios

### 1. Hot lead
Use a detailed, urgent request with a clear timeline.

Expected:
- high qualification signals
- hot score tier
- urgent recommended action
- Telegram recommendation flag
- follow-up draft
- audit events

### 2. Low-signal lead
Use a short price inquiry with no timeline.

Expected:
- lower score
- cold tier
- nurture follow-up recommendation

### 3. Duplicate lead
Submit the same payload twice.

Expected:
- same lead ID
- `duplicate=true`
- duplicate audit event

### 4. n8n unavailable
Configure an unreachable webhook.

Expected:
- lead still created
- bounded retries
- automation status `failed`
- attempts and error persisted
- audit event records failure

## Roadmap

- v0.1.0 — Lead intake foundation ✅
- v0.2.0 — AI qualification ✅
- v0.3.0 — Explainable lead scoring ✅
- v0.4.0 — Automation integrations ✅
- v0.5.0 — Reliability, audit and demo ✅
- v1.0.0 — Portfolio hardening and release
