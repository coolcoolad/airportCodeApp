import json, re

aa = 'ee'
print aa[1:5]

print '23,342432,343343'.rfind(',')


# keywords = filter(lambda x:x != '', re.split('\s|-|\.|"|\'|\(|\)|/|,|&','Pinehurst-S. Pines'))
# print keywords

# num_str = ''
# if ord(num_str[0]) < ord('0') and ord(num_str[0]) > ord('9'):
#     dd = 1

keywords = filter(lambda x:x != '', re.split('\s|-|\.|"|\'|\(|\)|/|,|&|international|airport','..a b-c.d"5\'6(7)8/1,2&3internationalddairportcc'))
print keywords

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