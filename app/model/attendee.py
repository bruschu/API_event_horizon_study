from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Attendee(Base):
    __tablename__ = "attendee"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    email = Column(String(160), nullable=False)
    event_id = Column(Integer, ForeignKey("event.id"))

    event = relationship("Event", back_populates="attendees")
