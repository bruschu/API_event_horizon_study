from pydantic import BaseModel

from app.schemas.event import EventBase


class AttendeeBase(BaseModel):
    name: str
    email: str


class AttendeeCreate(AttendeeBase):
    event_id: int


class AttendeeResponse(AttendeeBase):
    id: int
    event_id: int
    event: EventBase | None = None

    class Config:
        from_attributes = True


class AttendeeUpdate(AttendeeBase):
    name: str | None = None
    email: str | None = None
    event_id: int | None = None
