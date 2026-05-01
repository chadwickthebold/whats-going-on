# Data Management Patterns

## Status: Accepted

## Context

The project has one data model layer: SQLAlchemy ORM classes in `data/db_models.py`. As written, the parser layer imports ORM types directly, coupling HTML extraction to database concerns. `refresh.py` then mutates returned ORM objects post-parse to inject DB-specific fields (`venue_id`) — an implicit contract that is easy to break silently.

As the project adds a reconciler module, workflow orchestration, and a FastAPI server layer, this coupling will compound. Ad-hoc SQLAlchemy session usage will spread across modules without a clear ownership boundary.

---

## Decisions

### 1. Pydantic schemas as the shared intermediate layer

Declare Pydantic as an explicit direct dependency in `pyproject.toml`. (It is already present as a transitive dependency via FastAPI.) Create a top-level `schemas.py` to hold all Pydantic models.

**Why Pydantic:**
- FastAPI (planned for v1.0) requires Pydantic for request/response models — this is not a net-new dependency
- Pydantic models provide validation and clear field contracts with minimal boilerplate, compared to stdlib dataclasses
- The development principle to avoid unnecessary 3rd-party dependencies is satisfied: Pydantic is unavoidable given FastAPI

**`ParsedEvent` is the parser-to-reconciler contract.** It carries exactly what a parser can extract from a source document:

```python
class ParsedEvent(BaseModel):
    title: str
    event_type: EventType | None
    event_start_timestamp: datetime | None
    source_url: str | None  # detail page URL; used as the primary dedup key
    short_description: str | None
```

All fields except `title` are optional to accommodate parsers that cannot reliably extract them. Venue association is not a field on `ParsedEvent` — it is injected by the reconciler based on the data source being processed.

**`schemas.py` as neutral ground:**
- `ParsedEvent` and other intermediate pipeline types belong in `schemas.py`, not in `parser/` or `data/`
- Future modules — reconciler, workflow, server routes — all import from this neutral location with no cross-module awkwardness
- FastAPI API response models also go in `schemas.py` when the server layer is built
- When `schemas.py` grows beyond two or three unrelated model groups, split it into `schemas/parsed.py` (pipeline types) and `schemas/api.py` (response types)

**ORM objects remain the persistence layer only:**
- `data/db_models.py` SQLAlchemy models are the source of truth for the DB schema
- ORM objects are constructed and managed by repositories (see below); they do not travel up into parsing or workflow logic

**`is_passed` is not stored.** Whether an event is in the past is derived at query or display time by comparing `event_start_timestamp` to the current date. It is not a field on `ParsedEvent` and should not be written to the DB.

### 2. Repository pattern for DB access

Create `data/repositories.py` with repository classes for each model area. Each repository takes a SQLAlchemy `Session` in its constructor and exposes domain-meaningful methods.

All SQLAlchemy queries live in repositories. No inline `session.execute()` or `session.add()` calls in `refresh.py`, workflow code, or server routes.

```python
# data/repositories.py
class EventRepository:
    def __init__(self, session: Session): ...
    def source_urls_for_venue(self, venue_id: int) -> set[str]: ...
    def save(self, event: Event) -> None: ...

class VenueRepository:
    def __init__(self, session: Session): ...
    def find_by_slug(self, slug: str) -> Venue | None: ...

class DataSourceRepository:
    def __init__(self, session: Session): ...
    def find_by_venue(self, venue_id: int) -> list[DataSource]: ...
    def mark_checked(self, source: DataSource) -> None: ...
```

**Repositories return `None` (or empty collections) when records are not found; they do not raise exceptions.** Callers interpret `None` as a domain error — an HTTP 404 in a server route, a workflow abort in the refresh pipeline.

### 3. Session lifecycle

The SQLAlchemy engine is constructed once in `data/database.py` and imported by any caller that needs to create a session. **Repositories never call `session.commit()`.** Commit is the responsibility of the caller, so that multiple repository writes within one operation are atomic.

In the refresh workflow, the workflow runner opens a session and commits after all writes for that run complete:

```python
with Session(engine) as session:
    event_repo = EventRepository(session)
    source_repo = DataSourceRepository(session)

    event_repo.save(event)
    source_repo.mark_checked(source)

    session.commit()  # one commit — both writes atomic
```

In the FastAPI server, a per-request session is injected via `Depends(get_db)`. The route handler commits on success; the dependency closes the session on exit.

---

## Layer Model

```
HTML / RSS
    │
    ▼
[ Parser ]  ──►  ParsedEvent  (schemas.py, Pydantic)
                      │
                      ▼
             [ Reconciler ]        ← owns ParsedEvent → ORM mapping and dedup
                      │
                      ▼
           [ Workflow / Orchestrator ]  ← sequences fetcher, parser, reconciler
                      │
                      ▼
              [ Repository ]  ──►  Event ORM  (data/db_models.py)
                      │
                      ▼
                   SQLite
```

Each layer has a single direction of dependency:
- Parsers produce Pydantic schemas; they know nothing about the DB
- The reconciler converts `ParsedEvent` → `Event` ORM and delegates persistence to repositories
- The workflow orchestrator sequences the steps and owns the session transaction boundary
- Repositories own all ORM construction and session interactions

---

## Consequences

- An explicit mapping step in the reconciler converts `ParsedEvent` → `Event` ORM. This is intentional — it is the seam between parsed data and persisted data
- Deduplication uses `source_url` as the primary key; title is the fallback when `source_url` is `None`. This requires `Event` to carry a `source_url` column
- Repository classes are thin query wrappers with no business logic
- As new venue parsers are added, they return the same `ParsedEvent` schema — no new DB coupling required per parser
- When the FastAPI server is introduced, API response schemas are added to `schemas.py` alongside `ParsedEvent`; split into sub-modules when the file grows beyond two or three unrelated groups
