from fastapi import Depends, FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import Session

from app.core.database import Base, engine, get_db
from app.exceptions import EntityNotFoundError
from app.model.attendee import Attendee
from app.model.event import Event
from app.schemas.attendee import AttendeeCreate, AttendeeResponse
from app.schemas.event import EventCreate, EventResponde, EventUpdate

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Event Horizon Study Case", version="1.0.0")


@app.get("/")
def read_root():
    return {"status": "API is online"}


@app.post("/event/", response_model=EventResponde)
def create_event(event_data: EventCreate, db: Session = Depends(get_db)):
    new_event = Event(**event_data.model_dump())

    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event


@app.get("/event/{event_id}", response_model=EventResponde)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).get(event_id)

    if not event:
        raise EntityNotFoundError(name="Event", id=event_id)

    return event


@app.patch("/event/{event_id}", response_model=EventResponde)
def update_event(event_id: int, event_data: EventUpdate, db: Session = Depends(get_db)):
    event = db.query(Event).get(event_id)

    if not event:
        raise EntityNotFoundError(name="Event", id=event_id)

    update_data = event_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(event, key, value)

    db.commit()
    db.refresh(event_data)
    return event_data


@app.delete("/event/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).get(event_id)

    if not event:
        raise EntityNotFoundError(name="Event", id=event_id)

    db.delete(event)
    db.commit()

    return {"message": "Event was deleted"}


@app.post("/attendee/register/", response_model=AttendeeResponse)
def register_attendee(attendee_data: AttendeeCreate, db: Session = Depends(get_db)):
    event = db.query(Event).get(attendee_data.event_id)

    if not event:
        raise EntityNotFoundError(name="Event", id=attendee_data.event_id)

    attendee = Attendee(**attendee_data.model_dump())

    db.add(attendee)
    db.commit()
    db.refresh(attendee)
    return attendee


@app.exception_handler(EntityNotFoundError)
async def entity_not_found_handler(request: Request, exc: EntityNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": f"{exc.name} with ID {exc.id} not found."},
    )


@app.exception_handler(DatabaseError)
async def database_exception_handler(request: Request, exc: DatabaseError):

    error_msg = str(exc.orig)

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": error_msg},
    )
