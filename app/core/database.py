from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# 1. Engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Try connection before use it
    pool_recycle=3600,  # Restart old connections
)

# 2. Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Base: class 
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
