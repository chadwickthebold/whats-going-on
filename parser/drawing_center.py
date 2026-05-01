from datetime import datetime
from email.utils import parsedate_to_datetime

from bs4 import Tag

from data.db_models import Event, EventType
from parser.parser import HTMLParser


class DrawingCenterParser(HTMLParser):
    def parse(self, file_path: str) -> list[Event]:
        soup = self._load(file_path)
        events: list[Event] = []

        onview = soup.find(id="onview")
        if onview:
            for exhibit in onview.find_all(class_="exhibit_module"):
                event = self._parse_exhibit(exhibit, is_upcoming=False)
                if event:
                    events.append(event)

        upcoming = soup.find(id="upcoming")
        if upcoming:
            for exhibit in upcoming.find_all(class_="exhibit_module"):
                event = self._parse_exhibit(exhibit, is_upcoming=True)
                if event:
                    events.append(event)

        return events

    def _parse_exhibit(self, exhibit: Tag, is_upcoming: bool) -> Event | None:
        title_tag = exhibit.find("h2")
        if not title_tag:
            raise ValueError(f"No title found in exhibit: {exhibit}")

        title = title_tag.get_text(strip=True)

        time_tag = exhibit.find("time")
        ## TODO need to add an end datetime field in our model, to identify events 
        ## we learned about when they were ongoing
        ## TODO add an optional url field to our event model to 
        ## TODO extract a reference image to be used for display in the UI
        event_start_timestamp: datetime | None = None
        if is_upcoming and time_tag and time_tag.get("datetime"):
            event_start_timestamp = _parse_js_date(str(time_tag["datetime"]))

        return Event(
            title=title,
            event_type=EventType.exhibition,
            event_start_timestamp=event_start_timestamp,
            is_passed=False,
        )

def _parse_js_date(date_str: str) -> datetime:
    """
    The Drawing Center sets `datetime` attributes using JS Date.toString(), which produces
    "Fri Jun 26 2026 00:00:00 GMT-0400" rather than an ISO 8601 string. Some environments
    also append a named timezone in parens (e.g. "(Eastern Daylight Time)") which strptime
    rejects, so we strip it before parsing.
    """
    if "(" in date_str:
        date_str = date_str[:date_str.index("(")].strip()
    return datetime.strptime(date_str, "%a %b %d %Y %H:%M:%S GMT%z")
