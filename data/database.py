from sqlalchemy import create_engine

DB_CONN_STR = "sqlite+pysqlite:///data/wgo.local.db"

engine = create_engine(DB_CONN_STR, echo=True)
