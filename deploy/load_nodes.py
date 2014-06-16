#!/usr/bin/env python

from pymongo import MongoClient
import sys, json

client = MongoClient()
db = client.main

f = sys.stdin

for l in f:
    objs = json.loads(l)
    print 'upserting %d JSON objects by mid...' % len(objs)
    for i, obj in enumerate(objs):
        db.nodes.update(
            {
                'mid': obj['mid'],
            },
            {
                '$set': obj
            },
            True
        )
