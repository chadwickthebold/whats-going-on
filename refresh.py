import argparse
import urllib.request
from pathlib import Path

from sqlalchemy.orm import Session

from data.database import engine
from data.db_models import Event
from data.repositories import DataSourceRepository, EventRepository, VenueRepository
from parser.drawing_center import DrawingCenterParser

TMP_DIR = Path(__file__).parent / "tmp"

PARSERS = {
    "drawing-center": DrawingCenterParser,
}

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("venue", help="venue slug for refresh")

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
        venue_repo = VenueRepository(session)
        event_repo = EventRepository(session)
        source_repo = DataSourceRepository(session)

        venue = venue_repo.find_by_slug(venue_target)
        if venue is None:
            print(f"No venue found with slug: [{venue_target}]")
            exit(1)

        sources = source_repo.find_by_venue(venue.id)
        print(f"Found {len(sources)} data source(s) for venue: [{venue.name}]")

        TMP_DIR.mkdir(exist_ok=True)

        total_new = 0
        for source in sources:
            print(f"Processing data source: {source.url}")

            tmp_file = TMP_DIR / f"{venue_target}.html"
            with urllib.request.urlopen(source.url) as response:
                tmp_file.write_bytes(response.read())

            parsed_events = parser_class().parse(str(tmp_file))

            existing_titles = event_repo.titles_for_venue(venue.id)
            new_events = [e for e in parsed_events if e.title not in existing_titles]
            for event in new_events:
                event.venue_id = venue.id
                event_repo.save(event)

            source_repo.mark_checked(source)
            total_new += len(new_events)

        session.commit()
        print(f"Inserted {total_new} new event(s)")
