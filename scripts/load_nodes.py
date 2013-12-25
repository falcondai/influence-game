from pymongo import MongoClient
import sys, json

client = MongoClient()
db = client.main

f = sys.stdin

for l in f:
    objs = eval(l)
    print len(objs)
    db.nodes.insert(objs)
