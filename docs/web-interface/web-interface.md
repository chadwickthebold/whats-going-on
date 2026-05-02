# Web Interface — Technical Design

**Milestone:** v1.0
**Status:** Proposed
**Date:** 2026-05-01

---

## 1. Overview

This document specifies the design of the first working web client for "What's Going On." The client is a Next.js application that lets the user browse upcoming NYC cultural events, filter them by venue and event type, and trigger per-venue data refreshes that surface new events without reloading the page.

The scope is limited to the v1.0 acceptance criteria. The backend API is the FastAPI server running at `http://localhost:8000`.

---

## 2. Background and Design Clarifications

Before settling on specific approaches, three questions had material impact on the design:

**Is pagination needed in the UI for v1.0?**
No. The dataset is small — a handful of tracked NYC venues, each with on the order of 10–30 upcoming events. Loading all events in one request keeps the implementation simple and avoids building paginator UI or infinite scroll for no real user benefit at this scale. The API's default `limit` is 20; we will request with `limit=100` (the API maximum) and treat that as "all." If the dataset later grows beyond 100 events this can be revisited.

**Should filtering happen client-side or server-side?**
Server-side. The API will expose `venue_id` and `event_type` filter params on `GET /events`, and the frontend will pass the active filter values on each request. Backend changes to support filtering are in scope for v1.0.

**Does the refresh endpoint need to be fully specified here?**
The endpoint does not yet exist on the backend, so this document defines only the frontend contract: what request shape the UI sends, and how it handles loading/success/error states. The backend design for `POST /venues/{slug}/refresh` is out of scope for this document and should be specified as part of a separate backend design task before implementation begins on that feature.

---

## 3. Route / Page Structure

The application has a single route. There is no need for multiple pages in v1.0.

| Route | Component | Purpose |
|---|---|---|
| `/` | `EventsPage` | Lists all upcoming events; hosts filter controls and per-venue refresh triggers |

Detail views for individual events and venue profile pages are deferred to a future milestone. The route structure will be extended then.

**Why App Router over Pages Router?**
The App Router is the current Next.js default and the direction the framework is heading. For this project the distinction matters in one way: we will use `"use client"` components for the interactive parts (filters, refresh buttons) while keeping the outer shell as a server component. This is a natural fit for App Router. Pages Router offers no advantage here and would require opting into a legacy mental model. App Router is the right choice.

---

## 4. Component Hierarchy

Only top-level and meaningful mid-level components are described here. Leaf elements (individual event cards, spinner icons) are implementation details.

```
RootLayout                      — Next.js root layout; sets <html> and global Tailwind base
└── EventsPage                  — Server component; fetches initial data, composes the page
    ├── FilterBar                — Client component; venue and event-type filter controls
    │   ├── VenueFilter          — Multi-select or button group for venue filtering
    │   └── EventTypeFilter      — Multi-select or button group for event type filtering
    ├── VenueRefreshPanel        — Client component; lists venues with per-venue refresh buttons
    │   └── VenueRefreshButton   — Stateful button: idle / loading / success / error
    └── EventList                — Client component; renders filtered event cards
        └── EventCard            — Single event: title, type badge, date, venue name, source link
```

**Responsibilities:**

- `EventsPage` — The page shell. As a server component it handles the initial data fetch for both events and venues. It passes data down as props to client components.
- `FilterBar` — Reads and writes filter state (URL search params, per section 5). Emits no network requests itself.
- `VenueRefreshPanel` — Manages refresh state per venue. On completion it triggers a re-fetch of the events list.
- `EventList` — Derives the displayed event list from the full fetched list plus the current filter state. All filtering logic lives here.
- `EventCard` — Pure display. Formats the timestamp to a human-readable local date/time. Renders a link to `source_url` when present.

---

## 5. Data Fetching Strategy

**Decision: Plain `fetch` — no data fetching library**

Libraries like SWR and TanStack Query exist to handle deduplication of simultaneous requests, cross-component caching, background revalidation on tab focus, and retry logic. None of these concerns apply to a personal local tool with one user and one page.

