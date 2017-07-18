# -*- coding: utf-8 -*-

import os, sys, json, re
sys.path.insert(0, os.path.abspath('../flaskPackages/'))
from flask import Flask, request, Response
app = Flask(__name__)
app.url_map.strict_slashes = False
airportMap = {}
airportKeywordList = []
featureMap = {}
sep = '\s|-|\.|"|\'|\(|\)|/|,|&|international|airport'

def getEditDistance(a,b):
    m = len(a)+1
    n = len(b)+1
    dp = [[0]*n for i in range(m)]
    for i in range(1,n):
        dp[0][i] = i
    for i in range(1,m):
        dp[i][0] = i
    for i in range(1,m):
        for j in range(1,n):
            case1 = dp[i-1][j-1] + (0 if a[i-1]==b[j-1] else 1)
            case2 = dp[i-1][j]+1
            case3 = dp[i][j-1]+1
            dp[i][j] = min(case1, case2, case3)
    return dp[m-1][n-1]

def fuzzySearch1(name):
    minDist = 100000
    ans = "null"
    for key, code in airportMap.items():
        cur = getEditDistance(key, name)
        if minDist > cur:
            minDist = cur
            ans = code
    return ans

def getTextDistance(src,target):
    score = 0
    for word in src:
        if word in target:
            score += 2
        else:
            score -= 1
    return score

def fuzzySearch(name):
    src = filter(lambda x: x != '', re.split(sep, name))
    maxScore = 0
    ans = 'null'
    realName = 'null'
    for keywords, code, name in airportKeywordList:
        score = getTextDistance(src, keywords)
        if maxScore < score:
            maxScore = score
            ans = code
            realName = name
    return ans, realName

@app.route('/getAirportCode')
def getAirportCode():
    fuzzy = request.args['fuzzy']
    name = request.args['name'].lower()
    if fuzzy == '0':
        if name not in airportMap:
            return "null"
        return airportMap[name]
    elif fuzzy == '1':
        return fuzzySearch(name)[0]
    else:
        arr = re.split(sep, name)
        feature = ''.join(arr)
        if feature not in featureMap:
            return "null"
        return featureMap[feature]

@app.route('/getAirportCodeAndName')
def getAirportCodeAndName():
    fuzzy = request.args['fuzzy']
    name = request.args['name'].lower()
    jsonMap = {}
    realName = 'null'
    code = 'null'
    if fuzzy == '0':
        if name in airportMap:
            realName = name
            code = airportMap[name]
    else:
        code, realName = fuzzySearch(name)
    jsonMap['name'] = realName
    jsonMap['code'] = code
    resp = Response(json.dumps(jsonMap, encoding='utf-8'))
    resp.headers['Content-Type'] = 'application/json'
    return resp

@app.route('/', methods=['POST','GET'])
@app.route('/hello', methods=['POST','GET'])
def hello():
    print request.data
    print request.args
    return "hello"

if __name__ == '__main__':
    with open('airport_code.json') as fd:
        jsonMap = json.load(fd,encoding='utf-8')
        for row in jsonMap['list']:
            name = row['name'].lower()
            code = row['code'].upper()
            airportMap[name] = code
            arr = re.split(sep,name)
            keywords = set(filter(lambda x:x != '', arr))
            airportKeywordList.append([keywords, code, name])
            featureMap[''.join(arr)] = code
    #app.run(host='23.105.198.140',port=5001)
    app.run(host='10.172.211.107',port=5001)

