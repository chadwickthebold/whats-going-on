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

Data will be persisted in a sqlite DB

Tasks can be dispatched in forked processes for the event processing workflow

An HTTP interface will be provided for a web application to provide a UI for interacting
with the service and initiating workflows.

## Models

### Event
An event is our core model. An event has a title, a description, and occurs at a specific time and for a specific duration.

**Attributes**
* EventType
* Duration
* EventStart
* is_passed

### Venue
A Venue is where an event takes place

**Attributes**
* Name
* Address
* Organization

### Organization
An organization can own multiple venues

**Attributes**
* Name

### Data Source
A data source is a source of information for event info. It represents a discrete feed of information such
as a calendar webpage, an rss feed, or a mailing list.

We'll start by modeling the types we encounter as we onboard new venues, and determine how to make this more
generic or specific in the future

**Attributes**
* URL
* Expected Update Cadence
* last_checked

A data source is the core unit of work we process for our event extraction workflow.

## Worklow
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

## Future Ideas
* Retain a log of data refresh workflow runs for later debugging
* Calendar sync
* Remote (non-local) access