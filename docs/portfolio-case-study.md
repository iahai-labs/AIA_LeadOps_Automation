# AIA LeadOps Automation — Portfolio Case Study

## Problem

Small and medium businesses often receive inbound leads through forms, messages, or lightweight CRM workflows, but the operational follow-up is inconsistent. Leads may be duplicated, poorly qualified, manually prioritized, or lost before a timely response is sent.

## Constraints

The system needed to demonstrate practical AI automation without turning core business decisions into opaque LLM output.

Key constraints included:

- lead intake must continue even when AI is unavailable
- automation failures must not lose customer data
- duplicate submissions should be handled deterministically
- prioritization should be explainable
- external AI and automation integrations should remain replaceable
- the public portfolio demo should not create uncontrolled API cost or automation abuse
- the live application should coexist with the existing portfolio site without replacing its root

## Decisions

### Structured qualification

Lead messages are converted into structured fields such as service type, intent, urgency, language, and summary through an OpenAI-compatible provider abstraction.

### Deterministic scoring

The LLM does not own the final lead score. Transparent business rules convert structured signals into a 0–100 score, a hot/warm/cold tier, reasons, and a recommended action.

### Failure isolation

AI fallback, database persistence, and outbound automation are separated so one failed dependency does not destroy the entire workflow.

### Auditable workflow

Important lifecycle events are persisted as audit events, including lead creation, duplicate detection, and automation outcomes.

### Production-safe public demo

The public deployment runs with external AI and n8n execution disabled while retaining the production integration code. Rate limiting reduces abuse risk. The service is bound to VPS loopback and exposed through the existing Nginx portfolio reverse proxy.

## Result

A deployed, interactive LeadOps system is available at:

`https://ai.iradhd.ir/leadops/`

A visitor can submit a sample lead and observe:

- structured qualification
- explainable lead scoring
- tier assignment
- recommended response timing
- follow-up draft generation
- automation state
- audit history
- duplicate detection

The result demonstrates an end-to-end business automation system rather than a standalone chatbot or static prototype.
