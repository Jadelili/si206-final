import json
import requests
import sqlite3
import matplotlib.pyplot as plt

def load_json(filename):
    try:
        fhand = open(filename, "r")
        string = fhand.read()    
        fhand.close()
        d = json.loads(string)

    except:
        d = {}
    # print(d)
    return d


def write_json(filename, dict): 
    with open(filename, "w") as fhand:
        fhand.write(json.dumps(dict))


def get_api(url, params):
    r = requests.get(url, params)
    health_json = r.json()
    # health_data = json.load(r.content)
    return health_json


def cache_health_data(filename):
    health_dic = []
    who_url = "https://chronicdata.cdc.gov/resource/cj8b-94cj.json"
    health_list = get_api(who_url, None)
    write_json(filename, health_list)


def get_lat(filename):
    loc_list = load_json(filename)
    coor_list = []
    for region_dic in loc_list:
        coor = region_dic["geolocation"]["coordinates"]
        coor_rounded = round(coor, 6)
        coor_list.append()
    return coor_list     # a list


def cache_weather(coor_list, filename):
    weather_d = {}
    base = "https://api.openweathermap.org/data/3.0/onecall/timemachine"
    # for i in range(25):
    for i in coor_list:
        dic = {"lat":i[0], "lon":i[1], "dt":"2000", "appid":"0ed702778efe831f0e3d546dc34eece3"}
        result = get_api(base, dic)
        weather_d[(i[0],i[1])] = result["results"]
    write_json(filename, weather_d)
    # count function of sql

def main():
    ### cache_health_data("health_data.json")
    loc_list = get_lat()
    cache_weather(loc_list, "weather_data.json")


if __name__ == "__main__":
    main()
