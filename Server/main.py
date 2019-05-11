#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Bauyrzhan Ospan"
__copyright__ = "Copyright 2018, KazPostBot"
__version__ = "1.0.1"
__maintainer__ = "Bauyrzhan Ospan"
__email__ = "bospan@cleverest.tech"
__status__ = "Development"

from flask import Flask, render_template, request, Markup, jsonify
import time
import json
from tqdm import tqdm
from pathlib import Path


app = Flask(__name__)  # Creating new flask app
home = str(Path.home())

def write_json(data, name):
    with open(name, 'w') as outfile:
        json.dump(data, outfile)


def read_json(name):
    with open(name, 'r') as f:
        print("File read")
        return json.load(f)

def whois():
    data1 = read_json("/home/naboo/CraneDemo/Server/static/json/data.json")
    data2 = read_json("/home/naboo/CraneDemo/Server/static/json/data.json")
    kran11 = ""
    kran12 = ""
    if data1[-1][1] == 1:
        kran11 = "Крановщик 1\n"
    elif data1[-1][1] == 2:
        kran12 = "Крановщик 2\n"
    if data2[-1][1] == 1:
        kran11 = "Крановщик 1"
    elif data2[-1][1] == 2:
        kran12 = "Крановщик 2"
    return kran11, kran12
    print(kran11 + kran12)


def zeros(path):
    print("Trying to read json")
    data = read_json(path)

    try:
        if time.time()*1000 - data[-1][0] > 60000:
            data.append([time.time()*1000, 0])
    except:
        print("First one")

    for i in tqdm(range(len(data) - 1)):
        x = (data[i+1][0]/1000) - (data[i][0]/1000)
        if x>60:
            print("SMB not in work")
            dif = 1
            change = ((data[i][0]/1000) + dif*60)
            while True:
                if change >= (data[i+1][0]/1000):
                    break
                data.append([((data[i][0]/1000) + dif*60)*1000, 0])
                dif += 1
                change = ((data[i][0]/1000) + dif*60)

    data = sorted(data, key=lambda x: x[0])
    write_json(data, path)


from datetime import datetime, time, date

def fromts_to_date(ts):
    date = datetime.fromtimestamp(ts/1000)
    return date


def convert_to_worktime(delta):
    seconds = delta.total_seconds()
    
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if seconds > 30:
        minutes += 1
    if minutes >= 60:
        hours += 1
        minutes %= 60
    result = [hours, minutes]

    return result


import itertools
def get_date(ts):
    return datetime.fromtimestamp(ts/1000).date()


def crane_table_info(path):
    data = read_json(path)
    crane_state = []

    for item in data:
        if item[1] == 1:
            crane_state.append(item[0])
    
    return crane_state


def get_hour(date):
    return fromts_to_date(date).hour

def calc_shifts_hours(path):
    blob = crane_table_info(path)
    date_groups = itertools.groupby(blob, get_date)
    dayshifts_hours = {}
    nightshifts_hours = {}

    daytime = [8,9,10,11,12,13,14,15,16,17,18,19]

    for date, date_group in date_groups:
        by_date = []
        by_hour_day = []
        by_hour_night = []
        hour_groups = itertools.groupby(date_group, get_hour)
        for hour, item in hour_groups:
            an_item = list(item)    
            delta = fromts_to_date(an_item[-1]) - fromts_to_date(an_item[0])
            if hour in daytime:
                by_hour_day.append(convert_to_worktime(delta))
            else:
                by_hour_night.append(convert_to_worktime(delta))
        
        by_hour_day_int = [[int(float(j)) for j in i] for i in by_hour_day]
        by_hour_night_int = [[int(float(j)) for j in i] for i in by_hour_night]
        
        dayshifts_hours[date.strftime("%d.%m.%Y")] = [sum(x) for x in zip(*by_hour_day_int)]
        nightshifts_hours[date.strftime("%d.%m.%Y")] = [sum(x) for x in zip(*by_hour_night_int)]

    return dayshifts_hours, nightshifts_hours