Plain `fetch()` inside `useEffect` + `useState` is sufficient. Events and venues are fetched on mount; events are re-fetched after a successful venue refresh. This aligns with the project principle of avoiding unnecessary dependencies.

**Fetch pattern:**

```
GET /events?limit=100    → all upcoming events
GET /venues?limit=100    → all venues (to populate filter options and resolve venue names)
```

Both fetches are initiated in the top-level `EventsPage` client component on mount. When filter state changes, the events fetch is re-issued with the updated params. Re-fetch of events is also triggered after a successful refresh POST.

**API base URL:**

During local development the backend is at `http://localhost:8000`. This is configured via a single `NEXT_PUBLIC_API_URL` environment variable in `.env.local`. No other environment configuration is needed for v1.0.

---

## 6. State Management

**Recommendation: URL search params for filter state**

Filter state (selected venues, selected event types) is stored in URL search params rather than React local state (`useState`).

**Why URL params:**

- The filtered view is bookmarkable and shareable, which is a small but real quality-of-life benefit even for a personal tool
- Filters survive a page refresh, which feels correct — if you've filtered to "Pioneer Works / performance" you expect that to persist while you're looking at it
- Next.js App Router provides `useSearchParams()` and `useRouter()` for reading and writing search params without external libraries
- The implementation is no more complex than `useState` for this case

**Why not `useState`:**

- Filter state is lost on hard reload
- Back-button behavior becomes confusing (back clears filters, which is unexpected)

**Param shape:**

```
/?venue=drawing-center&venue=pioneer-works&type=performance&type=talk
```

