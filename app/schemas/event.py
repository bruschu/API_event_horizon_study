from datetime import datetime

from pydantic import BaseModel, Field


class EventBase(BaseModel):
    name: str
    date: datetime
    location: str = Field(
        ...,  # The ellipsis means this field is REQUIRED
        max_length=200,
        description="The physical or virtual address where the event takes place",
        examples=["New York City", "Zoom Meeting"],
    )


class EventCreate(EventBase):
    pass


class EventResponde(EventBase):
    id: int

    class ConfigDict:
        from_attributes = True


class EventUpdate(BaseModel):
    name: str | None = None
    date: datetime | None = None
    location: str | None = None
