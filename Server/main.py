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


kran11 = ''
kran12 = ''

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
    data1 = read_json("./static/json/data.json")
    data2 = read_json("./static/json/data.json")
    kran1 = ""
    kran2 = ""
    if data1[-1][1] == 1:
        kran11 = "Крановщик 1\n"
    elif data1[-1][1] == 2:
        kran12 = "Крановщик 1\n"
    if data2[-1][1] == 1:
        kran11 = "Крановщик 2"
    elif data2[-1][1] == 2:
        kran12 = "Крановщик 2"


def zeros(path):
    print("Trying to read json")
    data = read_json(path)

    try:
        if time.time()*1000 - data[-1][0] > 60:
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

@app.route("/buynode/<mac>", methods=["GET", "POST"])
def dataCome(mac):
    data_show = read_json("./static/json/inside.json")
    data_show[0] += 1
    write_json(data_show, "./static/json/inside.json")

    if mac[0] == "4":
        ts = time.time()*1000
        data2write = [ts, int(mac[1])]
        data_old = read_json("./static/json/data.json")
        data_old.append(data2write)
        write_json(data_old, "./static/json/data.json")
    else:
        ts = time.time()*1000
        data2write = [ts, int(mac[1])]
        data_old = read_json("./static/json/data1.json")
        data_old.append(data2write)
        write_json(data_old, "./static/json/data1.json")
    return "200"


@app.route("/", methods=["GET", "POST"])
def data():
    data_show = read_json("./static/json/inside.json")
    data_show[1] += 1
    write_json(data_show, "./static/json/inside.json")

    enters = data_show[1]
    craneNUM = data_show[0]

    zeros("./static/json/data.json")
    zeros("./static/json/data1.json")
    try:
        whois()
    except:
        print("No one in kran")
    kran1 = kran11
    kran2 = kran12

    return render_template("index.html", **locals())


# Main flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7777, debug=True)
