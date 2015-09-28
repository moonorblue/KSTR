import psycopg2
import itertools
from os import listdir
import json
from sets import Set
import time as timer
# from multiprocessing.pool import ThreadPool as Pool
from multiprocessing import Pool
import sys
import operator
# from shapely.geometry import box,Point
import shutil
import datetime
from math import sqrt 

# keywords = []

def getMinAndMax(lats, longs):
    return str(min(lats)), str(min(longs)), str(max(lats)), str(max(longs))


def splitIntoHeadDict(route):
    length = len(route)
    for i in xrange(length):
        if i == length -1:
            break
        headID = route[i][0]
        tailID = route[i+1][0] 
        head = POIDataDict[headID]
        tail = POIDataDict[tailID] 
        tailScore = float(tail[2]+tail[3])
        if head[0] == tail[0] or head[1] >= tail[1]:
            continue
        if head[0] not in splitDict:
            splitDict[head[0]] = Set([])
            splitDict[head[0]].add((head,tail))
        else:
            splitDict[head[0]].add((head,tail))

def construct(pairSet):
    endflag = False
    # print pairSet
    global construct_c 
    global reconstructionIdx
    # construct_c += 1
    # if construct_c == 1:
        # endflag =True
    # construct_c += 1
    # print 'ORI: ',tempStack, endflag
    for i in pairSet:
        # if i[1][1] < i[0][1]:
        if len(tempStack) == 0:
            tempStack.append(i[0])
            tempStack.append(i[1])
        else:
            idx = len(tempStack) - 1
            # print i[1][1],' ',tempStack[idx][1]
            # print i[1][0],' ',tempStack[idx][0]
            if i[1][1] > tempStack[idx][1] and i[1][0] != tempStack[idx][0]:
                 tempStack.append(i[0])
                 tempStack.append(i[1])
                 # print 'hi'
            else:
                 # if tempStack[idx][0] != i[0][0]: 
                 tempStack.append(i[0])
                 # print 'no'
                 endflag = True

        # print 'ORI!!!: ',tempStack, endflag
        headSet = splitDict.get(i[0][0],None)
        tailSet = splitDict.get(i[1][0],None)
        # print tailSet
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
                    score += (i[2]+i[3]+i[4])
                if tuple(x_p) not in prefixSet:
                    #make prefix
                    prefix = []
                    length = len(x_p)
                    for i in xrange(length):
                        if i < length - 1:
                            prefix.append(x_p[i])
                            prefixSet.add(tuple(prefix))

                    if tuple(x_p) not in reconstructionInput_p :
                        if tuple(x_p) in orignalRouteScore:
                            if score > orignalRouteScore[tuple(x_p)]:
                                reconstructionOutput['Reconstruct_'+str(reconstructionIdx)] = tempStack_cpy
                                reconstructionIdx += 1
                                reconstructionInput_p.add(tuple(x_p))
                        else:
                            reconstructionOutput['Reconstruct_'+str(reconstructionIdx)] = tempStack_cpy
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
                    score += (i[2]+i[3]+i[4])

                if tuple(x_p) not in prefixSet:
                    #make prefix
                    prefix = []
                    length = len(x_p)
                    for i in xrange(length):
                        if i < length - 1:
                            prefix.append(x_p[i])
                            prefixSet.add(tuple(prefix))

                    if tuple(x_p) not in reconstructionInput_p :
                        if tuple(x_p) in orignalRouteScore:
                            if score > orignalRouteScore[tuple(x_p)]:
                                reconstructionOutput['Reconstruct_'+str(reconstructionIdx)] = tempStack_cpy
                                reconstructionIdx += 1
                                reconstructionInput_p.add(tuple(x_p))
                        else:
                            reconstructionOutput['Reconstruct_'+str(reconstructionIdx)] = tempStack_cpy
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
                    score += (i[2]+i[3]+i[4])

                if tuple(x_p) not in prefixSet:
                    #make prefix
                    prefix = []
                    length = len(x_p)
                    for i in xrange(length):
                        if i < length - 1:
                            prefix.append(x_p[i])
                            prefixSet.add(tuple(prefix))
                    if tuple(x_p) not in reconstructionInput_p :
                        if tuple(x_p) in orignalRouteScore:
                            if score > orignalRouteScore[tuple(x_p)]:
                                reconstructionOutput['Reconstruct_'+str(reconstructionIdx)] = tempStack_cpy
                                reconstructionIdx += 1
                                reconstructionInput_p.add(tuple(x_p))
                        else:
                            reconstructionOutput['Reconstruct_'+str(reconstructionIdx)] = tempStack_cpy
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
                                score += (i[2]+i[3]+i[4]) 

                            if tuple(x_p) not in prefixSet:
                                #make prefix
                                prefix = []
                                length = len(x_p)
                                for i in xrange(length):
                                    if i < length - 1:
                                        prefix.append(x_p[i])
                                        prefixSet.add(tuple(prefix))
                                if tuple(x_p) not in reconstructionInput_p :
                                    if tuple(x_p) in orignalRouteScore:
                                        if score > orignalRouteScore[tuple(x_p)]:
                                            reconstructionOutput['Reconstruct_'+str(reconstructionIdx)] = tempStack_cpy
                                            reconstructionIdx += 1
                                            reconstructionInput_p.add(tuple(x_p))
                                    else:
                                        reconstructionOutput['Reconstruct_'+str(reconstructionIdx)] = tempStack_cpy
                                        reconstructionIdx += 1
                                        reconstructionInput_p.add(tuple(x_p))




