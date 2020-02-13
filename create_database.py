import csv
import psycopg2
from psycopg2 import sql
import os.path

# Either create a super user with this name, or change superUser to match yours
superUser = 'postgres'
databaseName = 'earnup'
dataFile = './data/AB_NYC_2019.csv'
cleanDataFile = './data/AB_NYC_2019_CLEAN.csv'

# This table will be overwritten, so make sure you don't need data inside it.
tableName = 'rentals'
tableSQL = "CREATE TABLE {table} (\
        id INT PRIMARY KEY,\
        name TEXT,\
        host_id INT,\
        host_name TEXT,\
        neighbourhood_group TEXT,\
        neighbourhood TEXT,\
        latitude FLOAT,\
        longitude FLOAT,\
        room_type TEXT,\
        price INT,\
        minimum_nights INT,\
        number_of_reviews INT,\
        last_review DATE,\
        reviews_per_month FLOAT(2),\
        calculated_host_listings_count INT,\
        availability_365 INT\
        )"

# Assumes postgreSQL is running locally
conn = psycopg2.connect(host='localhost', dbname=superUser, user=superUser)

# Allows for creation of databases
conn.autocommit = True
cur = conn.cursor()

try:
    cur.execute(sql.SQL("CREATE DATABASE {database}").format(
        database=sql.Identifier(databaseName)
    ))
except psycopg2.DatabaseError: # If database already exists
    pass

cur.close()
conn.close()

conn = psycopg2.connect(host='localhost', dbname=databaseName, user=superUser)
conn.autocommit = True
cur = conn.cursor()

try:
    # Create a table with matching column headers
    cur.execute(sql.SQL(tableSQL).format(
        table=sql.Identifier(tableName)
    ))

# if table already exists, delete and create a new one
except psycopg2.DatabaseError:
    cur.execute(sql.SQL("DROP TABLE {table}").format(
        table=sql.Identifier(tableName)
    ))

    cur.execute(sql.SQL(tableSQL).format(
        table=sql.Identifier(tableName)
    ))    

if  not (os.path.isfile(cleanDataFile)):
    import clean_data
    clean_data.clean(dataFile)

with open(cleanDataFile, 'r', newline='') as f:
    next(f)
    # cur.copy_from(f, tableName, sep=",", null="")
    cur.copy_expert(
        sql.SQL("""COPY {table} FROM STDIN WITH (FORMAT CSV)""").format(
        table=sql.Identifier(tableName)
    ), f)