import requests
from datetime import date
import os

#Konfiguracja API
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


# Funkcje pomocnicze do API

def get_habits():
    resp = requests.get(f"{API_BASE_URL}/habits/")
    resp.raise_for_status()
    return resp.json()

def create_habit(name: str, description: str | None = None):
    payload = {"name": name, "description": description or None}
    resp = requests.post(f"{API_BASE_URL}/habits/", json=payload)
    resp.raise_for_status()
    return resp.json()

def create_habit_log(
    habit_id: int,
    log_date: date,
    done: bool,
    mood: int | None = None,
    energy_level: int | None = None,
    note: str | None = None,
):
    payload = {
        "habit_id": habit_id,
        "date": log_date.isoformat(),
        "done": done,
        "mood": mood,
        "energy_level": energy_level,
        "note": note or None,
    }
    resp = requests.post(f"{API_BASE_URL}/habit-logs/", json=payload)
    resp.raise_for_status()
    return resp.json()

def get_habit_stats(habit_id: int):
    resp = requests.get(f"{API_BASE_URL}/habits/{habit_id}/stats")
    resp.raise_for_status()
    return resp.json()


def get_logs_for_habit(habit_id: int):
    resp = requests.get(f"{API_BASE_URL}/habit-logs/by-habit/{habit_id}")
    resp.raise_for_status()
    return resp.json()

def predict_habit_probability(
        habit_id: int,
        prediction_date: date,
        mood: int | None = None,
        energy_level: int | None = None,
):
    params = {
        "prediction_date": prediction_date.isoformat(),
    }
    if mood is not None:
        params["mood"] = mood
    if energy_level is not None:
        params["energy_level"] = energy_level

    resp = requests.get(f"{API_BASE_URL}/habits/{habit_id}/predict", params=params)
    resp.raise_for_status()
    return resp.json()

def train_habit_model(habit_id: int):
    resp = requests.post(f"{API_BASE_URL}/habits/{habit_id}/train")
    resp.raise_for_status()
    return resp.json()

def delete_habit(habit_id: int):
    resp = requests.delete(f"{API_BASE_URL}/habits/{habit_id}")
    resp.raise_for_status()
    return resp.json()

def update_habit(habit_id: int, name: str | None = None, description: str | None = None):
    payload = {}
    if name is not None:
        payload["name"] = name
        if description is not None:
            payload["description"] = description
    resp = requests.put(f"{API_BASE_URL}/habits/{habit_id}", json=payload)
    resp.raise_for_status()
    return resp.json()