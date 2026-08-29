from fastapi.testclient import TestClient

from netra_setu.app import app

client = TestClient(app)


def test_registry_health() -> None:
    response = client.get("/registry/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_security_health() -> None:
    response = client.get("/authz/health")
    assert response.status_code == 200
