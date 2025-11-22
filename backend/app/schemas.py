from typing import Optional
from datetime import date
from pydantic import BaseModel
from typing import Optional

from sqlmodel import SQLModel


# ----- HABITS -----

class HabitBase(SQLModel):
    name: str
    description: Optional[str] = None


class HabitCreate(HabitBase):
    pass


class HabitRead(HabitBase):
    id: int


# ----- HABIT LOGS -----

class HabitLogBase(SQLModel):
    habit_id: int
    date: date
    done: bool
    mood: Optional[int] = None
    energy_level: Optional[int] = None
    note: Optional[str] = None


class HabitLogCreate(HabitLogBase):
    pass


class HabitLogRead(HabitLogBase):
    id: int


class HabitUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None