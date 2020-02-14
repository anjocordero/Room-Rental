import json
import requests
import psycopg2
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

    def get(self):
        params = parser.parse_args()

        if not params:
            response = "No parameters given. Provide query or coordinates."
            status_code = 422
            return (response, status_code)

        if params['query']:
            """
            Cases:
                - L&L&D
                - L&L
                - None
                - Other
            """
            pass

        # if coordinates and no query
        elif params['latitude'] and params['longitude']:
            if params['distance']:
                self.cursor.execute(sql.SQL(
                    "SELECT * FROM {table} WHERE\
                    distance(\
                        latitude, longitude, {latitude}, {longitude})\
                    < {distance}\
                    ORDER BY\
                    distance(\
                        latitude, longitude, {latitude}, {longitude})").format(
                        # columns=sql.Identifier(sqlColumns),
                        table=sql.Identifier(tableName),
                        latitude=sql.Identifier(params['latitude']),
                        longitude=sql.Identifier(params['longitude']),
                        distance=sql.Identifier(params['distance'])
                        )
                )
                return json.dumps(self.cursor.fetchall(), default=str)

            # if no distance
            else:
                self.cursor.execute(sql.SQL(
                    "SELECT * FROM {table}\
                    ORDER BY\
                    distance(\
                        latitude, longitude, (%s), (%s))").format(
                        # columns=sql.Identifier(sqlColumns),
                        table=sql.Identifier(tableName)),
                        (params['latitude'], params['longitude'])
                    
                )
                return json.dumps(self.cursor.fetchall(), default=str)

        # distance only
        else:
            response = "Incorrect parameters given. Provide query or coordinates."
            status_code = 422
            return (response, status_code)

parser = reqparse.RequestParser()
parser.add_argument('query', type=str)
parser.add_argument('longitude', type=str)
parser.add_argument('latitude', type=str)
parser.add_argument('distance', type=str)

api.add_resource(QueryListing, "/")

if __name__ == '__main__':
    app.run(debug=True)
