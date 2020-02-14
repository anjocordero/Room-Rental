# Room Rental API

API endpoint which receives location data and text string, returning available
rooms for rent in NYC.

## Requirements

This implementation uses postgreSQL to manage data, which needs to be installed
on your computer prior to running this application.

This application requires that there be both a superuser and a database titled
"postgres" on your installation of PostgreSQL with permission to create
databases. This should be included by default when installing PostgreSQL,
but if not, create one on the command line using:

`createuser postgres --superuser`

## Setup

Before running the application for the first time, run `python3 setup.py`
This will clean up the provided data file and create a PostgreSQL database/table
for use.
