import json
import requests
import sqlite3
import urllib
import matplotlib.pyplot as plt

def load_json(filename):
    try:
        fhand = open(filename, "r")
        string = fhand.read()    
        fhand.close()
        d = json.loads(string)

    except:
        d = {}
    return d


def write_json(filename, dict): 
    with open(filename, "w") as fhand:
        fhand.write(json.dumps(dict))


def get_api(url, params):
    r = requests.get(url, params)
    health_json = r.json()
    return health_json


def get_lat(f_r, f_w):
    loc_list = load_json(f_r)
    state_d = {}
    for region_dic in loc_list:
        state = region_dic["stateabbr"]
        city = region_dic["placename"]
        coor = region_dic["geolocation"]["coordinates"]
        pop = int(region_dic["totalpopulation"])
        
        d = {}
        coor_p = []
        for i in coor:
            coor_rounded = round(i, 2)
            coor_p.append(coor_rounded)
        d[city] = (pop, coor_p)
        if state not in state_d.keys():
            state_d[state] = d
        else:
            state_d[state].update(d)

    two_city_d = {}
    for state in state_d:
        new_d = {}
        s_city = sorted(state_d[state].items(), key = lambda x:x[1], reverse=True)
        new_d[s_city[0][0]] = s_city[0][1][1]
        if len(s_city) > 1:
            new_d[s_city[1][0]] = s_city[1][1][1]
        two_city_d[state] = new_d
    write_json(f_w, two_city_d)


def cache_weather(coor_list, filename):
    weather_d = {}
    base = "https://api.openweathermap.org/data/3.0/onecall/timemachine"
    # for i in range(25):
    for i in coor_list:
        dic = {"lat":i[0], "lon":i[1], "dt":"1609520400", "appid":"0ed702778efe831f0e3d546dc34eece3"}
        result = get_api(base, dic)
        weather_d[(i[0],i[1])] = result["results"]
    write_json(filename, weather_d)

def main():
    loc_list = get_lat("health_data_r.json", "health_data.json")
    # cache_weather(loc_list, "weather_data.json")


if __name__ == "__main__":
    main()
