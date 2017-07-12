# -*- coding: utf-8 -*-

import os, sys, json
sys.path.insert(0, os.path.abspath('../flaskPackages/'))
from flask import Flask, request, Response
app = Flask(__name__)
app.url_map.strict_slashes = False
airportMap = {}

@app.route('/getAirportCode')
def getAirportCode():
    name = request.args['name']
    return airportMap[name]

@app.route('/hello', methods=['POST','GET'])
def hello():
    print request.data
    print request.args
    return "hello"

if __name__ == '__main__':
    with open('airport_code.json') as fd:
        jsonMap = json.load(fd,encoding='utf-8')
        for row in jsonMap['list']:
            airportMap[row['name']] = row['code']
    app.run(host='10.172.211.107',port=5001)

