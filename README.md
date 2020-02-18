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

The applications' other dependencies are:

- Flask (used to run the server)
- flask_restful (a library to help create simple APIs)
- psycopg2 (Python software to integrate with PostgreSQL)
- requests (to send GET requests in get_request.py)

You can install these (and their own dependencies) using
`pip3 install -r requirements.txt`

## Setup

Before running the application for the first time, run `python3 setup.py`
This will clean up the provided data file and create a PostgreSQL database/table
for use. The script overwrites the "rentals" server on the "earnup" database so
make sure to save your data if that happens to be something you already have!

## Usage

After running setup.py, you can start the Flask server using:
`python3 rental.py`

Once the server is running, you can use another terminal window to send a GET
request using something like cURL:

`curl -X GET -d "query=skylit" -d "latitude=40.5" -d "longitude=-74" -d "distance=15" http://localhost:5000`

However, it may be more useful to you to use the included script get_request.py,
which will prompt you for parameters and use python's requests library to send
the request and print the information with proper indentation.

`python get_request.py`
