from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Smart Habit Coach" in data["message"]


def test_create_and_list_habits(client):
    # 1. Utworzenie nowego nawyku
    payload = {
        "name": "Testowy nawyk pytest",
        "description": "Opis testowy"
    }
    response = client.post("/habits/", json=payload)
    assert response.status_code == 200

    created = response.json()
    habit_id = created["id"]

    assert created["name"] == payload["name"]
    assert created["description"] == payload["description"]

    # 2. Pobranie listy nawyków
    response = client.get("/habits/")
    assert response.status_code == 200
    habits = response.json()

    assert any(h["id"] == habit_id for h in habits)

def test_update_habit(client):
    payload = {
        "name": "stara nazwa",
        "description": "stary opis"
    }
    resp = client.post("/habits/", json=payload)
    assert resp.status_code == 200
    habit = resp.json()
    habit_id = habit["id"]

    update_payload = {
        "name": "nowa nazwa",
        "description": "nowy opis"
    }
    resp = client.put(f"/habits/{habit_id}/", json=update_payload)
    assert resp.status_code == 200
    updated = resp.json()

    assert updated["id"] == habit_id
    assert updated["name"] == "nowa nazwa"
    assert updated["description"] == "nowy opis"
