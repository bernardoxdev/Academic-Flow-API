from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_fluxograma_endpoint():
    response = client.get("/fluxograma/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
