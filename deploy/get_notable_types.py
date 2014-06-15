#!/usr/bin/env python

import sys, json, time, argparse
import grequests

endpoint = 'https://www.googleapis.com/freebase/v1/topic%s?filter=/common/topic/notable_types'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('data', help='path to json objects imported')
    parser.add_argument('-o', '--output', help='output file path')
    parser.add_argument('-k', '--key', help='FreeBase API key path', default='../credentials/freebase-api-key')
    parser.add_argument('-b', '--batch', help='batch size', type=int, default=100)
    args = parser.parse_args()

    reqs = []

    total_count = 0
    freebase_key = open(args.key).read()
    with open(args.data) as fi:
        with open(args.output, 'wb') if args.output else sys.stdout as fo:
            for l in fi:
                objs = json.loads(l)
                for obj in objs:
                    r = grequests.get(endpoint % obj['mid'], params={'key': freebase_key})
                    reqs.append(r)
                    if len(reqs) == args.batch:
                        ress = grequests.map(reqs)
                        nreqs = []
                        for i, res in enumerate(ress):
                            result = res.json()
                            if 'property' in result:
                                obj['/common/topic/notable_types'] = result['property']['/common/topic/notable_types']['values']
                                total_count += 1
                                if total_count % 100 == 0:
                                    print 'queried %d notable types' % total_count
                            else:
                                print 'ERROR', repr(result)
                                nreqs.append(reqs[i])
                        reqs = nreqs

                fo.write(json.dumps(objs))
                fo.write('\n')
    print 'done getting notable types for %d objects' % total_count
