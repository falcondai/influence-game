#!/usr/bin/env python

import json, requests, sys, argparse

if __name__ == '__main__':
    endpoint = 'https://www.googleapis.com/freebase/v1/mqlread'

    parser = argparse.ArgumentParser()
    parser.add_argument('query', help='path to FreeBase MQL query')
    parser.add_argument('-o', '--output', help='output file path')
    parser.add_argument('-c', '--cursor', help='cursor to resume', default='')
    
    args = parser.parse_args()

    with open(args.query) as f:
        query = f.read()

    print 'making MQL query to %s:' % endpoint
    print query

    total_count = 0

    switch = 'wb' if args.cursor == '' else 'ab'
    with open(args.output, switch) if args.output else sys.stdout as f:
        prev_cursor = args.cursor
        while prev_cursor == '' or prev_cursor:
            req = requests.get(endpoint, params={
                'query': query, 
                'cursor': prev_cursor or '',
            })
            r = req.json()
            if 'result' in r:
                total_count += len(r['result'])
                f.write(json.dumps(r['result']))
                f.write('\n')
            prev_cursor = r['cursor']
            print len(r['result']), prev_cursor

    print 'done downloading %d objects from Freebase' % total_count

