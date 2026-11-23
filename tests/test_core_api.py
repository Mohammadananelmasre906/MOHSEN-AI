from fastapi.testclient import TestClient
from mohsen_core.main import app


def test_health_reports_model_not_ready():
    response = TestClient(app).get("/health")
    assert response.status_code == 200
    assert response.json()["model_ready"] is False


def test_chat_endpoint_does_not_fake_an_answer():
    response = TestClient(app).post(
        "/api/v1/chat",
        headers={"Authorization": "Bearer example-token"},
        json={"message": "Hello"},
    )
    assert response.status_code == 503
    assert response.json()["detail"] == "Core API token is not configured"
