# backend/tests/test_habit_logs.py
from datetime import date


def test_create_and_get_logs(client):
    # 1. Utwórz nawyk
    habit_payload = {
        "name": "Test habit log",
        "description": "habit for logging tests"
    }
    habit_resp = client.post("/habits/", json=habit_payload)
    assert habit_resp.status_code == 200
    habit = habit_resp.json()
    habit_id = habit["id"]

    # 2. Dodaj log (np. wykonany)
    log_payload = {
        "habit_id": habit_id,
        "date": date.today().isoformat(),
        "done": True,
        "mood": 4,
        "energy_level": 3,
        "note": "Test note"
    }
    log_resp = client.post("/habit-logs/", json=log_payload)
    assert log_resp.status_code == 200

    created_log = log_resp.json()
    assert created_log["habit_id"] == habit_id
    assert created_log["done"] is True
    assert created_log["mood"] == 4
    assert created_log["energy_level"] == 3

    # 3. Pobierz logi
    logs_resp = client.get(f"/habit-logs/by-habit/{habit_id}")
    assert logs_resp.status_code == 200
    logs = logs_resp.json()

    assert isinstance(logs, list)
    assert len(logs) == 1

    log = logs[0]
    assert log["habit_id"] == habit_id
    assert log["done"] is True
