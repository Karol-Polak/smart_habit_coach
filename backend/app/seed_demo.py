# demo seed do sprawdzenia działania aplikacji
# aby zasiać "python -m backend.app.seed_demo"

from datetime import date, timedelta
import random

from sqlmodel import Session

from .db import engine, create_db_and_tables
from .models import Habit, HabitLog


def seed_demo():
    create_db_and_tables()

    with Session(engine) as session:
        existing_habits = session.query(Habit).all()
        if existing_habits:
            print("Seed pominięty – nawyki już istnieją.")
            return

        # Tworzymy kilka przykładowych nawyków
        habit1 = Habit(name="Poranna nauka Pythona", description="30 minut kodowania dziennie rano")
        habit2 = Habit(name="Bieganie", description="Bieganie co najmniej 20 minut")
        habit3 = Habit(name="Czytanie książki", description="10 stron dziennie")

        session.add(habit1)
        session.add(habit2)
        session.add(habit3)
        session.commit()

        session.refresh(habit1)
        session.refresh(habit2)
        session.refresh(habit3)

        habits = [habit1, habit2, habit3]

        today = date.today()
        start = today - timedelta(days=30)

        for habit in habits:
            for i in range(31):
                d = start + timedelta(days=i)

                # losowość wykonania zależna trochę od dnia tygodnia
                base_prob = 0.7
                if d.weekday() in (5, 6):  # sobota/niedziela
                    base_prob -= 0.15

                done = random.random() < base_prob

                mood = random.randint(2, 5)
                energy = random.randint(2, 5)

                log = HabitLog(
                    habit_id=habit.id,
                    date=d,
                    done=done,
                    mood=mood,
                    energy_level=energy,
                    note=None,
                )
                session.add(log)

        session.commit()
        print("Seed demo zakończony – utworzono przykładowe nawyki i logi.")


if __name__ == "__main__":
    seed_demo()


