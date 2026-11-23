from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from pydantic import SecretStr

from mohsen_core.config import settings
from mohsen_core.main import app


@pytest.fixture()
def client(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(settings, "database_path", str(tmp_path / "mohsen-test.sqlite3"))
    monkeypatch.setattr(settings, "core_api_token", SecretStr("test-owner-token"))
    return TestClient(app), {"Authorization": "Bearer test-owner-token"}


def test_task_lifecycle(client):
    api, headers = client
    created = api.post(
        "/api/v1/tasks",
        headers=headers,
        json={"title": "Review lecture"},
    )
    assert created.status_code == 201
    task_id = created.json()["id"]

    listed = api.get("/api/v1/tasks?status=open", headers=headers)
    assert listed.status_code == 200
    assert listed.json()["count"] == 1

    completed = api.post(f"/api/v1/tasks/{task_id}/complete", headers=headers)
    assert completed.status_code == 200
    assert completed.json()["status"] == "completed"


def test_notes_can_be_saved_and_searched(client):
    api, headers = client
    saved = api.post(
        "/api/v1/notes",
        headers=headers,
        json={"title": "Project idea", "content": "Build a bilingual assistant"},
    )
    assert saved.status_code == 201

    results = api.get("/api/v1/notes?q=bilingual", headers=headers)
    assert results.status_code == 200
    assert results.json()["count"] == 1
    assert results.json()["items"][0]["title"] == "Project idea"


def test_arabic_assistant_command_creates_task(client):
    api, headers = client
    response = api.post(
        "/api/v1/assistant/message",
        headers=headers,
        json={"message": "أضف مهمة: مراجعة المحاضرة"},
    )
    assert response.status_code == 200
    assert response.json()["action"] == "task_created"


def test_free_form_message_does_not_fake_model_response(client):
    api, headers = client
    response = api.post(
        "/api/v1/assistant/message",
        headers=headers,
        json={"message": "Explain quantum mechanics"},
    )
    assert response.status_code == 503
    assert response.json()["mode"] == "model_unavailable"


def test_protected_endpoints_reject_missing_token(client):
    api, _ = client
    response = api.get("/api/v1/tasks")
    assert response.status_code == 401
