# -*- coding: utf-8 -*-

import os, sys, json, re
sys.path.insert(0, os.path.abspath('../flaskPackages/'))
from flask import Flask, request, Response
app = Flask(__name__)
app.url_map.strict_slashes = False
featureMap = {}
sep = '\s|-|\.|"|\'|\(|\)|/|,|&|airport'

@app.route('/getAirportCode')
def getAirportCode():
    jsonMap = {'status':0, 'message':'', 'data':{'name':'null', 'code':'null'}}
    try:
        fuzzy = request.args['fuzzy']
        name = request.args['name'].lower()
        if fuzzy == '0':
            arr = re.split(sep, name)
            feature = ''.join(arr)
            if feature in featureMap:
                jsonMap['data']['name'] = featureMap[feature][0]
                jsonMap['data']['code'] = featureMap[feature][1]
        else:
            raise Exception("fuzzy is wrong")
    except Exception, ex:
        print ex.message
        jsonMap['status'] = 1
        jsonMap['message'] = ex.message
    resp = Response(json.dumps(jsonMap, encoding='utf-8'))
    resp.headers['Content-Type'] = 'application/json'
    return resp

@app.route('/', methods=['POST','GET'])
@app.route('/hello', methods=['POST','GET'])
def hello():
    print request.data
    print request.args
    return "hello"

def initApp():
    with open('airport_code.json') as fd:
        jsonMap = json.load(fd,encoding='utf-8')
        for row in jsonMap['list']:
            name = row['name'].lower()
            code = row['code'].upper()
            arr = re.split(sep,name)
            featureMap[''.join(arr)] = (name,code)

initApp()

if __name__ == '__main__':
    #app.run(host='23.105.198.140',port=5001)
    app.run(host='10.172.211.107',port=5001)

