# Milestones

This document will track our series of project milestones, allowing us to land features in an incremental way.
Once a milestone is marked complete, it should not be updated. Refinements to project architecture should be
added in sub-milestones (following major.minor.patch version numbering)

Compare to the changelog before reviewing this document to ensure you're looking at the current WIP milestone

## Format

```
## v0.1 (target release version)

(Summary of functionality added in this milestone. Include context about changes to project architecture,
patterns introduced, changes to library utlization, and other major architectural points)

**Definition of Done**
(Bullet point list of acceptance criteria for milestone)

**TODO**
- [ ] Item 1
- [ ] Item 2
```

## v0.1

Create initial database scaffolding. Use sqlalchemy to create class definitions for our core models.
Use these models to create a local migration script that can initialze an empty database with the schema
required from our configured sqlalchemy models.

**Definition of Done**
* sqlalchemy models defined in data/db_models.py that match models outlined in project architecture
* Running `make empty-db` causes a new db wgo.local.db to be created in the `/data` dir with the 
schema required to support the defined sqlalchemy models

## v0.2

Create a working end-to-end refresh pipeline for a single venue (The Drawing Center). This milestone proves
out the full Fetcher → Parser → Reconciler flow and results in real events written to the local database.

Introduces venue-specific parser modules under `parser/`, porting the existing `scrape_drawingcenter.py`
proof-of-concept into a structured `DrawingCenterParser` class. Seed data for the venue and its data source
URL must exist in the DB for the workflow to run.

**Definition of Done**
* `DrawingCenterParser` implemented in `parser/` and extracts events from Drawing Center HTML
* `refresh.py` dispatches to the correct parser based on venue and writes new events to the DB
* Seed data script populates Drawing Center venue and data source
* Running `python refresh.py drawing-center` results in events inserted into `wgo.local.db` with no duplicates on subsequent runs

## v0.3

Establish data management patterns and refactor the refresh pipeline to follow them. Introduces an Architecture Decision Record (ADR) at `docs/data-management/data-management-patterns.md` that defines three conventions: Pydantic schemas as the shared intermediate layer between parsers and persistence, a repository pattern for all DB access, and a clear session lifecycle where the caller owns the transaction boundary.

Implements these patterns in code: engine construction moves to `data/database.py`; `data/repositories.py` introduces `EventRepository`, `VenueRepository`, and `DataSourceRepository`; `refresh.py` is refactored to use repositories with a single commit at the end covering all writes for a run. The `Event` model gains a `source_url` column (the dedup key once parsers supply it) and drops `is_passed`, which is now derived at query time from `event_start_timestamp`.

**Definition of Done**
* ADR written at `docs/data-management/data-management-patterns.md` covering Pydantic schemas, repository pattern, and session lifecycle
* `data/database.py` exports the SQLAlchemy engine
* `data/repositories.py` implements `EventRepository`, `VenueRepository`, and `DataSourceRepository` with no inline queries; repositories do not call `session.commit()`
* `refresh.py` uses repositories exclusively; session commit is a single call after all writes complete
* `Event` ORM model has `source_url` column; `is_passed` field removed
* `python refresh.py drawing-center` inserts events on first run and 0 events on subsequent runs

## v0.4

Introduces the FastAPI server layer with two read endpoints and automatic Swagger documentation. The server exposes a paginated `GET /venues` and `GET /events` endpoint, both returning a consistent envelope with `total`, `limit`, `offset`, and `items`. This milestone proves out the full data path from SQLite through the repository layer to a JSON HTTP response, and establishes the `schemas.py` Pydantic layer called for in the data management ADR.

Adds `find_all(offset, limit)` and `count()` methods to `EventRepository` and `VenueRepository`. Introduces `server.py` as the FastAPI entry point with per-request session injection via `Depends(get_db)`. Swagger UI is available at `/docs` with no additional configuration.

**Definition of Done**
* `GET /venues` returns a paginated list of venues with `total`, `limit`, `offset`, and `items`
* `GET /events` returns a paginated list of events with the same envelope
* Both endpoints accept `offset` and `limit` query parameters
* `schemas.py` defines `PaginatedResponse[T]`, `VenueResponse`, and `EventResponse` as Pydantic models
* Swagger UI loads at `http://localhost:8000/docs`
* `make dev` starts the server with hot reload

## v0.5

Bootstraps the Next.js frontend stack. Introduces a `web/` directory containing a Next.js 16 app (App Router, TypeScript, Tailwind CSS) served alongside the existing FastAPI backend. Proves out the full browser-to-API data path: the `/events` page fetches from `GET /events` and renders a list of event cards with title, type badge, formatted date, and source link. A welcome page at `/` links through to `/events`. CORS middleware is added to the FastAPI server to allow requests from the Next.js dev server.

**Definition of Done**
* `web/` directory initialized with Next.js 16, TypeScript, and Tailwind CSS
* `GET /events` is called from the browser and events are rendered at `/events`
* Event cards display title, event type badge, formatted date, and source link
* Root `/` displays a welcome message with a link to `/events`
* `make web-dev` starts the Next.js dev server
* No CORS errors when the frontend calls the FastAPI backend

## v1.0

First fully working product with a UI. Introduces the FastAPI server layer and a React/Next.js web client.
Users can browse upcoming events through the web UI and trigger a data refresh via the server.

The server exposes the Events API (read/filter) and a refresh endpoint that invokes the orchestrator.
The web client consumes these endpoints to display events, filterable by venue or event type.
Refresh is triggered on a venue-basis.

**Definition of Done**
* FastAPI server runs locally and exposes endpoints for listing events and triggering a venue refresh
* React/Next.js web client displays a list of upcoming events fetched from the server
* Events can be filtered by venue and/or event type in the UI
* Refresh can be triggered from the UI and reflects new events without a page reload

