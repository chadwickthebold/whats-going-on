# Development Principles

General rules to follow while working on this project

* Prefer min-age for dependency updates to be at last 7d to allow for security
issues to be uncovered
* Ensure all timestamps are TZ-aware (relative to event, or UTC if non-event-specific)
* Avoid 3rd party packages where possible, except for the really complicated stuff where reimplementation would be unfeasible
