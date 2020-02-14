import json
import requests
import psycopg2
import geopy.distance
from flask import Flask
from psycopg2 import sql
from flask_restful import Api, Resource, reqparse
from config import superUser, databaseName, cleanDataFile,\
    tableName, postgres_host, postgres_port, sqlColumns

app = Flask(__name__)
api = Api(app)

class QueryListing(Resource):

    def __init__(self):
        # Assumes postgreSQL is running locally
        # Ensure you have a superuser matching superUser
        self.connection = psycopg2.connect(
            host=postgres_host, port=postgres_port,
            dbname=databaseName, user=superUser
        )
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()

    def get(self, params={}):

        if params:
            # Either text query or coordinates are required
            if params['query'] or (params['latitude'] and params['longitude']):
                
                if params['query']:
                    pass
                else:    

                    if params['distance']:
                        self.cursor.execute(sql.SQL(
                            "SELECT {columns} FROM {table} WHERE\
                            distance(\
                                latitude, longitude, {latitude}, {longitude})\
                            < {distance}\
                            ORDER BY\
                            distance(\
                                latitude, longitude, {latitude}, {longitude})".format(
                                columns=sql.Identifier(sqlColumns),
                                latitude=sql.Identifier(params['latitude']),
                                longitude=sql.Identifier(params['longitude']),
                                distance=sql.Identifier(params['distance'])
                            )
                        ))
                    # If distance not provided
                    else:
                        self.cursor.execute(sql.SQL(
                            "SELECT {columns} FROM {table}\
                            ORDER BY\
                            distance(\
                                latitude, longitude, {latitude}, {longitude})".format(
                                columns=sql.Identifier(sqlColumns),
                                latitude=sql.Identifier(params['latitude']),
                                longitude=sql.Identifier(params['longitude']),
                                distance=sql.Identifier(params['distance'])
                            )
                        ))
                        self.cursor

                # # TODO: Implement appropriate SQL queries
                # self.cursor.execute(sql.SQL(
                #     "SELECT * FROM {table}"
                #     ).format(
                #     table=sql.Identifier(tableName)
                # ))
                # return json.dumps(self.cursor.fetchone(), default=str)
            
            else:
                response = "Incorrect format given. Provide query or latitude and longitude."
                status_code = 422
                return (response, status_code)

        response = "No parameters given."
        status_code = 422
        return (response, status_code)

    def findNearby(self, latitude, longitude, distance=None):
        self.cursor.execute(sql.SQL("SELECT * FROM {table}").format(
            table=sql.Identifier(tableName)
        ))

api.add_resource(QueryListing, "/")
app.run(debug=True)