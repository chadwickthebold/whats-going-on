from pathlib import Path

from sqlalchemy import create_engine

from db_models import Base, Organization, Venue, Event, DataSource

DB_PATH = Path(__file__).parent / "wgo.local.db"
DB_CONN_STR = f"sqlite+pysqlite:///{DB_PATH}"

engine = create_engine(DB_CONN_STR, echo=True)

Base.metadata.create_all(engine)
