import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
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

    pass

class Venue(Base):
    __tablename__ = 'venue'

    name: Mapped[str] = mapped_column(index=True, nullable=False)
    address: Mapped[str] = mapped_column(nullable=True)
    website: Mapped[str] = mapped_column(nullable=True)


class Event(Base):
    __tablename__ = 'event'

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    title: Mapped[str]
    short_description: Mapped[str]
    event_start_timestamp: Mapped[datetime.datetime]
    # should be stored with a timezone
