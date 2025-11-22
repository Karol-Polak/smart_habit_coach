from collections import Counter
from datetime import datetime
import os

import pandas as pd
from joblib import dump
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from ..db import engine
from ..models import HabitLog
from sqlmodel import Session, select

MODELS_DIR = "ml_models"
os.makedirs(MODELS_DIR, exist_ok=True)


def load_logs_for_habit(habit_id: int) -> pd.DataFrame:
    with Session(engine) as session:
        stmt = select(HabitLog).where(HabitLog.habit_id == habit_id)
        logs = session.exec(stmt).all()

    if not logs:
        raise ValueError(f"Brak logów dla habit_id={habit_id}")

    rows = []
    for log in logs:
        rows.append(
            {
                "habit_id": log.habit_id,
                "date": log.date,
                "done": int(log.done),
                "mood": log.mood,
                "energy_level": log.energy_level,
                "weekday": log.date.weekday(),
            }
        )
    return pd.DataFrame(rows)


def prepare_features(df: pd.DataFrame):
    df = df.copy()

    for col in ["mood", "energy_level"]:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].mean())

    X = df[["weekday", "mood", "energy_level"]]
    y = df["done"]
    return X, y


def train_model_for_habit(habit_id: int) -> dict:
    """Trenuje model dla danego nawyku i zwraca podsumowanie treningu."""
    df = load_logs_for_habit(habit_id)
    X, y = prepare_features(df)

    class_counts = Counter(y)
    if len(class_counts) < 2:
        # tylko 0 albo tylko 1 – brak sensownego treningu
        raise ValueError(
            f"Za mało zróżnicowanych danych dla habit_id={habit_id}. "
            f"Potrzebne są logi z done=1 ORAZ done=0, a masz: {dict(class_counts)}."
        )

    warn_few_samples = False
    if len(df) < 10:
        warn_few_samples = True

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )

    model = LogisticRegression()
    model.fit(X_train, y_train)

    metrics_dict = classification_report(y_test, model.predict(X_test), output_dict=True)
    accuracy = float(metrics_dict["accuracy"])

    trained_at = datetime.utcnow().isoformat()
    model_path = os.path.join(MODELS_DIR, f"habit_{habit_id}.joblib")

    dump(
        {
            "model": model,
            "trained_at": trained_at,
            "habit_id": habit_id,
            "n_samples": len(df),
            "class_counts": dict(class_counts),
            "accuracy": accuracy,
        },
        model_path,
    )

    return {
        "habit_id": habit_id,
        "trained_at": trained_at,
        "n_samples": len(df),
        "class_counts": dict(class_counts),
        "accuracy": accuracy,
        "model_path": model_path,
        "warning_few_samples": warn_few_samples,
    }


if __name__ == "__main__":
    habit_id_to_train = 1
    summary = train_model_for_habit(habit_id_to_train)
    print("Podsumowanie treningu:", summary)
