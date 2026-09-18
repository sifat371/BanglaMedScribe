from fastapi.testclient import TestClient

from banglamedscribe.api import app


def test_health_endpoint_does_not_load_asr_model() -> None:
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