def levenshtein(a,b):
    "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a,b = b,a
        n,m = m,n
        
    current = range(n+1)
    for i in range(1,m+1):
        previous, current = current, [i]+[0]*n
        for j in range(1,n+1):
            add, delete = previous[j]+1, current[j-1]+1
            change = previous[j-1]
            if a[j-1] != b[i-1]:
                change = change + 1
            current[j] = min(add, delete, change)
            
    return current[n]

def if_dominate(check,test):
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

def cal_re(row):

    process_start_time = timer.time()
    select_rid = row[0]
    
    if orignal_rid == select_rid:
        return
    

    POIs = row[1]
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
    longs = []
    lats = []
    for POI in POIs:
        pid = POI[0]
        PATS = POI[2]
        timescore = POI[3]
        time = POI[1]
        socialINF = 0.0
        recommendPOI.add((pid,float(time)))

        category = POIDict[pid]['category']
        recommendCategory.add(category)

        latitude = POIDict[pid]['latitude']
        longitude = POIDict[pid]['longitude']
        lats.append(latitude)
        longs.append(longitude)
        
        for keyword in keywords:
            Total_KM += KM(keyword,pid)
        
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

        pScore = PATS + timescore + socialINF
        rScore += pScore
    # cover = None

    minlat, minlong, maxlat, maxlong = getMinAndMax(lats,longs)    

    cover = 100.0
    cStart = timer.time()
    # recommend_box = box(float(minlong),float(minlat),float(maxlong),float(maxlat))
    # try:
    #     cover = (recommend_box.intersection(orignal_box).area / orignal_box.area) * 100
    # except:
    #     cover = 0.0

    # if cover == 0.0:
    #     return


    avg_rScore = float(rScore) / POICount

    # POI hitness
    poi_hitCount = 0
    for p in recommendPOI:
        if p in orignalPOI:
            poi_hitCount += 1
    poiHit = float(poi_hitCount) / len(orignalPOI) * 100


    #edit distance
    sorted_recommendPOI = [i[0] for i in sorted(recommendPOI, reverse=False, key=lambda tup: tup[1])]
    sorted_orignalPOI = [i[0] for i in sorted(orignalPOI, reverse=False, key=lambda tup: tup[1])]
    editdistance = levenshtein(sorted_orignalPOI,sorted_recommendPOI)    


    hitCount = 0
    for cate_r in recommendCategory:
        if cate_r in orignalCategory:
            hitCount += 1
    categoryHit = float(hitCount) / len(orignalCategory) * 100
    cosine = float(hitCount) / (sqrt(len(recommendCategory)) * sqrt(len(orignalCategory)))
    ScoringTime = timer.time() - scoring_start_time
    ProcessTime = timer.time() - process_start_time

    reconstructionFlag = True
    tup = uid,orignal_rid, select_rid, rScore, avg_rScore, categoryHit, cover, poi_hitCount, poiHit, socialFlag, ScoringTime, ProcessTime, Total_PATS, Total_Timescore, Total_SocialINF,float(Total_PATS)/POICount, float(Total_Timescore)/POICount, float(Total_SocialINF)/POICount,editdistance,reconstructionFlag,cosine,Total_KM
    return tup

