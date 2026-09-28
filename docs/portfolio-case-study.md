# Portfolio Case Study

## Problem

SMBs often collect leads through forms but still process them manually. That creates
slow response times, inconsistent prioritization, and weak visibility into what happened
after a lead arrived.

## Constraints

The system needed to:
- use AI without depending on AI for core reliability
- remain explainable to business users
- avoid losing leads when an integration fails
- support external automation tools such as n8n
- be testable without calling paid external services
- remain small enough to understand as a portfolio project

## Decisions

### Structured qualification instead of free-form chat
AI is used to extract bounded business signals rather than to control the whole workflow.

### Deterministic scoring
Lead scoring is explicit and testable. The model does not invent an opaque score.

### Safe fallback
Provider failure falls back to deterministic behavior so valid leads still enter the system.

### Persist before automation
The lead is committed before external workflow delivery. Integration failure therefore
does not cause business-data loss.

### Audit trail
Lead creation, duplicate detection, and automation outcomes are recorded as events.

### Provider and integration boundaries
External dependencies are isolated behind dedicated modules so they can be replaced.

## Result

The final workflow demonstrates:
- production-minded API design
- AI integration
- deterministic business rules
- failure handling
- workflow automation
- persistence
- auditability
- automated testing
- CI and repository security practices

## Skills demonstrated

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- REST APIs
- LLM integrations
- structured AI output
- workflow automation
- n8n integration
- retry / failure handling
- audit design
- Docker
- pytest
- Ruff
- GitHub Actions
- dependency and repository security practices

## Interview discussion points

Useful questions this project can answer in an interview:

- Why should AI qualification and lead scoring be separate?
- How do you prevent an LLM outage from breaking lead intake?
- Why persist before calling n8n?
- How do bounded retries differ from infinite retries?
- How does duplicate detection work?
- Why store scoring reasons?
- How would the webhook integration be made asynchronous at larger scale?
- How would you add a CRM adapter without rewriting business logic?
