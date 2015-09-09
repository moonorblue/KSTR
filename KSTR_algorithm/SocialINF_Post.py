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
from py2neo.packages.httpstream import http
http.socket_timeout = 9999
from scipy.sparse import dok_matrix
import scipy.linalg
import re
from sets import Set





if __name__ == '__main__':
    CAPath_new = '/home/moonorblue/routes/CA/WithScore/'
    FBPath_new = '/home/moonorblue/routes/FB/WithScore/'

    CASocialIdxPath = '/home/moonorblue/socialINF/CA/idxDict'
    FBSocialIdxPath = '/home/moonorblue/socialINF/FB/idxDict'
    
    CASocialLocPath = '/home/moonorblue/socialINF/CA/locDict'
    FBSocialLocPath = '/home/moonorblue/socialINF/FB/locDict'
    

    # g = Graph()
    print 'CA'
    CASocialIdxDict = json.load(open(CASocialIdxPath))
    locDict = {}
    for u in listdir(CAPath_new):
        f = open(CAPath_new + u)
        j = json.load(f)
        routes = j['route']

        for routeList in routes:
            for r in routeList:
                pid = r['pid']
                if pid in locDict:
                    continue
                else:
                    userListSet = Set([])
                    locDict[pid] = userListSet
    
    CAPlaceData = '/home/ytwen/CA Dataset/checkin_CA_venues.txt'
    f = open(CAPlaceData)
    flag = False
    count = 0
    lines = f.readlines()
    for l in lines:
        if( flag ):
            print str(float(count)/len(lines)*100),'%'
            m=re.match('(.*)\t(.*)\t(.*)\t(\{.*\})\t(\{.*\})\r\n',l)
            pid = str(m.group(3))
            uid = str(m.group(1))
            if uid in CASocialIdxDict:
                if pid in locDict:
                    locDict[pid].add(uid)   
                    # print locDict[pid]       
        flag = True 
        count +=1 

    for loc in locDict:
        locDict[loc] = list(locDict[loc])

    w = open(CASocialLocPath,'w')
    w.write(json.dumps(locDict))
    w.close()

    print 'FB'
    FBSocialIdxDict = json.load(open(FBSocialIdxPath))
    locDict = {}
    for u in listdir(FBPath_new):
        f = open(FBPath_new + u)
        j = json.load(f)
        routes = j['route']

        for routeList in routes:
            for r in routeList:
                pid = r['pid']
                if pid in locDict:
                    continue
                else:
                    userListSet = Set([])
                    locDict[pid] = userListSet
    
    rootPath = "/home/ytwen/fbdata/"
    count = 1
    userL = listdir(rootPath)
    recordC=Set([])
    recordL=Set([])
    for user in userL:
        print str(float(count)/len(userL)*100),'%'

        rootPath = "/home/ytwen/fbdata/"+user
        for friend in listdir(rootPath):
            if friend in FBSocialIdxDict:
                # print '#',friend
                furtherPath = rootPath+'/'+friend
                for folder in listdir(furtherPath):
                    if(folder == "checkin"):
                        if(friend in recordC):
                            continue
                        else:
                            recordC.add(friend)
                            path = furtherPath+'/'+folder
                            uID = friend
                            
                            jsonFile = path+'/'+uID
                            json_data=open(jsonFile)
                            data = json.load(json_data)
                            for eachData in data:
                                if('place' in eachData):
                                    placeID = str(eachData['place']['id'])
                                    # if uID in FBSocialIdxDict:
                                    if placeID in locDict:
                                        # print '##',placeID
                                        locDict[placeID].add(uID)
                                        # print locDict[pid]                            

                    elif(folder == "location"):
                        if(friend in recordL):
                            continue
                        else:
                            recordL.add(friend)
                            path = furtherPath+'/'+folder
                            uID = friend
                            jsonFile = path+'/'+uID
                            json_data=open(jsonFile)
                            data = json.load(json_data)
                            for eachData in data:
                                if('place' in eachData):
                                    placeID = str(eachData['place']['id'])
                                    # if uID in FBSocialIdxDict:
                                    if placeID in locDict:
                                        # print '##',placeID
                                        locDict[placeID].add(uID)
                                        # print locDict[pid] 
        count += 1

    for loc in locDict:
        locDict[loc] = list(locDict[loc])

    w = open(FBSocialLocPath,'w')
    w.write(json.dumps(locDict))
    w.close()
    
    # for u in listdir(FBPath_new):
    #     f = open(FBPath_new + u)
    #     j = json.load(f)
    #     routes = j['route']

    #     for routeList in routes:
    #         for r in routeList:
    #             pid = r['pid']
    #             if pid in locDict:
    #                 continue
    #             userList = []
    #             for user in FBSocialIdxDict:
    #                 request = g.cypher.execute("MATCH (n:User {id:{uid}})-[r:VISITED]->(p:Place {id:{pid}}) RETURN COUNT(*)",{"uid":user,"pid":pid})
    #                 for re in request:
    #                     if re['COUNT(*)'] != 0:
    #                         userList.append(user)
    #             locDict[pid] = userList

    # w = open(FBSocialLocPath,'w')
    # w.write(json.dumps(locDict))
    # w.close()
