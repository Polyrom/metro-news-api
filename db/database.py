from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import get_settings

settings = get_settings()

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()


def get_db():
    try:
        return db
    finally:
        db.close()
