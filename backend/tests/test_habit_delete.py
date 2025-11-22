from datetime import date

def test_delete_habit_and_logs(client):
    payload = {
        "name": "Nawyk do usuniecia",
        "description": "Test delete",
    }
    resp = client.post("/habits/", json=payload)
    assert resp.status_code == 200
    habit = resp.json()
    habit_id = habit["id"]

    for i in range(3):
        log_payload = {
            "habit_id": habit_id,
            "date": date.today().isoformat(),
            "done": True,
            "mood": 4,
            "energy_level": 4,
            "note": f"log {i}"
        }
        resp = client.post("/habit-logs/", json=log_payload)
        assert resp.status_code == 200

    resp = client.get(f"/habit-logs/by-habit/{habit_id}")
    assert resp.status_code == 200
    logs = resp.json()
    assert len(logs) == 3

    resp = client.delete(f"/habits/{habit_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["deleted_habit_id"] == habit_id

    resp = client.get(f"/habit-logs/by-habit/{habit_id}")
    assert resp.status_code == 200
    logs_after = resp.json()
    assert logs_after == []