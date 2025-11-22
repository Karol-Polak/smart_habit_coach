from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from datetime import date

from ..db import get_session
from ..models import Habit, HabitLog

router = APIRouter(prefix="/habits", tags=["habit-stats"])


@router.get("/{habit_id}/stats")
def habit_stats(habit_id: int, session: Session = Depends(get_session)):
    # sprawdź czy habit istnieje
    habit = session.get(Habit, habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")

    # pobierz logi
    statement = select(HabitLog).where(HabitLog.habit_id == habit_id)
    logs = session.exec(statement).all()

    if not logs:
        return {
            "habit_id": habit_id,
            "total": 0,
            "done": 0,
            "not_done": 0,
            "success_rate": 0.0,
            "streak_current": 0,
            "streak_longest": 0,
            "by_weekday": {}
        }

    total = len(logs)
    done = sum(1 for log in logs if log.done)
    not_done = total - done
    success_rate = done / total if total > 0 else 0.0

    # streaks (ciągi wykonanych dni)
    sorted_logs = sorted(logs, key=lambda x: x.date)
    streak_current = 0
    streak_longest = 0
    prev_date = None

    for log in sorted_logs:
        if log.done:
            if prev_date and (log.date - prev_date).days == 1:
                streak_current += 1
            else:
                streak_current = 1
            streak_longest = max(streak_longest, streak_current)
            prev_date = log.date
        else:
            prev_date = None
            streak_current = 0

    # rozkład po dniach tygodnia
    by_weekday = {}
    for log in logs:
        weekday = log.date.weekday()
        by_weekday.setdefault(weekday, 0)
        if log.done:
            by_weekday[weekday] += 1

    return {
        "habit_id": habit_id,
        "total": total,
        "done": done,
        "not_done": not_done,
        "success_rate": round(success_rate, 2),
        "streak_current": streak_current,
        "streak_longest": streak_longest,
        "by_weekday": by_weekday
    }
