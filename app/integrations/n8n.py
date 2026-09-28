from __future__ import annotations

import time
from dataclasses import dataclass

import httpx

from app.core.config import settings


@dataclass(frozen=True)
class WebhookResult:
    status: str
    attempts: int
    last_error: str = ""


def send_lead_webhook(payload: dict[str, object]) -> WebhookResult:
    if not settings.n8n_webhook_url:
        return WebhookResult(status="skipped", attempts=0)

    headers = {"Content-Type": "application/json"}
    if settings.n8n_webhook_secret:
        headers["X-AIA-Webhook-Secret"] = settings.n8n_webhook_secret

    last_error = ""
    max_attempts = max(1, settings.automation_max_attempts)

    for attempt in range(1, max_attempts + 1):
        try:
            with httpx.Client(timeout=settings.automation_timeout_seconds) as client:
                response = client.post(
                    settings.n8n_webhook_url,
                    json=payload,
                    headers=headers,
                )
                response.raise_for_status()
            return WebhookResult(status="sent", attempts=attempt)
        except httpx.HTTPError as exc:
            last_error = str(exc)[:500]
            if attempt < max_attempts:
                time.sleep(settings.automation_retry_backoff_seconds)

    return WebhookResult(
        status="failed",
        attempts=max_attempts,
        last_error=last_error,
    )
