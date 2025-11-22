from datetime import date
from typing import Optional
from fastapi import Depends

from fastapi import APIRouter, HTTPException

from ..models import Habit
from ..db import get_session
from ..ml.predict_model import predict_probability_for_habit
from ..ml.train_model import train_model_for_habit
from sqlmodel import Session

router = APIRouter(prefix="/habits", tags=["habit-ml"])

@router.get("/{habit_id}/predict")
def predict_habit_execution(
        habit_id: int,
        prediction_date: date,
        mood: Optional[int] = None,
        energy_level: Optional[int] = None,
        session: Session = Depends(get_session),
):
    """Przewiduje prawdopodobieństwo wykonania nawyku w danym dniu"""
    with session as s:
        habit = s.get(Habit, habit_id)
        if not habit:
            raise HTTPException(status_code=404, detail="Habit not found")

    try:
        result = predict_probability_for_habit(
            habit_id=habit_id,
            prediction_date=prediction_date,
            mood=mood,
            energy_level=energy_level,
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd podczas predykcji: {e}")

    return result

@router.post("/{habit_id}/train")
def train_habit_endpoint(
        habit_id: int,
        session: Session = Depends(get_session),
):
    habit = session.get(Habit, habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")

    try:
        summary = train_model_for_habit(habit_id)
        return summary
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd podczas treningu: {e}")