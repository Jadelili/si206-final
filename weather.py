import os
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
        fhand.close()

    except:
        d = {}
    return d


def write_json(filename, dict): 
    with open(filename, "w") as fhand:
        fhand.write(json.dumps(dict))


def get_api(url, params):
    try:
        r = requests.get(url, params)
        return r.json()
    except:
        print("Cannot find API")
        return None


def cache_health_data(filename):
    health_list = []
    for i in range(2000,55000,10000):
        base_url = 'https://chronicdata.cdc.gov/resource/cj8b-94cj.json'
        where_clause = f'totalpopulation > {i}'
        url = f"{base_url}?$where={urllib.parse.quote(where_clause)}"
        group_result = get_api(url, None)
        for dic in group_result:
            health_list.append(dic)
    write_json(filename, health_list)


def get_lat(f_r, f_w):
    loc_list = load_json(f_r)
    state_d = {}
    for region_dic in loc_list:
        state = region_dic["stateabbr"]
        city = region_dic["placename"]
        coor_b = region_dic["geolocation"]["coordinates"]
        pop = int(region_dic["totalpopulation"])
        
        d = {}
        coor = (coor_b[1], coor_b[0])
        d[city] = (pop, coor)
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
    # print(two_city_d)
    return two_city_d


def cache_weather_data(two_city_d, weatherfile):
    weather_d = {}
    base = "https://history.openweathermap.org/data/2.5/aggregated/year"
    for state in two_city_d:
        d = {}
        for city in two_city_d[state]:
            dic = {"lat":two_city_d[state][city][0], "lon":two_city_d[state][city][1], "appid":"0ed702778efe831f0e3d546dc34eece3"}
            result = get_api(base, dic)
            d[city] = result
            # weather_d[state] = d        # {state:{city:data, city2:data}}
            if state not in weather_d.keys():
                weather_d[state] = d
            else:
                weather_d[state].update(d)
    write_json(weatherfile, weather_d)


def process_weather_data(weatherfile_r, weatherfile):
    weather_r = load_json(weatherfile_r)
    lst = []
    weather_d = {}
    for state in weather_r:
        for city in weather_r[state]:
            d = {}
            total_t_median = 0
            total_ps_median = 0
            total_c_median = 0 
            count = 0
            for i in weather_r[state][city]["result"]:
                count += 1
                total_t_median += i["temp"]["median"]
                total_ps_median += i["pressure"]["median"]
                total_c_median += i["clouds"]["median"]
            t_avg = total_t_median / count
            ps_avg = total_ps_median / count
            c_avg = total_c_median / count
            d["temp_medium"] = t_avg
            d["pressure_medium"] = ps_avg
            d["clouds_medium"] = c_avg

            if city not in list(weather_d.keys()):
                weather_d[city] = d
            elif city == "Portland":
                weather_d["Portland_Maine"] = d
            elif city == "Charleston":
                weather_d["Charleston_WestVirginia"] = d
            elif city == "Columbia":
                weather_d["Columbia_Maryland"] = d
    # print(weather_d)
    write_json(weatherfile, weather_d)
    return weather_d


def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/' + db_name)
    cur = conn.cursor()
    return cur, conn


def make_weather_table(filename, cur, conn):
    weather = load_json(filename)
    cur.execute("CREATE TABLE IF NOT EXISTS Weather (id INTEGER PRIMARY KEY, city_name TEXT, temp FLOAT, pressure FLOAT, clouds FLOAT)")

    lst2 = []
    for city in weather:
        city_n = city
        temp = round(weather[city]["temp_medium"], 2)
        pressure = round(weather[city]["pressure_medium"], 2)
        clouds = round(weather[city]["clouds_medium"], 2)
        lst2.append((city_n, temp, pressure, clouds))
        
    for i in range(len(weather)):
        # print(lst2[i][0])
        cur.execute("INSERT OR IGNORE INTO Weather (id, city_name, temp, pressure, clouds) VALUES (?,?,?,?,?)",
                    (i, lst2[i][0], lst2[i][1], lst2[i][2], lst2[i][3]))
    conn.commit()



def main():
    two_city_d = get_lat("health_data_r.json", "location_data.json")
    ### cache_weather_data(two_city_d, "weather_data_r.json")
    ### cache_weather_data(two_city_d, "weather_month_data_r.json")  
    ### process_weather_data("weather_data_r.json", "weather_data.json")
    # cur, conn = open_database("weather.db")
    # make_weather_table("weather_data.json", cur, conn)

if __name__ == "__main__":
    main()