def cal(row_r):

    process_start_time = timer.time()
    select_rid = row_r[1]
    
    if orignal_rid == select_rid:
        return
    cover = float(row_r[2])
    POIs = eval(row_r[0])
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
    for POI in POIs:
        pid = POI['pid']
        PATS = POI['PATS']
        timescore = POI['timeScore']
        time = POI['time']
        socialINF = 0.0
        recommendPOI.add((pid,float(time)))
        
        category = POIDict[pid]['category']
        recommendCategory.add(category)

        latitude = POIDict[pid]['latitude']
        longitude = POIDict[pid]['longitude']
        visiters = Set(POIDict[pid]['visiters'])

        for keyword in keywords:
            Total_KM += KM(keyword,pid)
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

        pScore = PATS + timescore + socialINF
        rScore += pScore
    
    avg_rScore = float(rScore) / POICount

    # POI hitness
    poi_hitCount = 0
    for p in recommendPOI:
        if p in orignalPOI:
            poi_hitCount += 1
    poiHit = float(poi_hitCount) / len(orignalPOI) * 100


    #edit distance
    sorted_recommendPOI = [i[0] for i in sorted(recommendPOI, reverse=False, key=lambda tup: tup[1])]
    sorted_orignalPOI = [i[0] for i in sorted(orignalPOI, reverse=False, key=lambda tup: tup[1])]
    editdistance = levenshtein(sorted_orignalPOI,sorted_recommendPOI)    


    hitCount = 0
    for cate_r in recommendCategory:
        if cate_r in orignalCategory:
            hitCount += 1
    categoryHit = float(hitCount) / len(orignalCategory) * 100
    cosine = float(hitCount) / (sqrt(len(recommendCategory)) * sqrt(len(orignalCategory)))
    ScoringTime = timer.time() - scoring_start_time
    ProcessTime = timer.time() - process_start_time

    reconstructionFlag = False
    tup = uid,orignal_rid, select_rid, rScore, avg_rScore, categoryHit, cover, poi_hitCount, poiHit, socialFlag, ScoringTime, ProcessTime, Total_PATS, Total_Timescore, Total_SocialINF,float(Total_PATS)/POICount, float(Total_Timescore)/POICount, float(Total_SocialINF)/POICount,editdistance,reconstructionFlag,cosine,Total_KM

    return tup
    
pro = [0.1]
conn_string = "host='192.168.100.200' dbname='moonorblue' user='moonorblue' password='4321'"
conn = psycopg2.connect(conn_string)
cur = conn.cursor()
query = "SELECT a.poi,a.region_minlong,a.region_minlat,a.region_maxlong,a.region_maxlat,a.uid,a.rid,a.geom FROM fb_route a,fb_checkincount b WHERE b.uid = a.uid AND st_area(a.geom) != 0 ORDER BY b.checkincount,a.rid ;"
cur.execute(query)
rows = [r for r in cur]

FBsInfIdxDict = json.load(open('/home/moonorblue/socialINF/FB/idxDict'))
FBsInfMatrix = json.load(open('/home/moonorblue/socialINF/FB/matrixList'))
POIDict = json.load(open('/home/moonorblue/exp/materials/FB_POIDict'))
RelationDict = json.load(open('/home/moonorblue/exp/materials/FB_relationDict'))

