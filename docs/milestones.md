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



## v1.0