def get_final_time(shift_hours):
    for shift, workhours in shift_hours.items():
        try:
            if workhours[1] >= 60:
                workhours[0] += workhours[1] //60
                workhours[1] = workhours[1] % 60
        except IndexError:
            workhours = 0
            
    return shift_hours


def get_worktime_in_h_m(dictionary):
    dates = []
    worktime = []
    worktime_str = []

    for key, value in dictionary.items():
        dates.append(key)
        try:
            worktime.append([value[0], value[1]])
            worktime_str.append(f"{value[0]} ч {value[1]} мин")
        except IndexError:
            worktime.append([0,0])
            worktime_str.append("Нет данных")
        
    return dates, worktime, worktime_str


def avg_time(array_of_time):
    sum_hours = 0
    sum_minutes = 0
    counter = 0
    for item in array_of_time:
        sum_hours += item[0] 
        sum_minutes += item[1]
        counter += 1
    try:
        sum_minutes += sum_hours * 60 
        avg_time = sum_minutes // counter
        avg_hours = avg_time // 60
        avg_minutes = avg_time - avg_hours * 60
        average_work_time = f"{avg_hours} ч {avg_minutes} мин"
    except ZeroDivisionError:
        average_work_time = "Недостаточно данных"
    
    return average_work_time


@app.route("/buynode/<mac>", methods=["GET", "POST"])
def dataCome(mac):
    data_show = read_json("/home/naboo/CraneDemo/Server/static/json/inside.json")
    data_show[0] += 1
    write_json(data_show, "/home/naboo/CraneDemo/Server/static/json/inside.json")

    if mac[0] == "4":
        ts = time.time()*1000
        data2write = [ts, int(mac[1])]
        data_old = read_json("/home/naboo/CraneDemo/Server/static/json/data.json")
        data_old.append(data2write)
        write_json(data_old, "/home/naboo/CraneDemo/Server/static/json/data.json")
    else:
        ts = time.time()*1000
        data2write = [ts, int(mac[1])]
        data_old = read_json("/home/naboo/CraneDemo/Server/static/json/data1.json")
        data_old.append(data2write)
        write_json(data_old, "/home/naboo/CraneDemo/Server/static/json/data1.json")
    return "200"


@app.route("/", methods=["GET", "POST"])
def data():
    data_show = read_json("/home/naboo/CraneDemo/Server/static/json/inside.json")
    data_show[1] += 1
    write_json(data_show, "/home/naboo/CraneDemo/Server/static/json/inside.json")

    enters = data_show[1]
    craneNUM = data_show[0]
    

    # TODO consider oop for these ugly functions
    dayshftsdic1,nightshiftsdic1 = calc_shifts_hours('/home/naboo/CraneDemo/Server/static/json/data.json')
    day_shifts1 = get_final_time(dayshftsdic1)
    night_shifts1 = get_final_time(nightshiftsdic1)
    date_day1, day_workhours1, day_workhours_str1 = get_worktime_in_h_m(day_shifts1)
    date_night1, night_workhours1, night_workhours_str1 = get_worktime_in_h_m(night_shifts1)
    avg_day_worktime1 = avg_time(day_workhours1)
    avg_night_worktime1 = avg_time(night_workhours1)

    dayshftsdic2,nightshiftsdic2 = calc_shifts_hours('/home/naboo/CraneDemo/Server/static/json/data1.json')
    day_shifts2 = get_final_time(dayshftsdic2)
    night_shifts2 = get_final_time(nightshiftsdic2)
    date_day2, day_workhours2, day_workhours_str2 = get_worktime_in_h_m(day_shifts2)
    date_night2, night_workhours2, night_workhours_str2 = get_worktime_in_h_m(night_shifts2)
    avg_day_worktime2 = avg_time(day_workhours2)
    avg_night_worktime2 = avg_time(night_workhours2)


    zeros("/home/naboo/CraneDemo/Server/static/json/data.json")
    zeros("/home/naboo/CraneDemo/Server/static/json/data1.json")
    try:
        kran1, kran2 = whois()
    except:
        print("No one in kran")

    return render_template("index.html", **locals())


# Main flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8787, debug=True)
