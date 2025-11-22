from datetime import date
from typing import Optional

from sqlmodel import SQLModel, Field


class HabitBase(SQLModel):
    name: str
    description: Optional[str] = None


class Habit(HabitBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class HabitLogBase(SQLModel):
    habit_id: int = Field(foreign_key="habit.id")
    date: date
    done: bool
    mood: Optional[int] = None
    energy_level: Optional[int] = None
    note: Optional[str] = None


class HabitLog(HabitLogBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