FBCategoryPOICountDict = json.load(open('/home/moonorblue/exp/materials/FB_CategoryPOICount'))
FBPOICountDict = json.load(open('/home/moonorblue/exp/materials/FB_POICount'))
FBUserPOICountDict = json.load(open('/home/moonorblue/exp/materials/FB_userPOICheckinCount'))
FB_ATDict = json.load(open('/home/moonorblue/exp/materials/FB_AT'))

doneSet = Set([])

for p in pro: 
   
    conn_string = "host='192.168.100.200' dbname='moonorblue' user='moonorblue' password='4321'"
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()



    start_time = timer.time()
    avgReconstructTime = 0.0
    avgOri = 0.0
    avgLength = 0.0

    length = len(rows)
    StopNumbers = Set([10000,15000,20000,25000,30000,35000,40000,50000])
    progressCount = 1

    for row in rows:
        # print len(qByRegion_rows)
        print 'fb ',str(p)+" Start # "+str(progressCount)+"/"+str(length)+"\n"  
        # if progressCount > 20000:
        #     break
        o_rid = str(row[6])
        if o_rid in doneSet:
            progressCount += 1
            continue

        qByRegion = "SELECT poi,rid,(st_area(st_intersection(geom,'" + str(row[7])+ "'))/st_area('"+str(row[7])+"'))*100 FROM fb_route WHERE geom && '"+str(row[7])+"' AND st_area(geom) != 0 AND st_area('"+str(row[7])+"') != 0 AND (st_area(st_intersection(geom, '"+str(row[7])+"'))/st_area('"+str(row[7])+"')) != 0"
        qByRegion_start_time = timer.time()
        cur.execute(qByRegion)
        qByRegion_rows = [r for r in cur]

        start_time = timer.time()
        # poi information
        orignalCategory = Set([])
        orignalPOI = Set([])
        POIs = eval(row[0])
        keywords = []
        for POI in POIs:
            pid = POI['pid']
            PATS = POI['PATS']
            timescore = POI['timeScore']
            time = POI['time']
            orignalPOI.add((pid,float(time)))
            ###########
            category = POIDict[pid]['category']
            orignalCategory.add(category)
            keywords.append(str(category))
        orignal_minlong = float(row[1])
        orignal_minlat = float(row[2])
        orignal_maxlong = float(row[3])
        orignal_maxlat = float(row[4])
        # orignal_box = box(orignal_minlong,orignal_minlat,orignal_maxlong,orignal_maxlat)
        uid = row[5]
        orignal_rid = str(row[6])
        #get relation users
        fids = RelationDict.get(uid,[])
        fids = Set(fids)
        
        
       
        # reconstruction
        reconstruction_start = timer.time()
        splitDict = {}
        reconstructionInput = []
        reconstructionOutput = {}
        reconstructionOutputSet = Set([])
        reconstructionIdx = 0

        scoreD = {}
        POIScoreDict = {}
        POIDataDict = {}
        c = 0
        for r in qByRegion_rows:
            POIs = eval(r[0])
            rid = r[1]
            localInput = []
            score = 0.0
            for POI in POIs:
                pid = POI['pid']

                latitude = POIDict[pid]['latitude']
                longitude = POIDict[pid]['longitude']
                if latitude >= orignal_minlat and latitude <= orignal_maxlat and longitude >= orignal_minlong and longitude <= orignal_maxlong: 
                    PATS = POI['PATS']
                    timescore = POI['timeScore']
                    socialINF = 0.0
                    KMs=0.0
                    # time = float(POI['time'])
                    time =  int(datetime.datetime.fromtimestamp(float(POI['time'])).strftime('%H'))
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

                    localInput.append((pid,time,PATS,timescore,socialINF,category))
                    # localInput.append((pid,time,PATS,timescore,category))

                    if pid not in POIScoreDict:
                        POIScoreDict[pid] = PATS + timescore + socialINF+KMs
                        POIDataDict[pid] = (pid,time,PATS,timescore,socialINF,category)
                    else:
                        if (PATS + timescore + socialINF+KMs) > POIScoreDict[pid]:
                            POIDataDict[pid] = (pid,time,PATS,timescore,socialINF,category)
                else:
                    continue

            scoreD[c] = score
            c += 1
            reconstructionInput.append(tuple(localInput))
        sorted_scoreD = sorted(scoreD.items(), key=operator.itemgetter(1),reverse=True)
        limit = p * len(sorted_scoreD)

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
                score += (x[2]+x[3]+x[4])
            orignalRouteScore[tuple(t)] = score
          
        reconstructionInput_p = Set(reconstructionInput_p)
        prefixSet = Set()

        for i in splitDict:
            tempStack = []
            construct_c = 0
            construct(splitDict[i]) 

        reconstructionTime = timer.time() - reconstruction_start
        avgReconstructTime += reconstructionTime
        avgOri += len(reconstructionInput)
        avgLength += len(reconstructionOutput)

        reconstructionOutPutList = [(i,reconstructionOutput[i]) for i in reconstructionOutput]
        
      
        routeList = []
        totalroute_start_time = timer.time()
        qCoverTime = 0.0
        ScoringTime = 0.0
        ProcessTime = 0.0
        
        pool_size = 8  # your "parallelness"
        pool = Pool(pool_size)
        result_r_start = timer.time()
        # print 'start result_r'
        if len(reconstructionOutPutList) > 0 :
            result_r = pool.map(cal_re,reconstructionOutPutList)
        else:
            result_r = []
        result_r_time = timer.time() - result_r_start
        pool.close()
        pool.join()


        pool = Pool(pool_size)
        result_start = timer.time()
        # print 'start result' 
        result = pool.map(cal,qByRegion_rows)
        result_time = timer.time() - result_start
        # print 'result_r: ',str(len(result_r)),'  result: ',str(len(result))
        # result += result_r
        result_r += result
        # result = pool.map_async(cal,qByRegion_rows)
        # need to add reconstruct result
        result = [d for d in result_r if d is not None]    
        pool.close()
        pool.join()
        
        skylineInputDict = {}
        skylineInputValue = []
        skylineInputDict_avg = {}
        skylineInputValue_avg = []
        idxCount = 0
        for t in result:
            # qCoverTime += t[10]
            rid = t[2]
            ScoringTime += t[10]
            ProcessTime += t[11]
            # skylineT = (t[12],t[13],t[14])
            skylineT_avg = (t[15],t[16],t[17],t[21])
            # skylineInputDict[(rid,skylineT)] = idxCount
            skylineInputDict_avg[(rid,skylineT_avg)] = idxCount
            # skylineInputValue.append((rid,skylineT))
            skylineInputValue_avg.append((rid,skylineT_avg))
            idxCount += 1

        

        
        #skyline multi
        
        pool_skyline = Pool(8) 
        skyline_start_avg = timer.time()
        r = pool_skyline.map(cal_dominate,itertools.izip(skylineInputValue_avg, itertools.repeat(skylineInputValue_avg)))
        skyline_avg = timer.time()-skyline_start_avg
        r = [i for i in r if i is not None]
        resultData_avg = [result[skylineInputDict_avg[i]] for i in r]
        pool_skyline.close()
        pool_skyline.join()


        skyline_avg = timer.time()-skyline_start_avg



        #sorting by all score
        sorted_by_allScore = sorted(result, reverse=True, key=lambda tup: tup[3])[:len(resultData_avg)]
        #sorting by avg score
        sorted_by_avgScore = sorted(result, reverse=True, key=lambda tup: tup[4])[:len(resultData_avg)] 
        #sorting by PATS
        sorted_by_PATS = sorted(result, reverse=True, key=lambda tup: tup[12])[:len(resultData_avg)] 
        #sorting by timescore
        sorted_by_timescore = sorted(result, reverse=True, key=lambda tup: tup[13])[:len(resultData_avg)]
        #sorting by socialINF 
        sorted_by_socialINF = sorted(result, reverse=True, key=lambda tup: tup[14])[:len(resultData_avg)]
        #sorting by KM 
        sorted_by_KM = sorted(result, reverse=True, key=lambda tup: tup[21])[:len(resultData_avg)]









         
        totalTime = timer.time() - start_time

        #tup = uid,orignal_rid, select_rid, rScore, avg_rScore, categoryHit, cover, poi_hitCount, poiHit, socialFlag, ScoringTime, ProcessTime, Total_PATS, Total_Timescore, Total_SocialINF,float(Total_PATS)/POICount, float(Total_Timescore)/POICount, float(Total_SocialINF)/POICount,editdistance,reconstructionFlag


        with open('/home/moonorblue/exp/V8/fb/allScore/expV8_'+str(p)+'.csv', 'a') as w:
            for d in sorted_by_allScore:
                w.write(str(d[0]) + ',' + str(d[1]) + ',' + str(d[2]) +
                        ','  + str(d[5]) +','+str(d[6])+','+str(d[7])+','+str(d[8])+','+str(d[9])+','+str(d[18])+','+str(d[20])+ '\n')
                #uid,orignal_rid, select_rid,categoryHit, cover, poi_hitCount, poiHit, if have socialINF score, editdistance, consine similarity
            w.close()

        with open('/home/moonorblue/exp/V8/fb/avgScore/expV8_'+str(p)+'.csv', 'a') as w:
            for d in sorted_by_avgScore:
                w.write(str(d[0]) + ',' + str(d[1]) + ',' + str(d[2]) +
                        ','  + str(d[5]) +','+str(d[6])+','+str(d[7])+','+str(d[8])+','+str(d[9])+','+str(d[18])+','+str(d[20])+ '\n')
                #uid,orignal_rid, select_rid,categoryHit, cover ratio, poi_hitCount, poiHit, if have socialINF score, editdistance, consine similarity
            w.close()
             
        
        with open('/home/moonorblue/exp/V8/fb/PATS/expV8_'+str(p)+'.csv', 'a') as w:
            for d in sorted_by_PATS:
                w.write(str(d[0]) + ',' + str(d[1]) + ',' + str(d[2]) +
                        ','  + str(d[5]) +','+str(d[6])+','+str(d[7])+','+str(d[8])+','+str(d[9])+','+str(d[18])+','+str(d[20])+ '\n')
                #uid,orignal_rid, select_rid,categoryHit, cover ratio, poi_hitCount, poiHit, if have socialINF score, editdistance, consine similarity
            w.close()

        with open('/home/moonorblue/exp/V8/fb/timescore/expV8_'+str(p)+'.csv', 'a') as w:
            for d in sorted_by_timescore:
                w.write(str(d[0]) + ',' + str(d[1]) + ',' + str(d[2]) +
                        ','  + str(d[5]) +','+str(d[6])+','+str(d[7])+','+str(d[8])+','+str(d[9])+','+str(d[18])+','+str(d[20])+ '\n')
                #uid,orignal_rid, select_rid,categoryHit, cover ratio, poi_hitCount, poiHit, if have socialINF score, editdistance, consine similarity
            w.close()

        with open('/home/moonorblue/exp/V8/fb/socialInf/expV8_'+str(p)+'.csv', 'a') as w:
            for d in sorted_by_socialINF:
                w.write(str(d[0]) + ',' + str(d[1]) + ',' + str(d[2]) +
                        ','  + str(d[5]) +','+str(d[6])+','+str(d[7])+','+str(d[8])+','+str(d[9])+','+str(d[18])+','+str(d[20])+ '\n')
                #uid,orignal_rid, select_rid,categoryHit, cover ratio, poi_hitCount, poiHit, if have socialINF score, editdistance, consine similarity
            w.close() 

        with open('/home/moonorblue/exp/V8/fb/skyline/expV8_'+str(p)+'.csv', 'a') as w:
            for d in resultData_avg:
                w.write(str(d[0]) + ',' + str(d[1]) + ',' + str(d[2]) +
                        ',' + str(d[5]) +','+str(d[6])+','+str(d[7])+','+str(d[8])+','+str(d[9])+','+str(d[18])+','+str(d[20])+ '\n')
                #uid,orignal_rid, select_rid,categoryHit, cover ratio, poi_hitCount, poiHit, if have socialINF score, editdistance, consine similarity
            w.close()
        with open('/home/moonorblue/exp/V8/fb/KM/expV8_'+str(p)+'.csv', 'a') as w:
            for d in sorted_by_KM:
                w.write(str(d[0]) + ',' + str(d[1]) + ',' + str(d[2]) +
                        ',' + str(d[5]) +','+str(d[6])+','+str(d[7])+','+str(d[8])+','+str(d[9])+','+str(d[18])+','+str(d[20])+'\n')
                #uid,orignal_rid, select_rid,categoryHit, cover ratio, poi_hitCount, poiHit, if have socialINF score, editdistance, consine similarity 
            w.close()
        #time
        with open('/home/moonorblue/exp/V8/fb/expV8_time_'+str(p)+'.csv', 'a') as y:
            y.write(str(orignal_rid)+','+str(len(qByRegion_rows))+','+str(totalTime)+','+str(skyline_avg)+','+str(reconstructionTime)+','+str(result_r_time)+','+str(result_time)+','+str(len(result_r))+'\n')
            #original rid, covered routes, total process time, skyline with average score time, route reconstruction time, reconstructed routes scoring time, original routes scoring time
            y.close()
     

        if progressCount in StopNumbers:
            shutil.copyfile('/home/moonorblue/exp/V8/fb/allScore/expV8_'+str(p)+'.csv', '/home/moonorblue/exp/V8/fb/allScore/expV8_'+str(progressCount)+'_'+str(p)+'.csv')
            shutil.copyfile('/home/moonorblue/exp/V8/fb/avgScore/expV8_'+str(p)+'.csv', '/home/moonorblue/exp/V8/fb/avgScore/expV8_'+str(progressCount)+'_'+str(p)+'.csv')
            shutil.copyfile('/home/moonorblue/exp/V8/fb/PATS/expV8_'+str(p)+'.csv', '/home/moonorblue/exp/V8/fb/PATS/expV8_'+str(progressCount)+'_'+str(p)+'.csv')
            shutil.copyfile('/home/moonorblue/exp/V8/fb/timescore/expV8_'+str(p)+'.csv', '/home/moonorblue/exp/V8/fb/timescore/expV8_'+str(progressCount)+'_'+str(p)+'.csv')
            shutil.copyfile('/home/moonorblue/exp/V8/fb/socialInf/expV8_'+str(p)+'.csv', '/home/moonorblue/exp/V8/fb/socialInf/expV8_'+str(progressCount)+'_'+str(p)+'.csv')
            shutil.copyfile('/home/moonorblue/exp/V8/fb/skyline/expV8_'+str(p)+'.csv', '/home/moonorblue/exp/V8/fb/skyline/expV8_'+str(progressCount)+'_'+str(p)+'.csv')
            shutil.copyfile('/home/moonorblue/exp/V8/fb/KM/expV8_'+str(p)+'.csv', '/home/moonorblue/exp/V8/fb/KM/expV8_'+str(progressCount)+'_'+str(p)+'.csv')
            shutil.copyfile('/home/moonorblue/exp/V8/fb/expV8_time_'+str(p)+'.csv', '/home/moonorblue/exp/V8/fb/expV8_time_'+str(progressCount)+'_'+str(p)+'.csv')



        progressCount += 1

print 'Finish!'




