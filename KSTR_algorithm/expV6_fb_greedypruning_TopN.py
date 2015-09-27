import pg
import itertools
from os import listdir
import json
from sets import Set
import time as timer
# from multiprocessing.pool import ThreadPool as Pool
from multiprocessing import Pool
import sys
import operator
from random import shuffle
import shutil
import datetime

def cal_re_in(select_rid,tuples):

    Total_PATS = 0.0
    Total_Timescore = 0.0
    Total_SocialINF = 0.0
    for t in tuples:
        Total_PATS += t[2]
        Total_Timescore += t[3]
        Total_SocialINF += t[4]
        

    POIs = row[1]
    rScore = 0.0
    recommendCategory = Set([])
    
    # socialFlag = False

    rScore  = Total_PATS + Total_Timescore + Total_SocialINF
    POICount = len(tuples)
    cover = 0.0

    avg_rScore = float(rScore) / POICount

    reconstructionFlag = True
    tup = uid,orignal_rid,select_rid, rScore, avg_rScore, 0, 0, 0, 0, 0, 0, 0, Total_PATS, Total_Timescore, Total_SocialINF,float(Total_PATS)/POICount, float(Total_Timescore)/POICount, float(Total_SocialINF)/POICount,0,0
    return tup

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
        if head[0] == tail[0] or head[1] >= tail[1]:
            continue
        if head[0] not in splitDict:
            splitDict[head[0]] = Set([])
            splitDict[head[0]].add((head,tail))
        else:
            splitDict[head[0]].add((head,tail))


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


        headSet = splitDict.get(i[0][0],None)
        tailSet = splitDict.get(i[1][0],None)

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

                if tuple(x_p) not in reconstructionInput_p :
                    if tuple(x_p) in orignalRouteScore:
                        if score > orignalRouteScore[tuple(x_p)]:
                            r_rid = 'Reconstruct_'+str(reconstructionIdx)
                            reconstructionOutput.append(cal_re_in(r_rid,tempStack))
                            # reconstructionOutput['Reconstruct_'+str(reconstructionIdx)] = tempStack_cpy
                            reconstructionIdx += 1
                            reconstructionInput_p.add(tuple(x_p))
                    else:
                        r_rid = 'Reconstruct_'+str(reconstructionIdx)
                        reconstructionOutput.append(cal_re_in(r_rid,tempStack))
                        # reconstructionOutput['Reconstruct_'+str(reconstructionIdx)] = tempStack_cpy
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
                if tuple(x_p) not in reconstructionInput_p :
                    if tuple(x_p) in orignalRouteScore:
                        if score > orignalRouteScore[tuple(x_p)]:
                            r_rid = 'Reconstruct_'+str(reconstructionIdx)
                            reconstructionOutput.append(cal_re_in(r_rid,tempStack))
                            # reconstructionOutput['Reconstruct_'+str(reconstructionIdx)] = tempStack_cpy
                            reconstructionIdx += 1
                            reconstructionInput_p.add(tuple(x_p))
                    else:
                        r_rid = 'Reconstruct_'+str(reconstructionIdx)
                        reconstructionOutput.append(cal_re_in(r_rid,tempStack))
                        # reconstructionOutput['Reconstruct_'+str(reconstructionIdx)] = tempStack_cpy
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
                if tuple(x_p) not in reconstructionInput_p :
                    if tuple(x_p) in orignalRouteScore:
                        if score > orignalRouteScore[tuple(x_p)]:
                            r_rid = 'Reconstruct_'+str(reconstructionIdx)
                            reconstructionOutput.append(cal_re_in(r_rid,tempStack))
                            # reconstructionOutput['Reconstruct_'+str(reconstructionIdx)] = tempStack_cpy
                            reconstructionIdx += 1
                            reconstructionInput_p.add(tuple(x_p))
                    else:
                        r_rid = 'Reconstruct_'+str(reconstructionIdx)
                        reconstructionOutput.append(cal_re_in(r_rid,tempStack))
                        # reconstructionOutput['Reconstruct_'+str(reconstructionIdx)] = tempStack_cpy
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
                        if tuple(x_p) not in reconstructionInput_p :
                            if tuple(x_p) in orignalRouteScore:
                                if score > orignalRouteScore[tuple(x_p)]:
                                    r_rid = 'Reconstruct_'+str(reconstructionIdx)
                                    reconstructionOutput.append(cal_re_in(r_rid,tempStack))
                                    # reconstructionOutput['Reconstruct_'+str(reconstructionIdx)] = tempStack_cpy
                                    reconstructionIdx += 1
                                    reconstructionInput_p.add(tuple(x_p))
                            else:
                                r_rid = 'Reconstruct_'+str(reconstructionIdx)
                                reconstructionOutput.append(cal_re_in(r_rid,tempStack))
                                # reconstructionOutput['Reconstruct_'+str(reconstructionIdx)] = tempStack_cpy
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

    
def cal_re(row):
    tuples = row[1]
    select_rid = row[0]
    
    Total_PATS = 0.0
    Total_Timescore = 0.0
    Total_SocialINF = 0.0
    for t in tuples:
        Total_PATS += t[2]
        Total_Timescore += t[3]
        Total_SocialINF += t[4]
        

    POIs = row[1]
    rScore = 0.0
    recommendCategory = Set([])
    
    socialFlag = False

    rScore  = Total_PATS + Total_Timescore + Total_SocialINF
    POICount = len(tuples)
    cover = 0.0

    avg_rScore = float(rScore) / POICount

    reconstructionFlag = True

    tup = uid,orignal_rid, select_rid, rScore, avg_rScore, 0, 0, 0, 0, socialFlag, 0, 0, Total_PATS, Total_Timescore, Total_SocialINF,float(Total_PATS)/POICount, float(Total_Timescore)/POICount, float(Total_SocialINF)/POICount,0,reconstructionFlag
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
    for POI in POIs:
        pid = POI['pid']
        PATS = POI['PATS']
        timescore = POI['timeScore']
        time = POI['time']
        socialINF = 0.0
        recommendPOI.add((pid,float(time)))
        
        category = POIDict[pid]['category']
        

        latitude = POIDict[pid]['latitude']
        longitude = POIDict[pid]['longitude']
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
    
    avg_rScore = float(rScore) / POICount
    # POI hitness
    poi_hitCount = 0
    # for p in recommendPOI:
    #     if p in orignalPOI:
    #         poi_hitCount += 1
    poiHit = float(poi_hitCount) / 1 * 100
    # print recommendPOI,orignalPOI
    # category hitness (need edit for CA)

   
    editdistance = 0

    hitCount = 0
    categoryHit = float(hitCount) / 1 * 100
    ScoringTime = timer.time() - scoring_start_time
    ProcessTime = timer.time() - process_start_time

    reconstructionFlag = False
    tup = uid,orignal_rid, select_rid, rScore, avg_rScore, categoryHit, cover, poi_hitCount, poiHit, socialFlag, ScoringTime, ProcessTime, Total_PATS, Total_Timescore, Total_SocialINF,float(Total_PATS)/POICount, float(Total_Timescore)/POICount, float(Total_SocialINF)/POICount,editdistance,reconstructionFlag

    return tup
    
