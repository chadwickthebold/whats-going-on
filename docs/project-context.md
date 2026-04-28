A service to track upcoming events.

## Context
New York has a lot of cultural venues such as museums, concert halls, and other event spaces that host interesting events. However it can be challenging to keep up to date with their schedules. Most venues announce events through email mailing lists or publish them on their websites. However the cadence of these updates is inconsistent and requires a lot of manual work to check them all regularly.

I want to create a service that I can use to track upcoming events and find interesting ones that I might want to go to.

## Project Goals

1. Provide a digest of newly announced events since the last time I reviewed the upcoming calendar
2. Enable sorting/filtering based on common categories
	1. These common categories may differ between event types like concerts or art exhibitions
3. Record state in a durable, lightweight manner
4. Allow control via a minimal yet functional UI

## Examples
* Drawing Center
	* https://drawingcenter.org/exhibitions
* Pioneer Works
	* https://pioneerworks.org/calendar
* Carnegie Hall
	* https://www.carnegiehall.org/#calendar
* Park Ave Armory
	* https://www.armoryonpark.org/season-events/current-season/
* Knockdown Center
	* https://www.knockdown.center/upcoming
* Playwrights Horizons
	* https://www.playwrightshorizons.org/shows
* New York Theater Workshop
	* https://www.nytw.org/calendar/
* Artnet
	* New York Events https://www.artnet.com/events/new-york/
* Artforum
	* https://artguide.artforum.com/artguide/place/new-york

## Stretch Goals
These goals won't be considered for the initial MVP, but we'll record them here for future reference
* Calendar sync
* Remote (non-local) access

## References
* https://sqlite.org/
* SQLAlchemy
	* Tutorial https://docs.sqlalchemy.org/en/20/tutorial/index.html
* Beautiful Soup
	* bs4 docs https://www.crummy.com/software/BeautifulSoup/bs4/doc/
