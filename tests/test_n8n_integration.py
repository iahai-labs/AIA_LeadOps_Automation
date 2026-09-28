from app.integrations import n8n


def test_webhook_is_skipped_when_not_configured(monkeypatch) -> None:
    monkeypatch.setattr(n8n.settings, "n8n_webhook_url", None)

    result = n8n.send_lead_webhook({"event": "lead.created"})

    assert result.status == "skipped"
    assert result.attempts == 0
    assert result.last_error == ""
