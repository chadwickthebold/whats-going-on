from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    total: int
    limit: int
    offset: int
    items: list[T]


class VenueResponse(BaseModel):
    id: int
    name: str
    slug: str
    address: str | None
    website: str | None

    model_config = {"from_attributes": True}


class EventResponse(BaseModel):
    id: int
    title: str
    event_type: str | None
    event_start_timestamp: datetime | None
    source_url: str | None
    venue_id: int | None

    model_config = {"from_attributes": True}
