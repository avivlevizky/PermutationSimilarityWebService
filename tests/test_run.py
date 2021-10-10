from fastapi.testclient import TestClient

from app.main import fastapi_app

client = TestClient(fastapi_app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}