#!flask/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify
from flask import request
from flask import make_response
from flask import abort
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper
import psycopg2
import json
import itertools
from os import listdir
import json
from sets import Set
import time as timer
from multiprocessing import Pool
import sys
import operator
from random import shuffle
import shutil
import datetime
_pool = None

def if_dominate(check, test):
    if check == test:
        return True
    for i in xrange(len(check)):
        if check[i] > test[i]:
            return True

    return False
def cal_dominate(input):
    check = input[0]
    inputd = input[1]
    # print inputd
    all_dominate = True
    for test in inputd:
        if if_dominate(check[1],test[1]) == False:
            all_dominate = False
            return None
    
    return check


def core3(swLng, swLat, neLng, neLat, selectUid, rawkeywords, stime, etime):
    startTime = timer.time()
    timelist = []
    keywords = rawkeywords.split(',')
        
    def KM(k,p):
        category = POIDict[p]['category']
        if k == category:
            tf = 1
        else:
            return 0
        
        idf = FBCategoryPOICountDict[k]         
        AT = FB_ATDict[k]
        score = (tf / float(idf))*AT
        return score

    def cal_re_in(select_rid, tuples):
        Total_PATS = 0.0
        Total_Timescore = 0.0
        Total_SocialINF = 0.0
        Total_KM = 0.0
        AllPOI = []

        if len(tuples) <= POILength:
            return
        for t in tuples:
            Total_PATS += t[2]
            Total_Timescore += t[3]
            Total_SocialINF += t[4]
            pid = t[0]
            time = t[1]
            lat = POIDict[pid]['latitude']
            lng = POIDict[pid]['longitude']
            name = POIDict[pid]['name']
            category = POIDict[pid]['category']
            link = POIDict[pid]['link']
            likes = POIDict[pid]['likes']
            checkins = POIDict[pid]['checkins']

            for keyword in keywords:
                Total_KM += KM(keyword,pid)

            POITuple = {
                'pid': pid, 'time': time, 'coor': [lat, lng], 'name': name,'category':category,'link':link,'likes':likes,'checkins':checkins} 
            # POITuple = {
                # 'pid': pid, 'time': time, 'coor': [lat, lng], 'name': name}
            AllPOI.append(POITuple)

        rScore = 0.0

        rScore = Total_PATS + Total_Timescore + Total_SocialINF
        POICount = len(tuples)
        cover = 0.0

        avg_rScore = float(rScore) / POICount

        reconstructionFlag = True
        tup = uid, orignal_rid, select_rid, rScore, avg_rScore, 0, 0, 0, 0, 0, 0, 0, Total_PATS, Total_Timescore, Total_SocialINF, float(
            Total_PATS) / POICount, float(Total_Timescore) / POICount, float(Total_SocialINF) / POICount, 0, 0, AllPOI,Total_KM
        return tup

    def getMinAndMax(lats, longs):
        return str(min(lats)), str(min(longs)), str(max(lats)), str(max(longs))

    def splitIntoHeadDict(route):
        length = len(route)
        for i in xrange(length):
            if i == length - 1:
                break
            headID = route[i][0]
            tailID = route[i + 1][0]
            head = POIDataDict[headID]
            tail = POIDataDict[tailID]
            if head[0] == tail[0] or head[1] >= tail[1]:
                continue
            if head[0] not in splitDict:
                splitDict[head[0]] = Set([])
                splitDict[head[0]].add((head, tail))
            else:
                splitDict[head[0]].add((head, tail))

    def construct(pairSet):
        endflag = False

        global construct_c
        global reconstructionIdx

        for i in pairSet:

            if len(tempStack) == 0:
                tempStack.append(i[0])
                tempStack.append(i[1])
            else:
                idx = len(tempStack) - 1

                if i[1][1] > tempStack[idx][1] and i[1][0] != tempStack[idx][0]:
                    tempStack.append(i[0])
                    tempStack.append(i[1])
                else:
                    tempStack.append(i[0])
                    endflag = True

            headSet = splitDict.get(i[0][0], None)
            tailSet = splitDict.get(i[1][0], None)

            if tailSet != None and endflag == False:
                tempStack.pop()
                construct(tailSet)

                if len(tempStack) <= 1:
                    pass
                else:
                    x_p = []
                    tempStack_cpy = []
                    score = 0.0
                    for i in tempStack:
                        x_p.append(i[0])
                        tempStack_cpy.append(i)
                        score += (i[2] + i[3] + i[4])

                    if tuple(x_p) not in prefixSet:
                        #make prefix
                        prefix = []
                        length = len(x_p)
                        for i in xrange(length):
                            if i < length - 1:
                                prefix.append(x_p[i])
                                prefixSet.add(tuple(prefix))

                        if tuple(x_p) not in reconstructionInput_p:
                            if tuple(x_p) in orignalRouteScore:
                                if score > orignalRouteScore[tuple(x_p)]:
                                    r_rid = 'Reconstruct_' + str(reconstructionIdx)
                                    reconstructionOutput.append(
                                        cal_re_in(r_rid, tempStack))
                                    reconstructionIdx += 1
                                    reconstructionInput_p.add(tuple(x_p))
                            else:
                                r_rid = 'Reconstruct_' + str(reconstructionIdx)
                                reconstructionOutput.append(
                                    cal_re_in(r_rid, tempStack))
                                reconstructionIdx += 1
                                reconstructionInput_p.add(tuple(x_p))
                tempStack.pop()
            elif endflag == True:
                if len(tempStack) == 1:
                    pass
                else:
                    x_p = []
                    tempStack_cpy = []
                    score = 0.0
                    for i in tempStack:
                        x_p.append(i[0])
                        tempStack_cpy.append(i)
                        score += (i[2] + i[3] + i[4])

                    if tuple(x_p) not in prefixSet:
                        #make prefix
                        prefix = []
                        length = len(x_p)
                        for i in xrange(length):
                            if i < length - 1:
                                prefix.append(x_p[i])
                                prefixSet.add(tuple(prefix))

                        if tuple(x_p) not in reconstructionInput_p:
                            if tuple(x_p) in orignalRouteScore:
                                if score > orignalRouteScore[tuple(x_p)]:
                                    r_rid = 'Reconstruct_' + str(reconstructionIdx)
                                    reconstructionOutput.append(
                                        cal_re_in(r_rid, tempStack))
                                    reconstructionIdx += 1
                                    reconstructionInput_p.add(tuple(x_p))
                            else:
                                r_rid = 'Reconstruct_' + str(reconstructionIdx)
                                reconstructionOutput.append(
                                    cal_re_in(r_rid, tempStack))
                                reconstructionIdx += 1
                                reconstructionInput_p.add(tuple(x_p))

            else:
                if len(tempStack) == 1:
                    pass
                else:
                    x_p = []
                    tempStack_cpy = []
                    score = 0.0
                    for i in tempStack:
                        x_p.append(i[0])
                        tempStack_cpy.append(i)
                        score += (i[2] + i[3] + i[4])

                    if tuple(x_p) not in prefixSet:
                        #make prefix
                        prefix = []
                        length = len(x_p)
                        for i in xrange(length):
                            if i < length - 1:
                                prefix.append(x_p[i])
                                prefixSet.add(tuple(prefix))

                        if tuple(x_p) not in reconstructionInput_p:
                            if tuple(x_p) in orignalRouteScore:
                                if score > orignalRouteScore[tuple(x_p)]:
                                    r_rid = 'Reconstruct_' + str(reconstructionIdx)
                                    reconstructionOutput.append(
                                        cal_re_in(r_rid, tempStack))
                                    reconstructionIdx += 1
                                    reconstructionInput_p.add(tuple(x_p))
                            else:
                                r_rid = 'Reconstruct_' + str(reconstructionIdx)
                                reconstructionOutput.append(
                                    cal_re_in(r_rid, tempStack))
                                reconstructionIdx += 1
                                reconstructionInput_p.add(tuple(x_p))
                        for i in xrange(2):
                            tempStack.pop()
                            if len(tempStack) <= 1:
                                pass
                            else:
                                x_p = []
                                tempStack_cpy = []
                                score = 0.0
                                for i in tempStack:
                                    x_p.append(i[0])
                                    tempStack_cpy.append(i)
                                    score += (i[2] + i[3] + i[4])

                                if tuple(x_p) not in prefixSet:
                                    #make prefix
                                    prefix = []
                                    length = len(x_p)
                                    for i in xrange(length):
                                        if i < length - 1:
                                            prefix.append(x_p[i])
                                            prefixSet.add(tuple(prefix))

                                    if tuple(x_p) not in reconstructionInput_p:
                                        if tuple(x_p) in orignalRouteScore:
                                            if score > orignalRouteScore[tuple(x_p)]:
                                                r_rid = 'Reconstruct_' + \
                                                    str(reconstructionIdx)
                                                reconstructionOutput.append(
                                                    cal_re_in(r_rid, tempStack))
                                                reconstructionIdx += 1
                                                reconstructionInput_p.add(tuple(x_p))
                                        else:
                                            r_rid = 'Reconstruct_' + \
                                                str(reconstructionIdx)
                                            reconstructionOutput.append(
                                                cal_re_in(r_rid, tempStack))
                                            reconstructionIdx += 1
                                            reconstructionInput_p.add(tuple(x_p))

    # def if_dominate(check, test):
    #     if check == test:
    #         return True
    #     for i in xrange(len(check)):
    #         if check[i] > test[i]:
    #             return True

    #     return False

    # def cal_dominate(input):
    #     check = input[0]
    #     inputd = input[1]
    #     all_dominate = True
    #     for test in inputd:
    #         if if_dominate(check[1], test[1]) == False:
    #             all_dominate = False
    #             return None

    #     return check

    pro = 0.1
    POILength = 2
    conn_string = "host='192.168.100.200' dbname='moonorblue' user='moonorblue' password='4321'"
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()

    qByRegion = "SELECT poi,rid FROM fb_route WHERE geom && st_makeenvelope(" + str(swLng) + "," + str(swLat) + "," + str(neLng) + "," + str(
        neLat) + ",4326) AND st_area(geom) != 0 AND (st_area(st_intersection(geom,st_makeenvelope(" + str(swLng) + "," + str(swLat) + "," + str(neLng) + "," + str(neLat) + ",4326)))) != 0;"
    cur.execute(qByRegion)
    qByRegion_rows = [r for r in cur]
    timelist.append('Query:'+str(timer.time()-startTime))
    startTime = timer.time()
    orignalCategory = Set([])
    orignalPOI = Set([])

    minlong = float(swLng)
    minlat = float(swLat)
    maxlong = float(neLng)
    maxlat = float(neLat)

    uid = str(selectUid)
    orignal_rid = 0
    fids = RelationDict.get(uid, [])
    fids = Set(fids)

    reconstruction_start = timer.time()
    splitDict = {}

    reconstructionInput = []
    reconstructionOutput = []
    reconstructionOutputSet = Set([])
    global reconstructionIdx
    reconstructionIdx = 0

    scoreD = {}
    POIScoreDict = {}
    POIDataDict = {}
    c = 0
    qCount = 0
    for r in qByRegion_rows:
        # break if too much result
        if qCount > 10000:
            break
        POIs = eval(r[0])
        rid = r[1]
        localInput = []
        score = 0.0
        for POI in POIs:
            pid = POI['pid']

            latitude = POIDict[pid]['latitude']
            longitude = POIDict[pid]['longitude']
            if latitude >= minlat and latitude <= maxlat and longitude >= minlong and longitude <= maxlong:
                PATS = POI['PATS']
                timescore = POI['timeScore']
                socialINF = 0.0
                KMs=0.0
                time = int(datetime.datetime.fromtimestamp(float(POI['time'])).strftime('%H')) + 8
                if time > 24:
                    time = time - 24
                category = POIDict[pid]['category']
                visiters = Set(POIDict[pid]['visiters'])
                # select social influnce score
                for v in visiters:
                    if str(v) not in fids:
                        continue
                    new_u = FBsInfIdxDict[uid]
                    new_f = FBsInfIdxDict[v]
                    scores = FBsInfMatrix[new_u][new_f]
                    socialINF += float(scores)
                for keyword in keywords:
                    KMs += KM(keyword,pid)
                score += (PATS + timescore + socialINF+KMs)

                localInput.append(
                    (pid, time, PATS, timescore, socialINF, category))

                if pid not in POIScoreDict:
                    POIScoreDict[pid] = PATS + timescore + socialINF+KMs
                    POIDataDict[pid] = (
                        pid, time, PATS, timescore, socialINF, category)
                else:
                    if (PATS + timescore + socialINF + KMs) > POIScoreDict[pid]:
                        POIDataDict[pid] = (
                            pid, time, PATS, timescore, socialINF, category)
            else:
                continue

        scoreD[c] = score
        c += 1
        qCount += 1
        reconstructionInput.append(tuple(localInput))
    timelist.append('POI:'+str(timer.time()-startTime))
    startTime = timer.time()
    sorted_scoreD = sorted(
        scoreD.items(), key=operator.itemgetter(1), reverse=True)
    limit = pro * len(sorted_scoreD)
    chosedInput = []
    reconstructionInput_p = []
    orignalRouteScore = {}

    for i in xrange(int(limit)):
        chosedInput.append(sorted_scoreD[i][0])

    for i in chosedInput:

        splitIntoHeadDict(reconstructionInput[i])
        t = []
        score = 0.0
        for x in reconstructionInput[i]:
            t.append(x[0])
            score += (x[2] + x[3] + x[4])
        orignalRouteScore[tuple(t)] = score

    reconstructionInput_p = Set(reconstructionInput_p)
    prefixSet = Set()

    for i in splitDict:
        tempStack = []
        construct_c = 0
        construct(splitDict[i])
    timelist.append('Construct:'+str(timer.time()-startTime))
    startTime = timer.time()
    routeList = []
    result = []
    qCoverTime = 0.0
    ScoringTime = 0.0
    ProcessTime = 0.0
    qCount = 0
    for row_r in qByRegion_rows:
        # break if too much result
        if qCount > 10000:
            break
        process_start_time = timer.time()
        select_rid = row_r[1]

        if orignal_rid == select_rid:
            continue

        cover = 0
        POIs = eval(row_r[0])
        if len(POIs) <= POILength:
            continue

        rScore = 0.0
        recommendCategory = Set([])
        socialFlag = False
        POICount = len(POIs)
        recommendPOI = Set([])
        scoring_start_time = timer.time()

        Total_PATS = 0.0
        Total_Timescore = 0.0
        Total_SocialINF = 0.0
        Total_KM = 0.0

        AllPOI = []
        for POI in POIs:
            pid = POI['pid']
            PATS = POI['PATS']
            timescore = POI['timeScore']
            time = int(datetime.datetime.fromtimestamp(float(POI['time'])).strftime('%H')) + 8
            if time > 24:
                time = time - 24

            socialINF = 0.0

            latitude = POIDict[pid]['latitude']
            longitude = POIDict[pid]['longitude']

            if latitude >= minlat and latitude <= maxlat and longitude >= minlong and longitude <= maxlong:
                visiters = Set(POIDict[pid]['visiters'])
                # select social influnce score
                for v in visiters:
                    if str(v) not in fids:
                        continue
                    new_u = FBsInfIdxDict[uid]
                    new_f = FBsInfIdxDict[v]
                    scores = FBsInfMatrix[new_u][new_f]
                    socialFlag = True
                    socialINF += float(scores)

                Total_PATS += PATS
                Total_Timescore += timescore
                Total_SocialINF += socialINF
                for keyword in keywords:
                    Total_KM += KM(keyword,pid)

                pScore = PATS + timescore + socialINF
                rScore += pScore

            name = POIDict[pid]['name']
            category = POIDict[pid]['category']
            link = POIDict[pid]['link']
            likes = POIDict[pid]['likes']
            checkins = POIDict[pid]['checkins']
            POITuple = {
                'pid': pid, 'time': time, 'coor': [latitude, longitude], 'name': name,'category':category,'link':link,'likes':likes,'checkins':checkins}
            # POITuple = {'pid': pid, 'time': time , 'coor': [latitude, longitude], 'name': name}
            AllPOI.append(POITuple)

        avg_rScore = float(rScore) / POICount

        poi_hitCount = 0
        poiHit = 0
        editdistance = 0
        hitCount = 0
        categoryHit = 0
        ScoringTime = 0
        ProcessTime = 0

        reconstructionFlag = False
        tup = uid, orignal_rid, select_rid, rScore, avg_rScore, categoryHit, cover, poi_hitCount, poiHit, socialFlag, ScoringTime, ProcessTime, Total_PATS, Total_Timescore, Total_SocialINF, float(
            Total_PATS) / POICount, float(Total_Timescore) / POICount, float(Total_SocialINF) / POICount, editdistance, reconstructionFlag, AllPOI, Total_KM
        result.append(tup)
        qCount += 1
    
    
    result += reconstructionOutput
    timelist.append('Scoring:'+str(timer.time()-startTime))
    startTime = timer.time()
    result = [d for d in result if d is not None]
    # pool_size = 8  # your "parallelness"

    # _pool = Pool(pool_size)
    # xxx = _pool.map(cal,qByRegion_rows)

    #remove subsequence
    # POISequence = []
    # for i in result:
    #     if i is not None:
    #         POIs = i[20]
    #         Seq = ''
    #         for POI in POIs:
    #             Seq += POI['pid']
    #             Seq += ','
    #         POISequence.append(Seq)
    
    # seqIdx = 0
    # for seq in POISequence:
    #     for seqq in POISequence:
    #         if seq == seqq:
    #             continue
    #         if seq in seqq:
    #             result[seqIdx] = None
    #             break
    #     seqIdx += 1

    # timelist.append('Remove subseq:'+str(timer.time()-startTime))
    # startTime = timer.time()
    result_new = []
    #time constraint here!!!
    if stime == 'Anytime' and etime == 'Anytime':
        for i in result:
            if i is not None:
                POIs = i[20]
                nTuple = i + (POIs,)
                result_new.append(nTuple)
        pass
    elif stime == 'Anytime':
        endTime=int(etime.replace(':00',''))
        for i in result:
            if i is not None:
                POIs = i[20]
                newPOIs = []
                for POI in POIs:
                    time = POI['time'] 
                    if int(time) <= endTime:
                        newPOIs.append(POI)
                if len(newPOIs) > 1:
                    nTuple = i + (newPOIs,)
                    result_new.append(nTuple)
    elif etime == 'Anytime':
        startTime=int(stime.replace(':00',''))
        for i in result:
            if i is not None:
                POIs = i[20]
                newPOIs = []
                for POI in POIs:
                    time = POI['time'] 
                    if int(time) >= startTime:
                        newPOIs.append(POI)
                if len(newPOIs) > 1:
                    nTuple = i + (newPOIs,)
                    result_new.append(nTuple)
    else:
        startTime=int(stime.replace(':00',''))
        endTime=int(etime.replace(':00',''))
        for i in result:
            if i is not None:
                POIs = i[20]
                newPOIs = []
                for POI in POIs:
                    time = POI['time'] 
                    if int(time) >= startTime and int(time) <= endTime:
                        newPOIs.append(POI)
                if len(newPOIs) > 1:
                    nTuple = i + (newPOIs,)
                    result_new.append(nTuple)
    timelist.append('Time:'+str(timer.time()-startTime))
    startTime = timer.time()

    skylineInputDict = {}
    skylineInputValue = []
    skylineInputDict_avg = {}
    skylineInputValue_avg = []
    idxCount = 0
    for t in result_new:
        rid = t[2]
        ScoringTime += t[10]
        ProcessTime += t[11]
        # skylineT = (t[12], t[13], t[14])
        skylineT_avg = (t[15], t[16], t[17],t[21])
        # skylineInputDict[(rid, skylineT)] = idxCount
        skylineInputDict_avg[(rid, skylineT_avg)] = idxCount
        # skylineInputValue.append((rid, skylineT))
        skylineInputValue_avg.append((rid, skylineT_avg))
        idxCount += 1
    

    # _pool = Pool(8)
    r = _pool.map(cal_dominate,itertools.izip(skylineInputValue_avg, itertools.repeat(skylineInputValue_avg)))
    # r = [i for i in r if i is not None]
    resultData_avg = [result_new[skylineInputDict_avg[i]] for i in r if i is not None]
    # pool_skyline.close()
    # pool_skyline.join()
    # r = []

    # for i in skylineInputValue_avg:
    #     all_dominate = True
    #     for j in skylineInputValue_avg:
    #         if if_dominate(i[1], j[1]) == False:
    #             all_dominate = False
    #             break
    #     if all_dominate:
    #         r.append(i)

    # resultData_avg = [result_new[skylineInputDict_avg[i]] for i in r]
    timelist.append('Skyline:'+str(timer.time()-startTime))
    startTime = timer.time()  


    startTime = timer.time()
    #sorting by PATS
    sorted_by_PATS = sorted(result_new, reverse=True, key=lambda tup: tup[12])[:len(resultData_avg)] 
    #sorting by timescore
    sorted_by_timescore = sorted(result_new, reverse=True, key=lambda tup: tup[13])[:len(resultData_avg)]
    #sorting by socialINF 
    sorted_by_socialINF = sorted(result_new, reverse=True, key=lambda tup: tup[14])[:len(resultData_avg)]
    #sorting by KM
    sorted_by_KM = sorted(result_new, reverse=True, key=lambda tup: tup[21])[:len(resultData_avg)]



    resultPOI_skyline = [i[22] for i in resultData_avg]
    resultPOI_skyline_ori = [i[22] for i in resultData_avg if 'Reconstruct_' not in str(i[2])]
    resultPOI_skyline_re = [i[22] for i in resultData_avg if 'Reconstruct_' in str(i[2])]
    resultPOI_PATS = [i[22] for i in sorted_by_PATS]
    resultPOI_timescore = [i[22] for i in sorted_by_timescore]
    resultPOI_socialINF = [i[22] for i in sorted_by_socialINF]
    resultPOI_KM = [i[22] for i in sorted_by_KM]
    timelist.append('Sort:'+str(timer.time()-startTime))
    startTime = timer.time()
    return resultPOI_skyline,resultPOI_PATS,resultPOI_timescore,resultPOI_socialINF,resultPOI_skyline_ori,resultPOI_skyline_re,resultPOI_KM
    # return timelist
