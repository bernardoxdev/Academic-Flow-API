from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_pode_cursar_endpoint():
    payload = {
        "aluno_id": 1,
        "materia": "algoritmos"
    }

    response = client.post("/alunos/pode-cursar", json=payload)

    assert response.status_code == 200
    assert "pode_cursar" in response.json()
    assert isinstance(response.json()["pode_cursar"], bool)
