from sqlalchemy import Column, Integer, String

from app.core.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(250), nullable=False, unique=True)
    hashed_password = Column(String(100), nullable=False)
