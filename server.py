from fastapi import Depends, FastAPI, Query
from sqlalchemy.orm import Session

from data.database import engine
from data.repositories import EventRepository, VenueRepository
from schemas import EventResponse, PaginatedResponse, VenueResponse

app = FastAPI(title="What's Going On", version="0.4.1")


def get_db():
    with Session(engine) as session:
        yield session


@app.get("/venues", response_model=PaginatedResponse[VenueResponse])
def list_venues(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    repo = VenueRepository(db)
    return PaginatedResponse(
        total=repo.count(),
        offset=offset,
        limit=limit,
        items=repo.find_all(offset=offset, limit=limit),
    )


@app.get("/events", response_model=PaginatedResponse[EventResponse])
def list_events(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    repo = EventRepository(db)
    return PaginatedResponse(
        total=repo.count(),
        offset=offset,
        limit=limit,
        items=repo.find_all(offset=offset, limit=limit),
    )
