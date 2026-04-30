import datetime
import enum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.types import DateTime

"""
Code for generating DB models

General rules for data usage

* Timestamps relative to events should be recorded with the event-specific timezone

Usage of DeclarativeBase enables using Mapped to define columns. This may be overkill
as SQLite does not have a robust typing system
See https://docs.sqlalchemy.org/en/21/orm/declarative_tables.html#orm-declarative-mapped-column
"""

class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)


class EventType(str, enum.Enum):
    exhibition = "exhibition"
    performance = "performance"
    talk = "talk"
    screening = "screening"
    other = "other"


class Organization(Base):
    __tablename__ = 'organization'

    name: Mapped[str] = mapped_column(index=True, nullable=False)

    venues: Mapped[list["Venue"]] = relationship(back_populates="organization")
    data_sources: Mapped[list["DataSource"]] = relationship(back_populates="organization")


class Venue(Base):
    __tablename__ = 'venue'

    name: Mapped[str] = mapped_column(index=True, nullable=False)
    slug: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(nullable=True)
    website: Mapped[str] = mapped_column(nullable=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"), nullable=True)

    organization: Mapped["Organization"] = relationship(back_populates="venues")
    events: Mapped[list["Event"]] = relationship(back_populates="venue")
    data_sources: Mapped[list["DataSource"]] = relationship(back_populates="venue")


class Event(Base):
    __tablename__ = 'event'

    title: Mapped[str]
    short_description: Mapped[str] = mapped_column(nullable=True)
    event_type: Mapped[str] = mapped_column(nullable=True)
    event_start_timestamp: Mapped[datetime.datetime] = mapped_column(nullable=True)
    duration_minutes: Mapped[int] = mapped_column(nullable=True)
    is_passed: Mapped[bool] = mapped_column(default=False)
    venue_id: Mapped[int] = mapped_column(ForeignKey("venue.id"), nullable=True)

    venue: Mapped["Venue"] = relationship(back_populates="events")


class DataSource(Base):
    __tablename__ = 'data_source'

    url: Mapped[str] = mapped_column(nullable=False)
    last_checked: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    venue_id: Mapped[int] = mapped_column(ForeignKey("venue.id"), nullable=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"), nullable=True)

    venue: Mapped["Venue"] = relationship(back_populates="data_sources")
    organization: Mapped["Organization"] = relationship(back_populates="data_sources")
