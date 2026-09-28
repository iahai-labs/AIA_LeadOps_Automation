import httpx

from app.integrations import n8n


class FailingClient:
    def __init__(self, *args, **kwargs) -> None:
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        return None

    def post(self, *args, **kwargs):
        request = httpx.Request("POST", "https://example.test/webhook")
        raise httpx.ConnectError("boom", request=request)


def test_webhook_retries_until_max_attempts(monkeypatch) -> None:
    monkeypatch.setattr(n8n.settings, "n8n_webhook_url", "https://example.test/webhook")
    monkeypatch.setattr(n8n.settings, "automation_max_attempts", 3)
    monkeypatch.setattr(n8n.settings, "automation_retry_backoff_seconds", 0)
    monkeypatch.setattr(n8n.httpx, "Client", FailingClient)

    result = n8n.send_lead_webhook({"event": "lead.created"})

    assert result.status == "failed"
    assert result.attempts == 3
    assert "boom" in result.last_error
