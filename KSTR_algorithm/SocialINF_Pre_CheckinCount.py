from py2neo import Graph
from py2neo import Node, Relationship
import os
import itertools
from os import listdir
import json
import time
import math
import operator
from multiprocessing.pool import ThreadPool as Pool
# from multiprocessing import Pool
from py2neo.packages.httpstream import http
http.socket_timeout = 9999







def getCount():
    print '####: FB'
    users = graph.cypher.execute("MATCH (n:User) RETURN n.id")
    countDict={}
    for u in users:
	uid = u['n.id']
	checkinsCount = graph.cypher.execute("MATCH (n:User {id:{uid}})-[r:VISITED]->(p:Place) RETURN COUNT(*);",{"uid":uid})
        countDict[uid] = checkinsCount[0]['COUNT(*)']
    w = open('/home/moonorblue/checkinCount/FB/result','w')
    w.write(json.dumps(countDict))
    w.close()
    print '####: CA'
    users = graph.cypher.execute("MATCH (n:CAUser) RETURN n.id")
    countDict={}
    for u in users:
	uid = u['n.id']
	checkinsCount = graph.cypher.execute("MATCH (n:CAUser {id:{uid}})-[r:VISITED]->(p:CAPlace) RETURN COUNT(*);",{"uid":uid})
        countDict[uid] = checkinsCount[0]['COUNT(*)']
    w = open('/home/moonorblue/checkinCount/CA/result','w')
    w.write(json.dumps(countDict))
    w.close()
    print '####: GWL'
    users = graph.cypher.execute("MATCH (n:GWLUser) RETURN n.id")
    countDict={}
    for u in users:
	uid = u['n.id']
	checkinsCount = graph.cypher.execute("MATCH (n:GWLUser {id:{uid}})-[r:VISITED]->(p:GWLPlace) RETURN COUNT(*);",{"uid":uid})
        countDict[uid] = checkinsCount[0]['COUNT(*)']
    w = open('/home/moonorblue/checkinCount/GWL/result','w')
    w.write(json.dumps(countDict))
    w.close()
    print '####: FS'
    users = graph.cypher.execute("MATCH (n:FSUser) RETURN n.id")
    countDict={}
    for u in users:
	uid = u['n.id']
	checkinsCount = graph.cypher.execute("MATCH (n:FSUser {id:{uid}})-[r:VISITED]->(p:FSPlace) RETURN COUNT(*);",{"uid":uid})
        countDict[uid] = checkinsCount[0]['COUNT(*)']
    w = open('/home/moonorblue/checkinCount/FS/result','w')
    w.write(json.dumps(countDict))
    w.close()


graph=Graph()

getCount()
