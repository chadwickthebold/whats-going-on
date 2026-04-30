import argparse
import urllib.request
from pathlib import Path
from data.db_models import Venue, Event
from parser.drawing_center import DrawingCenterParser
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

TMP_DIR = Path(__file__).parent / "tmp"

DB_CONN_STR = "sqlite+pysqlite:///data/wgo.local.db"

PARSERS = {
    "drawing-center": DrawingCenterParser,
}

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("venue", help="venue slug for refresh")

engine = create_engine(DB_CONN_STR, echo=True)

"""
Script to manage workflow of refreshing content from a provided datasource
$ python refresh.py drawing-center

TODO
* Implement an incremental workflow process if the parse has to chew through a lot of old data
"""

if __name__ == '__main__':
    args = arg_parser.parse_args()
    venue_target = args.venue
    print(f"Attempting refresh for venue: [{venue_target}]")

    parser_class = PARSERS.get(venue_target)
    if parser_class is None:
        print(f"No parser registered for venue slug: [{venue_target}]")
        exit(1)

    with Session(engine) as session:
        venue = session.execute(select(Venue).where(Venue.slug == venue_target)).scalar_one_or_none()
        if venue is None:
            print(f"No venue found with slug: [{venue_target}]")
            exit(1)

        data_sources = venue.data_sources
        print(f"Found {len(data_sources)} data source(s) for venue: [{venue.name}]")

        TMP_DIR.mkdir(exist_ok=True)

        new_events = []
        for source in data_sources:
            print(f"Processing data source: {source.url}")

            tmp_file = TMP_DIR / f"{venue_target}.html"
            with urllib.request.urlopen(source.url) as response:
                tmp_file.write_bytes(response.read())

            parsed_events = parser_class().parse(str(tmp_file))

            existing_titles = {
                row[0] for row in session.execute(
                    select(Event.title).where(Event.venue_id == venue.id)
                )
            }
            new_events = [e for e in parsed_events if e.title not in existing_titles]
            for event in new_events:
                event.venue_id = venue.id
                session.add(event)

        session.commit()
        print(f"Inserted {len(new_events)} new event(s)")
