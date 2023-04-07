import json
import requests
import sqlite3
import matplotlib.pyplot as plt


def write_json(filename, dict): 
    with open(filename, "w") as fhand:
        fhand.write(json.dumps(dict))


def get_api(url, params):
    r = requests.get(url, params)
    dis_data = r.json()


def get_lat():
    coor_list = []
    who_url = "https://chronicdata.cdc.gov/resource/cj8b-94cj.json"
    lat = get_api(who_url, None)
    for region_dic in lat:
        coor = region_dic["geolocation"]["coordinates"]
        coor_rounded = round(coor, 6)
        coor_list.append()
    return coor_list     # a list


def cache_weather(loc_list, filename):
    weather_d = {}
    base = "https://api.openweathermap.org/data/3.0/onecall/timemachine"
    # for i in range(25):
    for i in loc_list:
        dic = {"lat":i[0], "lon":i[1], "dt":"2000", "appid":'''API key'''}
        result = get_api(base, dic)
        weather_d[(i[0],i[1])] = result["results"]
    write_json(filename, weather_d)
    # count function of sql

def main():
    loc_list = get_lat()
    cache_weather(loc_list, "weather_data.json")


if __name__ == "__main__":
    main()
