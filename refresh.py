import argparse
import urllib.request
from data.db_models import Venue, Event
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

DB_CONN_STR = "sqlite+pysqlite:///data/wgo.local.db"

parser = argparse.ArgumentParser()
parser.add_argument("venue", help="venue slug for refresh")

engine = create_engine(DB_CONN_STR, echo=True)

"""
Script to manage workflow of refreshing content from a provided datasource
$ ./refresh.py drawing_center

TODO
* Implement an incremental workflow process if the parse has to chew through a lot of old data
"""

if __name__ == '__main__':
    args = parser.parse_args()
    venue_target = args.venue
    print(f"Attempting refresh for venue: [{venue_target}]")

    with Session(engine) as session:
        venue = session.execute(select(Venue).where(Venue.slug == venue_target)).scalar_one_or_none()
        if venue is None:
            print(f"No venue found with slug: [{venue_target}]")
            exit(1)

        data_sources = venue.data_sources
        print(f"Found {len(data_sources)} data source(s) for venue: [{venue.name}]")

        new_events = []
        for source in data_sources:
            print(f"Processing data source: {source.url}")

            # Query the html page
            with urllib.request.urlopen(source.url) as response:
                html = response.read()

            # TODO: run through the venue-specific parser to extract event dicts from html

            parsed_events = []

            # Check for unknown events and insert into DB
            existing_titles = {
                row[0] for row in session.execute(
                    select(Event.title).where(Event.venue_id == venue.id)
                )
            }
            new_events = [e for e in parsed_events if e["title"] not in existing_titles]
            for event_data in new_events:
                session.add(Event(venue_id=venue.id, **event_data))

        session.commit()
        print(f"Inserted {len(new_events)} new event(s)")
