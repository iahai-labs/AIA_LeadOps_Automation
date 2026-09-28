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

## Database bootstrap

The production API container runs `python -m app.db.init_db` before Uvicorn starts.
For this portfolio deployment, the production database is created from a fresh volume,
so SQLAlchemy metadata initialization provides a deterministic first bootstrap.

Future schema changes should move to explicit versioned migrations before upgrading an
existing production database.

## Demo-safe mode

The public portfolio deployment is intended to run with:

- `DEMO_MODE=true`
- external AI disabled
- external n8n automation disabled
- per-IP POST rate limiting enabled

This keeps the demo interactive while avoiding uncontrolled API cost or automation abuse.

## Compose environment

Run production Compose with:

```text
docker compose --env-file .env.production -f docker-compose.prod.yml ...
```

The explicit `--env-file` is required because Compose uses `LEADOPS_DB_PASSWORD` while
rendering the database service configuration.

## Subpath support

`APP_ROOT_PATH=/leadops` ensures FastAPI-generated URLs such as OpenAPI documentation work
correctly behind the `/leadops/` reverse-proxy path.
