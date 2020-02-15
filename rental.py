import json
import requests
import psycopg2
from flask import Flask
from psycopg2 import sql
from flask_restful import Api, Resource, reqparse
from config import super_user, database_name, clean_data_file,\
    table_name, postgres_host, postgres_port, sql_columns, columns

app = Flask(__name__)
api = Api(app)

class QueryListing(Resource):

    def __init__(self):
        # Assumes postgreSQL is running locally
        # Ensure you have a super_user matching super_user
        self.connection = psycopg2.connect(
            host=postgres_host, port=postgres_port,
            dbname=database_name, user=super_user
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
            if params['latitude'] and params['longitude']:
                if params['distance']:
                    self.cursor.execute(sql.SQL(
                        '''
                        SELECT * from {table} WHERE
                            name ILIKE %(query)s AND distance(
                                latitude, longitude, %(latitude)s, %(longitude)s) < %(distance)s
                            ORDER BY distance(
                                latitude, longitude, %(latitude)s, %(longitude)s)
                        ''').format(
                            columns=sql.Identifier(sql_columns),
                            table=sql.Identifier(table_name)),
                            {
                                'query': '%'+params['query']+'%',
                                'latitude': params['latitude'],
                                'longitude': params['longitude'],
                                'distance': params['distance']
                            }
                    )
                    return json.dumps(self.cursor.fetchall(), indent=2, default=str)
                # if no distance
                else:
                    self.cursor.execute(sql.SQL(
                        '''
                        SELECT * from {table} WHERE
                            name ILIKE %s
                                ORDER BY distance(
                                latitude, longitude, %(latitude)s, %(longitude)s)
                        ''').format(
                            columns=sql.Identifier(sql_columns),
                            table=sql.Identifier(table_name)),
                            ('%'+params['query']+'%',)
                    )
                    return json.dumps(self.cursor.fetchall(), indent=2, default=str)

            # if query and no coordinates
            else:
                self.cursor.execute(sql.SQL(
                    '''
                    SELECT * from {table} WHERE
                        name ILIKE %s
                    ''').format(
                        columns=sql.Identifier(sql_columns),
                        table=sql.Identifier(table_name)),
                        ('%'+params['query']+'%',)
                )
                return zip_results(self.cursor.fetchall())

        # if coordinates and no query
        elif params['latitude'] and params['longitude']:
            if params['distance']:
                self.cursor.execute(sql.SQL(
                    '''
                    SELECT * FROM {table} WHERE\
                    distance(\
                        latitude, longitude, %(latitude)s, %(longitude)s)\
                    < %(distance)s\
                    ORDER BY\
                    distance(\
                        latitude, longitude, %(latitude)s, %(longitude)s)
                    ''').format(
                        columns=sql.Identifier(sql_columns),
                        table=sql.Identifier(table_name)),
                        {
                            'latitude': params['latitude'],
                            'longitude': params['longitude'],
                            'distance': params['distance']
                        }
                        
                )
                return json.dumps(self.cursor.fetchall(), indent=2, default=str)

            # if no distance
            else:
                self.cursor.execute(sql.SQL(
                    '''
                    SELECT * FROM {table}\
                    ORDER BY\
                    distance(\
                        latitude, longitude, %(latitude)s, %(longitude)s)
                    ''').format(
                        columns=sql.Identifier(sql_columns),
                        table=sql.Identifier(table_name)),
                        {
                            'latitude': params['latitude'],
                            'longitude': params['longitude']
                        }
                    
                )
                return json.dumps(self.cursor.fetchall(), indent=2, default=str)

        # distance only
        else:
            response = "Incorrect parameters given. Provide query or coordinates."
            status_code = 422
            return (response, status_code)

def zip_results(rows):
    results = []
    for row in rows:
        results.append(dict(zip(columns, row)))
    return json.dumps(results, indent=2, default=str)

parser = reqparse.RequestParser()
parser.add_argument('query', type=str)
parser.add_argument('longitude', type=str)
parser.add_argument('latitude', type=str)
parser.add_argument('distance', type=str)

api.add_resource(QueryListing, "/")

if __name__ == '__main__':
    app.run(debug=True)
