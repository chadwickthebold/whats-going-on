# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0] - 2026-05-01

### Added

- `web/` — Next.js 16 app (App Router, TypeScript, Tailwind CSS) initialized at `whats-going-on/web/`
- `web/app/page.tsx` — welcome page with link to `/events`
- `web/app/events/page.tsx` — events listing page; fetches from `GET /events` and renders a card per event
- `web/components/EventCard.tsx` — displays event title, type badge, formatted date, and source link
- `web/lib/types.ts` — TypeScript types for `EventResponse` and `PaginatedResponse<T>`
- `web/lib/api.ts` — `fetchEvents()` wrapper using plain `fetch`
- `web/lib/event-types.ts` — label and Tailwind badge color map for the five event types
- `web/.env.local` — `NEXT_PUBLIC_API_URL` pointing to the local FastAPI server
- `make web-dev` Makefile target — starts the Next.js dev server
- CORS middleware added to `server.py` — allows requests from `http://localhost:3000`

## [0.4.1] - 2026-04-30

### Changed

- `DrawingCenterParser` now extracts `source_url` from the exhibition detail page link; `BaseParser` accepts a `base_url` parameter passed in from `refresh.py` via `venue.website` so the full URL is constructed without hardcoding the hostname in the parser

## [0.4.0] - 2026-04-30

### Added

- `server.py` — FastAPI app with `GET /venues` and `GET /events` endpoints; Swagger UI at `/docs`
- `schemas.py` — `PaginatedResponse[T]` generic envelope, `VenueResponse`, and `EventResponse` Pydantic models
- `find_all(offset, limit)` and `count()` methods on `EventRepository` and `VenueRepository` in `data/repositories.py`
- `make dev` Makefile target — starts uvicorn with `--reload`
- `uvicorn` added as explicit project dependency

## [0.3.0] - 2026-04-30

### Added

- `data/database.py` — central engine construction, imported by `refresh.py` and future FastAPI server
- `data/repositories.py` — `EventRepository`, `VenueRepository`, and `DataSourceRepository`; all SQLAlchemy queries now live here; repositories do not call `session.commit()`
- `docs/data-management/data-management-patterns.md` — ADR establishing Pydantic schemas as the shared intermediate layer, repository pattern for DB access, and session lifecycle conventions

### Changed

- `refresh.py` refactored to use repositories exclusively; single `session.commit()` at end of run covers all writes including `DataSource.last_checked`
- `Event` model gains `source_url` column for stable dedup once parsers supply it; `is_passed` field removed (derived at query time from `event_start_timestamp`)
- `DrawingCenterParser` updated to remove `is_passed` from constructed `Event` objects

## [0.2.0] - 2026-04-29

### Added

- `DrawingCenterParser` in `parser/drawing_center.py` — parses `#onview` and `#upcoming` exhibit sections from Drawing Center HTML, returning candidate `Event` objects
- `HTMLParser` base class in `parser/parser.py` with abstract `parse(file_path) -> list[Event]` interface and `_load()` helper
- Slug-based parser dispatch in `refresh.py` via `PARSERS` dict
- Fetcher step in `refresh.py` — fetches data source URL and saves HTML to `tmp/<venue-slug>.html` before parsing
- Reconciler step in `refresh.py` — deduplicates events by title against existing DB records and inserts new events
- System diagram added to `docs/architecture.md`
- v0.2 and v1.0 milestones defined in `docs/milestones.md`

### Changed

- `Organization`, `DataSource` models added to `data/db_models.py`; `Venue` and `Event` models completed with all attributes and relationships
- `data/init_db.py` updated to import all four models and use a path relative to the script location
- Architecture doc models section updated to reflect concrete column names and types

## [0.1.0] - 2026-04-28

### Added

- Initial Makefile
- Basic DB model definitions
