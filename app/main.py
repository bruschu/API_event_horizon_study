from fastapi import FastAPI

from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Event Horizon Study Case", version="1.0.0")


@app.get("/")
def read_root():
    return {"status": "API is online"}
