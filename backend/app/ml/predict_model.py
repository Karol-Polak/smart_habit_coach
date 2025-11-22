import os
from datetime import date
from typing import Optional

import numpy as np
import pandas as pd
from joblib import load

MODELS_DIR = "ml_models"

def load_model_bundle(habit_id: int):
    """Ładuje zapisany model dla danego habit_id"""
    model_path = os.path.join(MODELS_DIR, f"habit_{habit_id}.joblib")
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Nie znaleziono modelu dla habit_id={habit_id}. "
            f"Upewnij się, że uruchomiłeś trening i powstał plik {model_path}."
        )
    bundle = load(model_path)
    return bundle

def prepare_single_feature_row(
        prediction_date: date,
        mood: Optional[int],
        energy_level: Optional[int],
) -> pd.DataFrame:
    """Przygotowuje pojedynczy wiesz cech do predykcji"""

    weekday = prediction_date.weekday()

    #Brak podanych wartości dla nastroju / energii przyjmujemy średnie wartości
    mood_val = float(mood) if mood is not None else 3.0
    energy_val = float(energy_level) if energy_level is not None else 0.0

    data = {
        "weekday": [weekday],
        "mood": [mood_val],
        "energy_level": [energy_val],
    }

    df = pd.DataFrame(data)
    return df

def predict_probability_for_habit(
        habit_id: int,
        prediction_date: date,
        mood: Optional[int],
        energy_level: Optional[int],
) -> dict:
    """Zwraca słownik z prawdopodobieństwem wykonania nawyku"""
    bundle = load_model_bundle(habit_id)
    model = bundle["model"]
    trained_at = bundle.get("trained_at")

    X = prepare_single_feature_row(prediction_date, mood, energy_level)

    #zakładamy że model ma predict_proba
    proba = model.predict_proba(X)[0][1]

    return {
        "habit_id": habit_id,
        "date": prediction_date.isoformat(),
        "mood": mood,
        "energy_level": energy_level,
        "probability_done": float(np.round(proba, 3)),
        "model_trained_at": trained_at,
    }