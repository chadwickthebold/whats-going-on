# Architecture Plan

This doc will contain initial architectural design for the whats going on project.

## Libraries/tools
mise for tool management
poetry for python dependency management
fastapi for python service web framework
sqlite for data storage
tailwind css for styling
React + nextjs for the frontend
AWS for any infra (most likely won't be any)

## System Design

```
  ┌─────────────────────────────────────────────────────────────┐
  │                        Web Client                           │
  │                      (React / Next.js)                      │
  └────────────────────────────┬────────────────────────────────┘
                               │ HTTP
                               ▼
  ┌─────────────────────────────────────────────────────────────┐
  │                      FastAPI Server                         │
  │                                                             │
  │  ┌──────────────────┐    ┌───────────────────────────────┐  │
  │  │   Events API     │    │     Refresh Orchestrator      │  │
  │  │  (read / filter) │    │    (dispatched per venue)     │  │
  │  └────────┬─────────┘    └──────────────┬────────────────┘  │
  │           │                             │                   │
  │           │              ┌──────────────▼──────────────┐    │
  │           │              │  1. Fetcher                 │    │
  │           │              │     (HTTP GET data source)  ├────┼──► Venue Sites
  │           │              │                             │    │    (HTML / RSS)
  │           │              │  2. Venue Parser            │    │
  │           │              │     (BS4 / lxml)            │    │
  │           │              │                             │    │
  │           │              │  3. Reconciler              │    │
  │           │              │     (dedup + insert)        │    │
  │           │              └──────────────┬──────────────┘    │
  └───────────┼─────────────────────────────┼───────────────────┘
              │                             │
              ▼                             ▼
  ┌─────────────────────────────────────────────────────────────┐
  │                   SQLite (wgo.prod.db)                      │
  │        Organization → Venue → Event                         │
  │                   └─── DataSource                           │
  └─────────────────────────────────────────────────────────────┘
```

**Note** we're not initializing wgo.prod.db until we're more certain the data model
is locked - I don't want to deal with migrations until we're at v1.0

## Models

### Event
An event is our core model. An event has a title, a description, and occurs at a specific time and for a specific duration.

**Attributes**
* title
* short_description
* event_type (string: exhibition, performance, talk, screening, other)
* event_start_timestamp (datetime with timezone)
* duration_minutes (int)
* is_passed (bool)
* venue_id (FK → Venue)

### Venue
A Venue is where an event takes place.

**Attributes**
* name
* address
* website
* organization_id (FK → Organization)

### Organization
An organization can own multiple venues.

**Attributes**
* name

### Data Source
A data source is a source of information for event info. It represents a discrete feed of information such
as a calendar webpage, an rss feed, or a mailing list.

We'll start by modeling the types we encounter as we onboard new venues, and determine how to make this more
generic or specific in the future

A Data Source can be mapped either to a venue or an organization

**Attributes**
* url
* last_checked (datetime)
* venue_id (FK → Venue, nullable)
* organization_id (FK → Organization, nullable)

A data source is the core unit of work we process for our event extraction workflow.

## Workflow
Data Refresh should be idempotent, pulling multiple times shouldn't result in duplicate data

1. Pull venue data from DB
2. Determine data source types for venue (html, rss, email)
3. For each data source, create refresh workflow

Refresh workflow
1. Pull data from source target
2. Run extracted data through parser
3. Normalize data
4. Reconcile with saved data
5. Record workflow result

## Basic Workflow Example

1. Use requests to pull calendar URL
2. Use beautiful soup to extract events
3. Normalize found events to data model
4. Record in DB

## Data Management

Track long-live production data in a sqlite object wgo.prod.db

For local development we should be able to both start a db from scratch with the
most current schema from production, as well as copy data over from production
to test how future migrations will work.

## Future Ideas
* Retain a log of data refresh workflow runs for later debugging
* Calendar sync
* Remote (non-local) access
* Dispatch workflow processes asyncronously from the main server process