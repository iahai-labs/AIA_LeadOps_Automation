# AIA LeadOps Automation

Production-minded AI lead operations and workflow automation for SMBs.

## Current release: v0.4.0 — Automation Integrations

### Implemented
- FastAPI lead intake API
- PostgreSQL persistence
- duplicate detection
- structured AI lead qualification
- provider abstraction for OpenAI-compatible APIs
- safe deterministic AI fallback
- explainable deterministic lead scoring
- hot / warm / cold lead tiers
- recommended next action
- deterministic follow-up draft generation
- outbound n8n webhook integration
- optional webhook secret header
- Telegram recommendation flag for hot leads
- integration status / attempt / error persistence
- pytest + Ruff
- GitHub Actions CI
- Dependabot
- Docker Compose

## Automation flow

```text
Lead API
  -> AI qualification
  -> deterministic scoring
  -> follow-up draft
  -> persist lead
  -> n8n webhook
  -> Telegram / CRM / email workflow
```

The application does not require n8n to accept leads. If no webhook is configured,
automation delivery is marked as `skipped`. If delivery fails, lead creation remains
successful and the integration result is stored for later inspection.

## Webhook payload

The n8n webhook receives:
- lead identity and message
- structured qualification
- explainable scoring
- recommended action
- follow-up draft
- `telegram_recommended=true` for hot leads

## Environment

```text
N8N_WEBHOOK_URL=https://your-n8n.example/webhook/leadops
N8N_WEBHOOK_SECRET=replace-with-a-secret
AUTOMATION_TIMEOUT_SECONDS=5
```

When a secret is configured it is sent as:

```text
X-AIA-Webhook-Secret: <secret>
```

Do not commit real secrets to Git.

## Roadmap

- v0.1.0 — Lead intake foundation ✅
- v0.2.0 — AI qualification ✅
- v0.3.0 — Explainable lead scoring ✅
- v0.4.0 — n8n / Telegram / follow-up automation ✅
- v0.5.0 — Reliability, audit and demo
- v1.0.0 — Portfolio release
