# Phase 8 — Production-Safe Deployment

## Target

Public demo path:

`https://ai.iradhd.ir/leadops/`

The existing portfolio root remains unchanged.

## Production topology

```text
Internet
  -> Cloudflare / TLS
  -> central nginx-proxy
  -> /leadops/
  -> 127.0.0.1:8002
  -> LeadOps API container
  -> PostgreSQL container
```

The application port is bound only to loopback and is not exposed directly to the public
internet.

## Demo-safe mode

The public portfolio deployment is intended to run with:

- `DEMO_MODE=true`
- external AI disabled
- external n8n automation disabled
- per-IP POST rate limiting enabled

This keeps the demo interactive while avoiding uncontrolled API cost or automation abuse.

The production-capable AI and n8n integration remain in the codebase and can be enabled
through environment configuration for a private/customer deployment.

## Subpath support

`APP_ROOT_PATH=/leadops` ensures FastAPI-generated URLs such as OpenAPI documentation work
correctly behind the `/leadops/` reverse-proxy path.

## Files

- `docker-compose.prod.yml` — production container topology
- `.env.production.example` — production environment template
- `deploy/nginx/leadops.location.conf` — Nginx location block for the existing portfolio
  server
