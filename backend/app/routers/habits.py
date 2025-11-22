from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, text

from ..db import get_session
from ..models import Habit, HabitLog
from ..schemas import HabitCreate, HabitRead, HabitUpdate

router = APIRouter(prefix="/habits", tags=["habits"])


@router.get("/", response_model=List[HabitRead])
def list_habits(session: Session = Depends(get_session)):
    statement = select(Habit)
    results = session.exec(statement)
    habits = results.all()
    return habits


@router.post("/", response_model=HabitRead)
def create_habit(habit_in: HabitCreate, session: Session = Depends(get_session)):
    habit = Habit.from_orm(habit_in)
    session.add(habit)
    session.commit()
    session.refresh(habit)
    return habit


@router.get("/{habit_id}", response_model=HabitRead)
def get_habit(habit_id: int, session: Session = Depends(get_session)):
    habit = session.get(Habit, habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit

@router.delete("/{habit_id}")
def delete_habit(habit_id: int, session: Session = Depends(get_session)):
    habit = session.get(Habit, habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")

    # usuń powiązane logi
    logs = session.exec(
        select(HabitLog).where(HabitLog.habit_id == habit_id)
    ).all()
    for log in logs:
        session.delete(log)

    # usuń sam nawyk
    session.delete(habit)
    session.commit()

    return {"status": "success", "deleted_habit_id": habit_id}

@router.put("/{habit_id}")
def update_habit(habit_id: int, habit_update: HabitUpdate, session: Session = Depends(get_session)):
    habit = session.get(Habit, habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")

    if habit_update.name is not None:
        habit.name = habit_update.name
    if habit_update.description is not None:
        habit.description = habit_update.description

    session.add(habit)
    session.commit()
    session.refresh(habit)
    return habit
