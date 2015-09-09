 
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


def constructMatrix(followDictAll, checkinCountDict):
    idxDict = {}
    idx = 0
    
    for f in followDictAll:
        allfollowee = followDictAll[f]
        if f not in idxDict:
            idxDict[f] = idx
            idx += 1
        for followee in allfollowee:
            if followee not in idxDict:
                idxDict[followee] = idx
                idx += 1

    size = idx
    matrix = dok_matrix((size, size))
    print str(matrix.shape)

    for f in followDictAll:

        fPersonalScore = 0.0
        allfollowee = followDictAll[f]

        if f not in idxDict:
            idxDict[f] = idx
            idx += 1

        for followee in allfollowee:
            
            if followee not in idxDict:
                idxDict[followee] = idx
                idx += 1
            follwCount = float(allfollowee[followee])-1
            userCheckinCount = float(checkinCountDict[f])
            followeeCheckinCount = float(checkinCountDict[followee])
            
            if follwCount == 0:
                continue
            # print f,followee,follwCount
            socialScore = follwCount / \
                ((math.sqrt(userCheckinCount))
                 * (math.sqrt(followeeCheckinCount)))
            # print f,followee,socialScore
            matrix[idxDict[f], idxDict[followee]] = socialScore
            fPersonalScore += socialScore

        matrix[idxDict[f], idxDict[f]] = -fPersonalScore

    # print matrix.shape
    # w = open('/home/moonorblue/matrix','w')
    # w.write(json.dumps(matrix.toarray().tolist()))
    # w.close()

    # matrix expnonetial
    print 'Matrix Expnonetial Start'
    finalMatrix = scipy.linalg.expm(matrix.tocsc())

    return idxDict, finalMatrix.toarray().tolist()


def loadUserCheckinsCount(dataset):
    checkinCountPath = '/home/moonorblue/checkinCount/' + dataset + '/result'
    j = json.load(open(checkinCountPath))
    return j


def conbineFollowDict(dataset):
    followDictPath = '/home/moonorblue/FollowCount/' + dataset
    allUser = listdir(followDictPath)
    followDictAll = {}
    for user in allUser:
        userFollowDictPath = '/home/moonorblue/FollowCount/' + \
            dataset + '/' + user
        userFollowDict = json.load(open(userFollowDictPath))
        for follow in userFollowDict.keys():
            if userFollowDict[follow] == 1:
                userFollowDict.pop(follow)
        if len(userFollowDict) >= 1 :
            followDictAll[user] = userFollowDict
    return followDictAll


if __name__ == '__main__':
    d = ['FB']
    # d = ['GWL','FS']
    for i in d:
        print i, ': loadUserCheckinsCount'
        checkinCountDict = loadUserCheckinsCount(i)
        print i, ': conbineFollowDict'
        followDictAll = conbineFollowDict(i)
        print i, ': constructMatrix'
        idxDict, matrixList = constructMatrix(followDictAll, checkinCountDict)

        w = open('/home/moonorblue/socialINF/' + i + '/idxDict', 'w')
        w.write(json.dumps(idxDict))
        w.close()

        y = open('/home/moonorblue/socialINF/' + i + '/matrixList', 'w')
        y.write(json.dumps(matrixList))
        y.close()
