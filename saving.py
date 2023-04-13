import os
import json
import sqlite3
import requests
from weather import load_json

def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/' + db_name)
    cur = conn.cursor()
    return cur, conn
 
def make_health_table(health_data, cur, conn):
    locations = []
    for place in data['list']:
        location = place['location']
        if location not in locations:
            locations.append(location)
    
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS Locations(
        id INTEGER PRIMARY KEY,
        city_name TEXT,
        depression FLOAT,
        sleep FLOAT,
        lpa FLOAT
        )'''
    )
    conn.commit()


def make_weather_table(weather_data, cur, conn):
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS Weather(
        id INTEGER PRIMARY KEY,
        city_name TEXT,
        temp FLOAT,
        app_temp FLOAT,
        pressure FLOAT,
        uvi FLOAT,
        clouds FLOAT,
        weather INTEGER
        )'''
    )

def main():
    health_data = load_json("health_data.json")
    weather_data = load_json("weather_data.json")
    cur, conn = open_database("sun_health.db")
    make_health_table(health_data, cur, conn)
    make_weather_table(weather_data, cur, conn)
    conn.close()

if __name__ == "__main__":
    main()