import requests
import json
from config import postgres_host, postgres_port, flask_port

class Query():
    def __init__(self):
        self.query = input("Enter search text: ")
        self.latitude = input("Enter latitude: ")
        self.longitude = input("Enter longitude: ")
        self.distance = input("Enter distance from coordinates in miles: ")

    def build_query(self):
        query = {}
        if self.query:
            query['query'] = self.query
        if self.latitude:
            query['latitude'] = self.latitude
        if self.longitude:
            query['longitude'] = self.longitude
        if self.distance:
            query['distance'] = self.distance
        return query

def main():

    q = Query()
    r = requests.get("http://" + postgres_host + ":" + flask_port, q.build_query())
    print(r.json())
    return r.json()

if __name__ == "__main__":
    main()