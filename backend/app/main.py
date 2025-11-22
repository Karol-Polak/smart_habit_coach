from fastapi import FastAPI

from .db import create_db_and_tables
from .routers import habits, habit_logs, habit_stats, habit_ml

app = FastAPI(title="Smart Habit Coach API")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def root():
    return {"message": "Smart Habit Coach API działa 🚀"}


# podpinamy routery
app.include_router(habits.router)
app.include_router(habit_logs.router)
app.include_router(habit_stats.router)
app.include_router(habit_ml.router)
