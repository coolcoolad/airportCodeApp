import json, re
from datetime import date, timedelta
from bs4 import BeautifulSoup

# with open('test2.txt', 'r') as fd:
#     jj = json.load(fd, encoding='utf-8')
#     print len(jj['cc'].encode('utf-8'))
#     print len(jj['dd'])

# with open('test.txt','r') as fd:
#     aa = fd.readline()
#     # soup = BeautifulSoup(aa, 'html.parser', from_encoding='utf-8')
#     # aa = soup.get_text()
#
#     print len(aa)
#     print aa
#     bb = aa.decode('utf-8')
#     print len(bb)
#     print bb
#
#     jsonMap = {aa:aa}
#     with open('test1.txt','w') as fd:
#         json.dump(jsonMap, fd, encoding='utf-8', ensure_ascii=True)


with open('airport_code_.json') as fd:
    jsonMap = json.load(fd, encoding='utf-8')
    nameMap = {}
    codeMap = {}

    for row in jsonMap['list']:
        name = row['name'].lower()
        code = row['iata'].upper()
        if name in nameMap:
            nameMap[name].append(code)
        else:
            nameMap[name] = [code]
        if code in codeMap:
            codeMap[code].append(name)
        else:
            codeMap[code] = [name]

    print 'name'
    for key, val in nameMap.items():
        if len(val) > 1:
            print (key, val)
    print 'iata'
    for key, val in codeMap.items():
        if len(val) > 1:
            print (key, val)

# delta = timedelta(days=5)
# future = date.today()+delta
# print future.isoformat()
#
# print future < date.today()

# aa = 'ee'
# print aa[1:5]
#
# print '23,342432,343343'.rfind(',')


# keywords = filter(lambda x:x != '', re.split('\s|-|\.|"|\'|\(|\)|/|,|&','Pinehurst-S. Pines'))
# print keywords

# num_str = ''
# if ord(num_str[0]) < ord('0') and ord(num_str[0]) > ord('9'):
#     dd = 1

# keywords = filter(lambda x:x != '', re.split('\s|-|\.|"|\'|\(|\)|/|,|&|airport','..a b--c.d"5\'6(7)8/1,2&3internationalddairportccSeattleTacoma International Airport'))
# print keywords


# with open('airport_code.json') as fd:
#     jsonMap = json.load(fd, encoding='utf-8')
#     ss = set([])
#     for row in jsonMap['list']:
#         name = row['name'].lower()
#         for ch in name:
#             ss.add(ch)
#
#     for ch in ss:
#         print ch