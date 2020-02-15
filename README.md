# Room Rental API

API endpoint which receives location data and a search string, returning available
rooms for rent, using data from NYC in 2019.

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
for use. The script overwrites the "rentals" server on the "earnup" database so
if that happens to be something you already have make sure to save your data!

## Usage

You can start the Flask server using:
`python3 rental.py`

The get_request.py script can be used in a separate instance to send a get request
to the server. The script prompts you for information so that you don't have to
format it yourself, however you could also send a request using something like
cURL.
