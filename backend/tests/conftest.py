# backend/tests/conftest.py
import os
import sys
import pytest
from sqlmodel import SQLModel
from fastapi.testclient import TestClient

# --- ustawiamy PYTHONPATH, żeby "backend" był widoczny jako pakiet ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT_DIR)

# --- osobna baza dla testów ---
os.environ["DATABASE_URL"] = "sqlite:///./smart_habits_test.db"

from backend.app.db import engine, create_db_and_tables  # noqa: E402
from backend.app.main import app  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def prepare_database():
    """
    Tworzy świeżą bazę testową na czas sesji testowej.
    """
    # wyczyść wszystko na starcie
    SQLModel.metadata.drop_all(engine)
    create_db_and_tables()
    yield
    # po testach możesz znów wyczyścić bazę
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(scope="session")
def client():
    """
    Wspólny TestClient dla wszystkich testów.
    """
    with TestClient(app) as c:
        yield c
