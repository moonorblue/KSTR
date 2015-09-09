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





if __name__ == '__main__':
    

    #Read CategoryData
    ##FB
    FBPlaceData = '/home/moonorblue/placeData_new/'
    ##CA
    CADict = {}
    CAPlaceData = '/home/ytwen/CA Dataset/checkin_CA_venues.txt'
    f = open(CAPlaceData)
    flag = False
    count = 1
    for l in f.readlines():
        if( flag ):
            m=re.match('(.*)\t(.*)\t(.*)\t(\{.*\})\t(\{.*\})\r\n',l)
            pid = str(m.group(3))
            s=''
            categories = m.group(5).strip('{').strip('}').split(',')
            for i in xrange(len(categories)-1):
                s += categories[i]
                if i != len(categories)-2:
                    s += ','
            CADict[pid] = s
	flag = True    


    #Read PATS
    CAPATSPath = '/home/moonorblue/PATS/CA/result'
    CAPATSDict = json.load(open(CAPATSPath))
    FBPATSPath = '/home/moonorblue/PATS/FB/result'
    FBPATSDict = json.load(open(FBPATSPath))

    #OrignalRoute
    CAPath = '/home/moonorblue/TimeDistribution/CA/'
    FBPath = '/home/moonorblue/TimeDistribution/FB/'

    #new Route With Scores
    CAPath_new = '/home/moonorblue/routes/CA/WithScore/'
    FBPath_new = '/home/moonorblue/routes/FB/WithScore/'

    
    for user in listdir(CAPath):
        f = open(CAPath+user)
        j = json.load(f)
        if 'route' in j:
            routes = j['route']
            print user
        else:
            print 'no route'
            continue
        # print '#r:',routes
        for r in routes:
            # route = routes[r]
            for rr in r:
                pid = rr['pid']
                category = CADict[str(pid)]
                PATSScore = CAPATSDict[str(pid)]
                rr['category'] = category
                rr['PATS'] = PATSScore

        w = open(CAPath_new+user,'w')
        w.write(json.dumps(j))
        w.close()


    for user in listdir(FBPath):
        f = open(FBPath+user)
        j = json.load(f)
        if 'route' in j:
            routes = j['route']
            print user
        else:
            print 'no route'
            continue
        for r in routes:
            # route = routes[r]
            for rr in r:
                pid = rr['pid']
                nf = open(FBPlaceData+pid)
                nj = json.load(nf)
                category = ''
                if( 'category' in nj):
                    category = nj['category'].encode()

                PATSScore = FBPATSDict[str(pid)] 
                rr['category'] = category
                rr['PATS'] = PATSScore

        w = open(FBPath_new+user,'w')
        w.write(json.dumps(j))
        w.close()


         
     

    

   
