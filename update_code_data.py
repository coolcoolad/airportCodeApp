#-*- coding: UTF-8 -*-

import urllib, json
from bs4 import BeautifulSoup

def get(url):
    response = urllib.urlopen(url)
    return response.read().decode('utf-8')

def main():
    baseUrl = 'https://en.wikipedia.org/wiki/List_of_airports_by_IATA_code:_'
    jsonMap = {'list':[]}
    fileName = 'airport_code_.json'
    for i in range(26):
        ch = chr(i+ord('A'))
        url = baseUrl+ch
        html = get(url)
        soup = BeautifulSoup(html, 'html.parser')
        trArr = soup.find('table').find_all('tr')
        for tr in trArr:
            tdArr = tr.find_all('td')
            if len(tdArr) < 3:
                continue
            map_ = {}
            map_['iata'] = tdArr[0].get_text().encode('utf-8')
            map_['icao'] = tdArr[1].get_text().encode('utf-8')
            map_['name'] = tdArr[2].get_text().encode('utf-8')
            map_['location'] = ''
            map_['timezone'] = ''
            map_['dst'] = ''
            if len(tdArr) > 3:
                if tdArr[3].a is not None:
                    map_['location'] = tdArr[3].a.get_text().encode('utf-8')
                else:
                    map_['location'] = tdArr[3].get_text().encode('utf-8')
            if len(tdArr) > 4:
                if tdArr[4].a is not None:
                    map_['timezone'] = tdArr[4].a.get_text().encode('utf-8')
                else:
                    map_['timezone'] = tdArr[4].get_text().encode('utf-8')
            if len(tdArr) > 5:
                map_['dst'] = tdArr[5].get_text().encode('utf-8')
            jsonMap['list'].append(map_)
        print i
    with open(fileName,'w') as fd:
        json.dump(jsonMap,fd, encoding='utf-8', indent=4, separators=(',', ': '), ensure_ascii=False)

if __name__ == '__main__':
    main()