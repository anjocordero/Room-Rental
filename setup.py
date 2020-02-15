import csv
import psycopg2
from psycopg2 import sql
import os.path
from config import super_user, database_name, postgres_host, data_file,\
                    clean_data_file, table_name, tableSQL, distanceSQL

conn = psycopg2.connect(host=postgres_host, dbname=super_user, user=super_user)

# Allows for creation of databases
conn.autocommit = True
cur = conn.cursor()

# Create new database if it doesn't already exist
try:
    cur.execute(sql.SQL("CREATE DATABASE {database}").format(
        database=sql.Identifier(database_name)
    ))
except psycopg2.DatabaseError:
    pass

cur.close()
conn.close()

# Switch to newly created database
conn = psycopg2.connect(host=postgres_host, dbname=database_name, user=super_user)
conn.autocommit = True
cur = conn.cursor()

# Create a table with matching column headers
try:
    cur.execute(sql.SQL(tableSQL).format(
        table=sql.Identifier(table_name)
    ))

# if table already exists, delete and create a new one
except psycopg2.DatabaseError:
    cur.execute(sql.SQL("DROP TABLE {table}").format(
        table=sql.Identifier(table_name)
    ))

    cur.execute(sql.SQL(tableSQL).format(
        table=sql.Identifier(table_name)
    ))    

# Create distance function for use later on
cur.execute(distanceSQL)

# Create clean data file if it doesn't already exist
# NOTE: if "clean" data file exists but is not clean then import will fail
if  not (os.path.isfile(clean_data_file)):
    import clean_data
    clean_data.clean(data_file)

with open(clean_data_file, 'r', newline='') as f:
    next(f)
    # cur.copy_from(f, table_name, sep=",", null="")
    cur.copy_expert(
        sql.SQL("""COPY {table} FROM STDIN WITH (FORMAT CSV)""").format(
        table=sql.Identifier(table_name)
    ), f)