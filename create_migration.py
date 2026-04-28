from sqlalchemy import create_engine
from db_models import Venue, Event

DB_PATH = "/data/wgo.db"
DB_CONN_STR = "sqlite+pysqlite://" + DB_PATH

"""
Create a new create_engine and have it log out
all of the table creation statement from the configured
models.
"""
engine = create_engine(DB_CONN_STR, echo=True)

Venue.metadata.create_all(engine)
