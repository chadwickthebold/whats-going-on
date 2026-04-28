This doc will contain initial architectural design for the whats going on service.

mise
python
fastapi
sqlite for data storage
tailwind css for styling
React + nextjs for the frontend
AWS for any infra

## Scraping Process

1. Use requests to pull calendar URL
2. Use beautiful soup to extract upcoming events
3. Normalize found events to data model
4. Record in DB

## Data Models

* Venue
	* Name
	* Address
	* Organization
* Organization
	* Name
* Event
	* EventType
	* Duration
	* EventStart
	* is_passed
* EventType
* EventTypeVenueMapping
