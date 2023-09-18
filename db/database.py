from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import get_settings


def get_db():
    settings = get_settings()

    engine = create_engine(settings.database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()