Multi-value params use repeated keys. Absent param means "no filter applied" (show all). The `FilterBar` component reads `useSearchParams()` and updates the URL via `router.replace()` on each change (not `router.push()`, so filter changes don't clutter browser history).

**Refresh trigger state** is kept in local component state inside `VenueRefreshButton`. It is ephemeral UI state — there is no reason to persist it in the URL or lift it higher.

---

## 7. Refresh Trigger Flow

The per-venue refresh is the most interactive part of the application. The flow is:

**Step 1 — User triggers refresh**

Each venue in `VenueRefreshPanel` has a "Refresh" button. Clicking it sends:

```
POST /venues/{slug}/refresh
```

The button immediately transitions to a loading state (spinner, disabled). No optimistic update is made to the event list — we wait for the refresh to complete before re-fetching.

**Step 2 — Backend processes the refresh**

The backend runs the Fetcher → Parser → Reconciler pipeline for the venue and returns when done. The response signals success or failure.

Expected responses:
- `202 Accepted` — refresh accepted; body may include a workflow reference ID for future async tracking
- `4xx / 5xx` — error; body includes a message

The frontend treats any `2xx` response as success and shows a generic "Done." The workflow reference ID is ignored for v1.0 but leaves the door open for async refresh tracking in a later milestone.

**Step 3 — Re-fetch events on success**

On a `2xx` response, `VenueRefreshButton` triggers a re-fetch of the events list (same fetch function used on mount). The `EventList` updates when the new data arrives — no page reload required.

The button transitions to a brief "Done" success state (2–3 seconds) then returns to idle.

**Step 4 — Error handling**

On a non-200 response, the button transitions to an error state showing a short message ("Refresh failed"). It returns to idle after a few seconds or on the next click. No toast library is needed — inline state on the button is sufficient.

**UX state machine for `VenueRefreshButton`:**

```
idle → loading (on click)
loading → success (on 2xx)
loading → error (on non-200 or network failure)
success → idle (after 2.5s)
error → idle (after 3s or on next click)
```

---

## 8. Tailwind Conventions

Tailwind CSS is the only styling mechanism. No custom CSS files will be added for v1.0.

- **Utility-first throughout.** No `@apply` directives; no CSS modules; no styled-components. All styles are inline utility classes.
- **No design system overhead.** A `tailwind.config.js` exists only to set `content` paths. No custom theme tokens, no extended color palette, no plugin configuration.
- **Responsive breakpoints if needed.** The app is primarily used on desktop. A single responsive breakpoint (`md:`) may be used to adjust layout on smaller screens, but this is not a v1.0 requirement.
- **Event type color coding.** The five event types (`exhibition`, `performance`, `talk`, `screening`, `other`) each get a distinct Tailwind badge color. These are hardcoded as a small map in a utility file (`lib/event-types.ts`) rather than stored in config — consistent with the no-premature-abstraction principle.

---

## 9. Project Structure

**Recommendation: Sibling directory to the FastAPI backend**

The Next.js app lives at `web/` as a sibling to the backend Python files in the project root, within the same git repository.

```
whats-going-on/
├── web/                        ← Next.js application root
│   ├── app/
│   │   ├── layout.tsx          ← RootLayout
│   │   ├── page.tsx            ← EventsPage (server component shell)
│   │   └── globals.css         ← Tailwind @tailwind directives only
│   ├── components/
│   │   ├── EventCard.tsx
│   │   ├── EventList.tsx
│   │   ├── EventTypeFilter.tsx
│   │   ├── FilterBar.tsx
│   │   ├── VenueFilter.tsx
│   │   ├── VenueRefreshButton.tsx
│   │   └── VenueRefreshPanel.tsx
│   ├── lib/
│   │   ├── api.ts              ← typed fetch wrappers for /events and /venues
│   │   ├── event-types.ts      ← event type labels and badge colors
│   │   └── hooks/
│   │       ├── useEvents.ts
│   │       └── useVenues.ts
│   ├── .env.local              ← NEXT_PUBLIC_API_URL=http://localhost:8000
│   ├── next.config.ts
│   ├── package.json
│   ├── postcss.config.js
│   └── tailwind.config.js
├── server.py                   ← FastAPI entry point
├── schemas.py
├── data/
├── parser/
├── docs/
├── Makefile
└── pyproject.toml
```

**Why sibling directory, not a separate repo or monorepo root:**

- Same git repository keeps frontend and backend changes in the same commit, which is appropriate for a personal tool where both sides evolve together
- A separate repo would add overhead (two `git pull`s, two separate issues lists) with no real benefit at this scale
- A monorepo tool (Turborepo, Nx) is overkill — there are no shared packages between Python and JavaScript, so "monorepo" here just means "two directories in one repo"
- The Python tooling (`poetry`, `mise`) is not affected by adding a `web/` subdirectory

**Makefile integration:**

Add a `web-dev` target to the Makefile:

```makefile
web-dev:
    cd web && npm run dev
```

This keeps the same ergonomics as `make dev` for the backend.

---

## 10. Key Trade-offs Considered

### Trade-off 1: Server-side filtering vs. client-side filtering

**Chosen:** Server-side filtering — `GET /events` will accept `venue_id` and `event_type` query params, and the frontend re-fetches when filters change.

**Alternative:** Fetch all events once and filter locally in the browser.

**Reasoning:** Backend changes are in scope for v1.0. Server-side filtering is the correct long-term pattern and avoids sending unnecessary data to the client as the dataset grows.

### Trade-off 2: Plain `fetch` vs. a data fetching library (SWR, TanStack Query)

**Chosen:** Plain `fetch()` with `useEffect` + `useState`.

**Alternative:** SWR or TanStack Query for request deduplication, caching, and automatic revalidation.

**Reasoning:** Those libraries exist to solve problems — deduplication, cross-component caching, background revalidation — that don't apply to a personal local tool with one user and one page. Plain `fetch` is sufficient and adds no dependencies, consistent with the project principle of avoiding unnecessary packages.

### Trade-off 3: URL params vs. local state for filter state

**Chosen:** URL search params via `useSearchParams()` and `router.replace()`.

**Alternative:** `useState` in `FilterBar`, with filter state passed down as props to `EventList`.

**Reasoning:** URL params win on behavior: filters survive a hard reload, the back button doesn't clear them, and a filtered view can be bookmarked. The implementation complexity over `useState` is minimal.
