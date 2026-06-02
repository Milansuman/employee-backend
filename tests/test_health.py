from fastapi.testclient import TestClient
from main import app

test_client = TestClient(app)


def test_health_check():
    response = test_client.get("/healthcheck")

    assert response.status_code == 200
    assert response.text == '"OK"'
