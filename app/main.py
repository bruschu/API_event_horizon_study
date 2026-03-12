from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED

from app.core.auth import get_current_user
from app.core.database import Base, engine, get_db
from app.core.security import create_access_token, get_password_hash, verify_password
from app.exceptions import EntityNotFoundError
from app.model.attendee import Attendee
from app.model.event import Event
from app.model.user import User  # noqa: F401
from app.schemas.attendee import AttendeeCreate, AttendeeResponse
from app.schemas.event import EventCreate, EventResponde, EventUpdate
from app.schemas.user import Token, UserCreate, UserResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Event Horizon Study Case", version="1.0.0")


@app.get("/")
def read_root():
    return {"status": "API is online"}


@app.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pwd = get_password_hash(user.password)

    new_user = User(email=user.email, hashed_password=hashed_pwd)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    # 1. Look for the user in the database
    user = db.query(User).filter(User.email == form_data.username).first()

    # 2. Check if user exists and password is correct
    if not user or not verify_password(form_data.password, str(user.hashed_password)):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Incorrect email or password"
        )

    # 3. Create the JWT
    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/event/", response_model=EventResponde)
def create_event(
    event_data: EventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_event = Event(**event_data.model_dump())

    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event


@app.get("/event/{event_id}", response_model=EventResponde)
def get_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
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
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    event = db.query(Event).get(event_id)

    if not event:
        raise EntityNotFoundError(name="Event", id=event_id)

    db.delete(event)
    db.commit()

    return {"message": "Event was deleted"}


@app.post("/attendee/register/", response_model=AttendeeResponse)
def register_attendee(
    attendee_data: AttendeeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
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
