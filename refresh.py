import argparse
from data.db_models import Venue

parser = argparse.ArgumentParser()
parser.add_argument("venue", help="venue name for refresh")



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

    # Query the DB to get data sources for the venue
    Venue.

    # For each data source go through the associated workflow
    # initial milestone - assume each data source is an html page

    # Query the html page

    # run through the venue parser

    # Check for unknown events and insert into DB
