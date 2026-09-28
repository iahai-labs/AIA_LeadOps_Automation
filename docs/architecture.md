# Architecture

## System flow

```text
Client / Website Form
        |
        v
FastAPI Lead Intake
        |
        +--> Validation
        |
        +--> Duplicate Fingerprint Check
        |
        +--> AI Qualification
        |      |
        |      +--> OpenAI-compatible Provider
        |      +--> Safe Fallback
        |
        +--> Deterministic Lead Scoring
        |
        +--> Follow-up Draft
        |
        +--> PostgreSQL Persistence
        |
        +--> Audit Event
        |
        +--> n8n Webhook
               |
               +--> Telegram
               +--> CRM
               +--> Email / Follow-up Workflow
```

## Boundaries

### API layer
Receives and validates HTTP requests and exposes lead and audit endpoints.

### Service layer
Owns business behavior:
- qualification orchestration
- scoring
- follow-up generation
- automation dispatch
- audit recording

### Repository layer
Owns persistence queries and updates.

### Integration layer
Contains external provider boundaries such as:
- LLM provider
- n8n webhook

This keeps external dependencies replaceable without rewriting business logic.

## Reliability

The core business path is designed so that:
- AI failure does not reject a valid lead
- webhook failure does not lose a lead
- retries are bounded
- final automation state is persisted
- important events are auditable
- duplicate submissions resolve to the existing lead

## Security posture

The repository avoids committing secrets and provides environment-based configuration.
Webhook authentication can use a shared secret header. GitHub CI, Dependabot, security
policy, dependency monitoring, and secret scanning are part of the repository workflow.

## Testing strategy

Tests cover:
- health endpoint
- lead creation
- duplicate detection
- AI normalization
- AI fallback
- deterministic scoring
- score boundaries
- follow-up generation
- webhook payloads
- unconfigured webhook behavior
- retry failure behavior
- audit creation
- lead detail retrieval
- API detail and audit endpoints
