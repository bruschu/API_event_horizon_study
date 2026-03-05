from datetime import datetime

from pydantic import BaseModel


class EventBase(BaseModel):
    name: str
    date: datetime
    location: str


class EventCreate(EventBase):
    pass


class EventResponde(EventBase):
    id: int

    class Config:
        from_attributes = True


class EventUpdate(BaseModel):
    name: str | None = None
    date: datetime | None = None
    location: str | None = None
