from datetime import date, timedelta


def _create_habit_with_logs(client, done_values):
    # helper: tworzy nawyk z listą done True/False
    payload = {
        "name": "ML test habit",
        "description": "ML test"
    }
    resp = client.post("/habits/", json=payload)
    assert resp.status_code == 200
    habit = resp.json()
    habit_id = habit["id"]

    start = date.today() - timedelta(days=len(done_values))

    for i, done in enumerate(done_values):
        log_payload = {
            "habit_id": habit_id,
            "date": (start + timedelta(days=i)).isoformat(),
            "done": done,
            "mood": 3,
            "energy_level": 3,
            "note": None,
        }
        resp = client.post("/habit-logs/", json=log_payload)
        assert resp.status_code == 200, resp.text

    return habit_id


def test_train_model_not_enough_class_diversity_returns_400(client):
    # wszystkie done=True -> jedna klasa
    habit_id = _create_habit_with_logs(client, done_values=[True] * 5)

    resp = client.post(f"/habits/{habit_id}/train")
    print("STATUS:", resp.status_code, "BODY:", resp.text)  # debug, możesz usunąć gdy zadziała
    assert resp.status_code == 400
    data = resp.json()
    assert "Za mało" in data["detail"] or "zróżnicowanych" in data["detail"]



def test_train_model_success_returns_summary(client):
    # miks True/False -> dwie klasy
    habit_id = _create_habit_with_logs(
        client,
        done_values=[True, False, True, False, True, True, False],
    )

    resp = client.post(f"/habits/{habit_id}/train")
    assert resp.status_code == 200
    summary = resp.json()

    # kilka sanity checków
    assert summary["habit_id"] == habit_id
    assert summary["n_samples"] >= 5
    assert "accuracy" in summary
    assert "class_counts" in summary

def test_habit_stats_basic_keys(client):
    habit_id = _create_habit_with_logs(
        client,
        done_values=[True, False, True]
    )

    resp = client.get(f"/habits/{habit_id}/stats")
    assert resp.status_code == 200
    stats = resp.json()

    for key in ["total", "done", "not_done", "success_rate", "streak_current", "streak_longest"]:
        assert key in stats