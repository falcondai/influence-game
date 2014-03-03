#!/usr/bin/python

import json, urllib, sys

endpoint = 'https://www.googleapis.com/freebase/v1/mqlread'

query = sys.stdin.read()

url = endpoint + '?' + urllib.urlencode({
    'query': query, 
    'cursor': ''
})
#print url

r = json.load(urllib.urlopen(url))
#print len(r['result']), r['cursor']
print json.dumps(r['result'])

while r['cursor']:
    url = endpoint + '?' + urllib.urlencode({
        'query': query, 
        'cursor': r['cursor']
    })
    prev_cursor = r['cursor']
    r = json.load(urllib.urlopen(url))
    #print len(r['result']), r['cursor']
    if 'result' in r:
        print json.dumps(r['result'])
    else:
        r['cursor'] = prev_cursor
        
