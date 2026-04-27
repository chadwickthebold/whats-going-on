from sqlalchemy import create_engine
from models import Venue

"""
Create a new create_engine and have it log out
all of the table creation statement from the configured
models.
"""
engine = create_engine("sqlite://", echo=False)

Venue.metadata.create_all(engine)