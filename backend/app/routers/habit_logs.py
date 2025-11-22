from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..db import get_session
from ..models import Habit, HabitLog
from ..schemas import HabitLogCreate, HabitLogRead

router = APIRouter(prefix="/habit-logs", tags=["habit-logs"])


@router.post("/", response_model=HabitLogRead)
def create_habit_log(log_in: HabitLogCreate, session: Session = Depends(get_session)):
    habit = session.get(Habit, log_in.habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")

    log = HabitLog.from_orm(log_in)
    session.add(log)
    session.commit()
    session.refresh(log)
    return log


@router.get("/by-habit/{habit_id}", response_model=List[HabitLogRead])
def list_logs_for_habit(habit_id: int, session: Session = Depends(get_session)):
    statement = select(HabitLog).where(HabitLog.habit_id == habit_id).order_by(HabitLog.date)
    results = session.exec(statement)
    logs = results.all()
    return logs
