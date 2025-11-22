from sqlmodel import SQLModel
from backend.app.db import engine, DATABASE_URL

def reset_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    print("Reset db", DATABASE_URL)

if __name__ == "__main__":
    reset_db()

#python -m backend.tools.reset_db