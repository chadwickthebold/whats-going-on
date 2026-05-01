from datetime import datetime, UTC

from sqlalchemy import select
from sqlalchemy.orm import Session

from data.db_models import DataSource, Event, Venue


class EventRepository:
    def __init__(self, session: Session):
        self.session = session

    def titles_for_venue(self, venue_id: int) -> set[str]:
        return {
            row[0] for row in self.session.execute(
                select(Event.title).where(Event.venue_id == venue_id)
            )
        }

    def source_urls_for_venue(self, venue_id: int) -> set[str]:
        return {
            row[0] for row in self.session.execute(
                select(Event.source_url).where(
                    Event.venue_id == venue_id,
                    Event.source_url.is_not(None),
                )
            )
        }

    def save(self, event: Event) -> None:
        self.session.add(event)


class VenueRepository:
    def __init__(self, session: Session):
        self.session = session

    def find_by_slug(self, slug: str) -> Venue | None:
        return self.session.execute(
            select(Venue).where(Venue.slug == slug)
        ).scalar_one_or_none()


class DataSourceRepository:
    def __init__(self, session: Session):
        self.session = session

    def find_by_venue(self, venue_id: int) -> list[DataSource]:
        return list(
            self.session.execute(
                select(DataSource).where(DataSource.venue_id == venue_id)
            ).scalars()
        )

    def mark_checked(self, source: DataSource) -> None:
        source.last_checked = datetime.now(UTC)
        self.session.add(source)
