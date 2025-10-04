from database import get_db
from sqlalchemy.orm import Session
from typing import Generator

def get_database() -> Generator[Session, None, None]:
    """Injection de dépendance pour la base de données"""
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()
