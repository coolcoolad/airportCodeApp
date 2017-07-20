# -*- coding: utf-8 -*-

import os, sys, json, re
sys.path.insert(0, os.path.abspath('../flaskPackages/'))
from flask import Flask, request, Response
import logging
app = Flask(__name__)
app.url_map.strict_slashes = False

airportMap = {}
featureMap = {}
sep = '\s|-|\.|"|\'|\(|\)|/|,|&|airport'

def getFeature(name):
    ans = ''
    for ch in name:
        if ch >= 'a' and ch <= 'z':
            ans += ch
    return ans.replace('airport', '')

@app.route('/getAirportCode')
def getAirportCode():
    jsonMap = {'status':0, 'message':'', 'data':{'name':'null', 'code':'null'}}
    try:
        fuzzy = request.args['fuzzy']
        name = request.args['name'].lower()
        if fuzzy == '0':
            if name in airportMap:
                jsonMap['data']['name'] = name.encode('utf-8')
                jsonMap['data']['code'] = airportMap[name].encode('utf-8')
        elif fuzzy == '2':
            feature = getFeature(name)
            if feature in featureMap:
                jsonMap['data']['name'] = featureMap[feature][0].encode('utf-8')
                jsonMap['data']['code'] = featureMap[feature][1].encode('utf-8')
        else:
            raise Exception("fuzzy is wrong")
    except Exception, ex:
        app.logger.info(ex.message)
        jsonMap['status'] = 1
        jsonMap['message'] = ex.message.encode('utf-8')
    resp = Response(json.dumps(jsonMap, encoding='utf-8'))
    resp.headers['Content-Type'] = 'application/json'
    return resp

@app.route('/', methods=['POST','GET'])
@app.route('/hello', methods=['POST','GET'])
def hello():
    app.logger.info(request.data)
    app.logger.info(request.args)
    return "hello"

def initApp():
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    logHandler = logging.FileHandler('info.log', encoding='utf-8')
    logHandler.setFormatter(formatter)
    app.logger.level = logging.INFO
    app.logger.addHandler(logHandler)

    with open('airport_code_.json') as fd:
        jsonMap = json.load(fd, encoding='utf-8')
        for row in jsonMap['list']:
            name = row['name'].lower()
            code = row['iata'].upper()
            airportMap[name] = code
            featureMap[getFeature(name)] = (name,code)

initApp()

if __name__ == '__main__':
    #app.debug = True
    #app.run(host='23.105.198.140',port=5001)
    app.run(host='10.172.211.107',port=5001)

