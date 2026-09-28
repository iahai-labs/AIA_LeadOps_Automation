from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_demo_ui_is_available() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "AIA LeadOps Automation" in response.text
    assert "Analyze lead" in response.text
