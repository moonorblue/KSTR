from sets import Set
from py2neo import Graph
from py2neo import Node, Relationship
import os
import itertools
from os import listdir
import json
import time
import cPickle as pickle
from copy import deepcopy
import sys
import re
import operator
import math
from py2neo.packages.httpstream import http
http.socket_timeout = 9999
from sortedcontainers import SortedList

g = Graph()


def getAllUser(user_l):
    query = 'MATCH (n:' + user_l + ') RETURN DISTINCT n.id;'
    request = g.cypher.execute(query)
    return request


def getCheckinsFromUser(user_l, uid, place_l):
    query = 'MATCH (n:' + user_l + \
        '{id:{uid}})-[r:VISITED]->(p:' + place_l + \
        ') RETURN r.atTime,p.id'
    queryDic = {"uid": uid}
    request = g.cypher.execute(query, queryDic)
    return request


def splitCheckinIntoRouteByDay(checkin_d, days):
    if len(checkin_d) == 0:
        return {}

    RouteDic = {}
    firstDay = float(checkin_d[0]['r.atTime'])
    for checkin in checkin_d:
        timestamp = float(checkin['r.atTime']) - firstDay
        day = int(timestamp / (86400 * days))
        if day in RouteDic:
            RouteDic[day].append(
                {'pid': checkin['p.id'].encode(), 'time': str(checkin['r.atTime'])})
        else:
            RouteDic[day] = []
            RouteDic[day].append(
                {'pid': checkin['p.id'].encode(), 'time': str(checkin['r.atTime'])})

    return RouteDic


def mainExtract(inPut):

    datasetLabel = ''
    datasetName = inPut[0]
    splitDay = inPut[1]

    if datasetName == 'FB':
        datasetLabel = ('User', 'Place')
    elif datasetName == 'FS':
        datasetLabel = ('FSUser', 'FSPlace')
    elif datasetName == 'GWL':
        datasetLabel = ('GWLUser', 'GWLPlace')
    elif datasetName == 'CA':
        datasetLabel = ('CAUser', 'CAPlace')

    allUsers = getAllUser(datasetLabel[0])
    checkPath = ('/home/moonorblue/routes/' + datasetName +
                 '/' + str(splitDay) + '/')
    checkSet = Set(listdir(checkPath))

    for User in allUsers:
        if User['n.id'].encode() + '.json' in checkSet:
            continue
        print 'Dataset:' + datasetName + '  User:' + User['n.id'].encode()
        checkins = getCheckinsFromUser(
            datasetLabel[0], User['n.id'].encode(), datasetLabel[1])
        routes = splitCheckinIntoRouteByDay(
            checkins, int(splitDay))  # split by splitDay
        jsonF = {'uid': User['n.id'].encode(), 'route': routes}

        f = open('/home/moonorblue/routes/' + datasetName +
                 '/' + str(splitDay) + '/' + User['n.id'].encode() + '.json', 'w')
        f.write(json.dumps(jsonF))
        f.close()


if __name__ == '__main__':
    # dsName = ['FB','CA','GWL','FS']
    dsName = ['FS']
    splitDays = [1, 7]
    for n in dsName:
        for d in splitDays:
            i = (n, d)
            mainExtract(i)
