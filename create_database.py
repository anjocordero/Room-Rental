import psycopg2
from psycopg2 import sql

# Either create a super user with this name, or change this to match yours
superUser = 'postgres'

databaseName = 'earnup'
dataFile = './data/AB_NYC_2019.csv'
tableName = 'rentals'

conn = psycopg2.connect(host='localhost', dbname=superUser, user=superUser)
# Allows for creation of databases
conn.autocommit = True
cur = conn.cursor()

# # Create an example user on the database
# cur.execute(sql.SQL("CREATE USER {user}").format(
#     user=sql.Identifier(databaseName)
# ))

# # Give user permission to create database
# cur.execute(sql.SQL("ALTER USER {user} CREATEDB").format(
#     user=sql.Identifier(databaseName)
# ))

cur.execute(sql.SQL("CREATE DATABASE {database}").format(
    database=sql.Identifier(databaseName)
))

cur.close()
conn.close()

conn = psycopg2.connect(host='localhost', dbname=databaseName, user=superUser)
conn.autocommit = True
cur = conn.cursor()

# Unfortunately, couldn't automatically grab header row while still specifying
# variable types.
cur.execute(sql.SQL("CREATE TABLE {table} (id int primary key,name text,\
    host_id int,host_name text,neighbourhood_group text,neighbourhood text,\
    latitude float,longitude float,room_type text,price int,minimum_nights int,\
    number_of_reviews int,last_review date,reviews_per_month float(2),\
    calculated_host_listings_count int,availability_365 int)").format(
    table=sql.Identifier(tableName)
))

with open(dataFile, 'r') as f:
    next(f)
    cur.copy_from(f, tableName, sep=',', null=None)