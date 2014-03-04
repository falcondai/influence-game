#!/usr/bin/python

import requests, sys, json, time

endpoint = 'https://www.googleapis.com/freebase/v1/topic%s?filter=/common/topic/notable_types'


if __name__ == '__main__':
    f = sys.stdin

    for l in f:
        objs = json.loads(l)
        for obj in objs:
            r = requests.get(endpoint % obj['mid'], params={'key': open('../credentials/freebase-api-key').read()})
            result = r.json()
            if 'property' in result:
                obj['/common/topic/notable_types'] = result['property']['/common/topic/notable_types']['values']
            else:
                sys.stderr.write(repr(result))
                sys.exit(1)
        print json.dumps(objs)
