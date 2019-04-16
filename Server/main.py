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


app = Flask(__name__)  # Creating new flask app

def write_json(data, name):
    with open(name, 'w') as outfile:
        json.dump(data, outfile)


def read_json(name):
    with open(name, 'r') as f:
        print("File read")
        return json.load(f)


@app.route("/buynode/", methods=["GET", "POST"])
def dataCome():
    data_show = read_json("./static/json/inside.json")
    data_show[0] += 1
    write_json(data_show, "./static/json/inside.json")
    ts = time.time()*1000
    data2write = [ts, 1]
    data_old = read_json("./static/json/data.json")
    data_old.append(data2write)
    write_json(data_old, "./static/json/data.json")
    return "200"


@app.route("/", methods=["GET", "POST"])
def data():
    data_show = read_json("./static/json/inside.json")
    data_show[1] += 1
    write_json(data_show, "./static/json/inside.json")

    enters = data_show[1]
    craneNUM = data_show[0]


    print("Trying to read json")
    data = read_json("./static/json/data.json")
    for i in tqdm(range(len(data) - 1)):
        x = (data[i+1][0]/1000) - (data[i][0]/1000)
        if x>600:
            dif = 1
            change = ((data[i][0]/1000) + dif*60)
            while True:
                if change >= (data[i+1][0]/1000):
                    break
                data.append([((data[i][0]/1000) + dif*60)*1000, 0])
                dif += 1
                change = ((data[i][0]/1000) + dif*60)

    data = sorted(data, key=lambda x: x[0])
    write_json(data, "./static/json/data.json")
    return render_template("index.html", **locals())


# Main flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=777, debug=True)
