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

rootPath = "/home/moonorblue/FollowCount/CA"


def calFollow(userID):
    uID = str(userID)
    print 'User: ',uID
    friends = graph.cypher.execute("MATCH (n:CAUser {id:{uid}})-[:KNOWS]->(f:CAUser) RETURN f.id;",{"uid":uID})
    followRelation = {}

    for friend in friends:
        visitRecords = graph.cypher.execute("MATCH (n:CAUser {id:{friendid}})-[r:VISITED]->(p:CAPlace) RETURN DISTINCT p.id;",{"friendid":friend['f.id']})
        isVisit=[]
        followCount = 1
        for record in visitRecords:
            if( record['p.id'] in isVisit):
                continue
            else:
                isVisit.append(record['p.id'])

            totalRecords = graph.cypher.execute("MATCH (n:CAUser {id:{friendid}})-[r:VISITED]->(p:CAPlace {id:{pid}}) RETURN r.atTime ORDER BY toFloat(r.atTime) DESC;",{"friendid":friend['f.id'], "pid":record['p.id']})
            userVisitRecords = graph.cypher.execute("MATCH (n:CAUser {id:{userid}})-[r:VISITED]->(p:CAPlace {id:{pid}}) RETURN r.atTime ORDER BY toFloat(r.atTime);",{"userid":uID,"pid":record['p.id']})

            flag = False
            for userVisitRecord in userVisitRecords:
                userVisitTime = float(userVisitRecord['r.atTime'])
                for totalR in totalRecords: 
                    if(userVisitTime > float(totalR['r.atTime'])):
                        followCount += 1
                        flag = True
                        break

                if flag == True:
                    break
        followRelation[str(friend['f.id'])] = followCount


    f = open('/home/moonorblue/FollowCount/CA/'+uID,'wb')
    f.write(json.dumps(followRelation))
    f.close()





graph=Graph()



pool_size = 5     # your "parallelness"
pool = Pool()



users = graph.cypher.execute("MATCH (n:CAUser) RETURN n.id")
usersL = [u['n.id'] for u in users]
# for u in usersL:
#     calFollow(u)
pool.map(calFollow,usersL)


pool.close()
pool.join()


