"""One-off bootstrap: create all tables from the SQLAlchemy models.
Run with: ./venv/Scripts/python.exe create_tables.py
"""

from app.core.db import engine
from app.models import Base

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Tables created:", list(Base.metadata.tables.keys()))