def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator







app = Flask(__name__)

FBsInfIdxDict = json.load(open('/home/moonorblue/socialINF/FB/idxDict'))
FBsInfMatrix = json.load(open('/home/moonorblue/socialINF/FB/matrixList'))
POIDict = json.load(open('/home/moonorblue/exp/materials/FB_POIDict'))

FBCategoryPOICountDict = json.load(open('/home/moonorblue/exp/materials/FB_CategoryPOICount'))
FBPOICountDict = json.load(open('/home/moonorblue/exp/materials/FB_POICount'))
FBUserPOICountDict = json.load(open('/home/moonorblue/exp/materials/FB_userPOICheckinCount'))
FB_ATDict = json.load(open('/home/moonorblue/exp/materials/FB_AT'))

RelationDict = json.load(
    open('/home/moonorblue/exp/materials/FB_relationDict'))


@app.route('/KSTR/api/v1.2/query/', methods=['GET'])
@crossdomain(origin='*')
def runKSTR3():
    uid = request.args['uid']
    uidv = '';
    if uid == 'User A':
        uidv = '100000207307379'
    elif uid == 'User B':
        uidv = '1804765491'
    elif uid == 'User C': 
        uidv = '100000120466143'
    elif uid == 'User D':
        uidv = '1135350371'
    elif uid == 'User E': 
        uidv = '100001454398148'
    elif uid == 'User F':
        uidv = '1517749004'
    elif uid == 'User G':
        uidv = '1545167581'
    elif uid == 'User H':
        uidv = '1120337880'
    elif uid == 'User I':
        uidv = '100000286470014'
    elif uid == 'User J':
        uidv = '100000968176510'
    elif uid == '':
        uidv = '100000207307379'
    
    x = core3(request.args['swLng'], request.args['swLat'], request.args[
             'neLng'], request.args['neLat'], uidv, request.args['keywords'],request.args['stime'],request.args['etime'])

    return jsonify({'data_skyline': x[0],'data_pats': x[1],'data_timescore': x[2],'data_socialinf': x[3],'data_skyline_ori':x[4],'data_skyline_re':x[5],'data_KM':x[6]})
    # return json.dumps(x)


if __name__ == '__main__':
    app.debug = True
    try:
        _pool = Pool(8)
        app.run(host="0.0.0.0",threaded=True)
    except KeyboardInterrupt:
        _pool.close()
        _pool.join()