pro = [0.01,0.025,0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
conn_string = "host='192.168.100.200' dbname='moonorblue' user='moonorblue' password='4321'"
conn = pg.connect(conn_string)
query = "SELECT a.poi,a.region_minlong,a.region_minlat,a.region_maxlong,a.region_maxlat,a.uid,a.rid,a.geom FROM fb_route a,fb_checkincount b WHERE b.uid = a.uid AND st_area(a.geom) != 0 ORDER BY b.checkincount,a.rid ;"
# query = "SELECT a.poi,a.region_minlong,a.region_minlat,a.region_maxlong,a.region_maxlat,a.uid,a.rid,a.geom FROM ca_route a WHERE st_area(a.geom) != 0 LIMIT 1;"
rows = conn.query(query).getresult() 
FBsInfIdxDict = json.load(open('/home/moonorblue/socialINF/FB/idxDict'))
FBsInfMatrix = json.load(open('/home/moonorblue/socialINF/FB/matrixList'))
POIDict = json.load(open('/home/moonorblue/exp/materials/FB_POIDict'))
RelationDict = json.load(open('/home/moonorblue/exp/materials/FB_relationDict'))
for p in pro: 
   
    conn_string = "host='192.168.100.200' dbname='moonorblue' user='moonorblue' password='4321'"
    conn = pg.connect(conn_string)



    start_time = timer.time()
    
    avgReconstructTime = 0.0
    avgOri = 0.0
    avgLength = 0.0

    length = len(rows)
    progressCount = 1
    for row in rows:
        if progressCount > 1000:
            break

        qByRegion = "SELECT poi,rid,(st_area(st_intersection(geom,'" + str(row[7])+ "'))/st_area('"+str(row[7])+"'))*100 FROM fb_route WHERE geom && '"+str(row[7])+"' AND st_area(geom) != 0 AND st_area('"+str(row[7])+"') != 0 AND (st_area(st_intersection(geom, '"+str(row[7])+"'))/st_area('"+str(row[7])+"')) != 0"
        qByRegion_start_time = timer.time()
        qByRegion_rows = conn.query(qByRegion).getresult()
        
        if len(qByRegion_rows) > 10000:
            continue
        
        print 'fb ',str(p)+" Start # "+str(progressCount)+"/"+str(length)+"\n"
        start_time = timer.time()


        orignalCategory = Set([])
        orignalPOI = Set([])
        POIs = eval(row[0])
        for POI in POIs:
            pid = POI['pid']
            PATS = POI['PATS']
            timescore = POI['timeScore']
            time = POI['time']
            orignalPOI.add((pid,float(time)))
            ###########1
            category = POIDict[pid]['category']

        minlong = float(row[1])
        minlat = float(row[2])
        maxlong = float(row[3])
        maxlat = float(row[4])

        uid = row[5]
        orignal_rid = str(row[6])
        fids = RelationDict.get(uid,[])
        fids = Set(fids)


        reconstruction_start = timer.time()
        splitDict = {}

        reconstructionInput = []
        reconstructionOutput = []
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
                if latitude >= minlat and latitude <= maxlat and longitude >= minlong and longitude <= maxlong: 
                    PATS = POI['PATS']
                    timescore = POI['timeScore']
                    socialINF = 0.0
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

                    score += (PATS+timescore+socialINF)

                    localInput.append((pid,time,PATS,timescore,socialINF,category))

                    if pid not in POIScoreDict:
                        POIScoreDict[pid] = PATS + timescore + socialINF
                        POIDataDict[pid] = (pid,time,PATS,timescore,socialINF,category)
                    else:
                        if (PATS + timescore + socialINF) > POIScoreDict[pid]:
                            POIDataDict[pid] = (pid,time,PATS,timescore,socialINF,category)
                else:
                    continue

            scoreD[c] = score
            c += 1
            reconstructionInput.append(tuple(localInput))

        sorted_scoreD = sorted(scoreD.items(), key=operator.itemgetter(1),reverse=True)
        # print sorted_scoreD
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

        for i in splitDict:
            tempStack = []
            construct_c = 0
            # if i == '65293':
            # if i == '41714':
            # if i == '17006':
            construct(splitDict[i])


        reconstructionTime = timer.time() - reconstruction_start
        avgReconstructTime += reconstructionTime

  
        routeList = []
        totalroute_start_time = timer.time()
        qCoverTime = 0.0
        ScoringTime = 0.0
        ProcessTime = 0.0
        
        pool_size = 8  # your "parallelness"



        pool = Pool(pool_size)
        result_start = timer.time()
        result = pool.map(cal,qByRegion_rows)
        result_time = timer.time() - result_start
        result += reconstructionOutput
        # result += result_r
        result = [d for d in result if d is not None]  
        pool.close()
        pool.join()
        
        skylineInputDict = {}
        skylineInputValue = []
        skylineInputDict_avg = {}
        skylineInputValue_avg = []
        idxCount = 0
        for t in result:
            rid = t[2]
            ScoringTime += t[10]
            ProcessTime += t[11]
            skylineT = (t[12],t[13],t[14])
            skylineT_avg = (t[15],t[16],t[17])
            skylineInputDict[(rid,skylineT)] = idxCount
            skylineInputDict_avg[(rid,skylineT_avg)] = idxCount
            skylineInputValue.append((rid,skylineT))
            skylineInputValue_avg.append((rid,skylineT_avg))
            idxCount += 1



        #skyline sequential
        r = []
        skyline_start = timer.time()
        for i in skylineInputValue:
            all_dominate = True
            for j in skylineInputValue:
                if if_dominate(i[1],j[1]) == False:
                    all_dominate = False
                    break
            if all_dominate:
                r.append(i)

        resultData = [result[skylineInputDict[i]] for i in r]
        skyline_total = timer.time()-skyline_start 

        r = []
        skyline_start_avg = timer.time()
        for i in skylineInputValue_avg:
            all_dominate = True
            for j in skylineInputValue_avg:
                if if_dominate(i[1],j[1]) == False:
                    all_dominate = False
                    break
            if all_dominate:
                r.append(i) 

        resultData_avg = [result[skylineInputDict_avg[i]] for i in r]



        skyline_avg = timer.time()-skyline_start_avg
        totalTime = timer.time() - start_time

         
        with open('/home/moonorblue/exp/topk_6/fb/expV6_fb_parallel_skyline_total_user_checkincount_'+str(p)+'.csv', 'a') as w:
            for d in resultData:
                w.write(str(d[0]) + ',' + str(d[1]) + ',' + str(d[2]) +
                        ',' + str(d[3]) + ',' + str(d[4]) + ',' + str(d[5]) +','+str(d[6])+','+str(d[7])+','+str(d[8])+','+str(d[9])+','+str(d[18])+','+str(d[12])+','+str(d[13])+','+str(d[14])+ '\n')
                #uid,original_rid, select_rid, total route Score, avg route score, category hit rate, cover ratio, poi hitCount, poi hit rate,if have socialINF score, editdistance,Total PATS score , Total Timescore, Total SocialINF score
            
            w.close()
        with open('/home/moonorblue/exp/topk_6/fb/expV6_fb_parallel_skyline_avg_user_checkincount_'+str(p)+'.csv', 'a') as w:
            for d in resultData_avg:
                w.write(str(d[0]) + ',' + str(d[1]) + ',' + str(d[2]) +
                        ',' + str(d[3]) + ',' + str(d[4]) + ',' + str(d[5]) +','+str(d[6])+','+str(d[7])+','+str(d[8])+','+str(d[9])+','+str(d[18])+','+str(d[15])+','+str(d[16])+','+str(d[17])+ '\n')
                #uid,original_rid, select_rid, rtotal route Score, avg route score, category hit rate, cover ratio, poi hitCount, poi hit rate,if have socialINF score, editdistance,Average PATS score, Average Timescore, Average SocialINF score
            
            w.close()
        with open('/home/moonorblue/exp/topk_6/fb/expV6_fb_parallel_skyline_user_checkincount_time_'+str(p)+'.csv', 'a') as y:
            y.write(str(orignal_rid)+','+str(len(qByRegion_rows))+','+str(totalTime)+','+str(skyline_total)+','+str(skyline_avg)+','+str(reconstructionTime)+','+str(len(reconstructionOutput))+','+str(result_time)+'\n')
            #original rid, covered routes, total process time, skyline with total score time, skyline with average score time, route reconstruction time, reconstructed routes counts, routes scoring time
            y.close()


        progressCount += 1

print 'Finish!'




