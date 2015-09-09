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


def getMinAndMax(lats, longs):
    return str(min(lats)), str(min(longs)), str(max(lats)), str(max(longs))


def splitIntoHeadDict(route):
    length = len(route)
    for i in xrange(length):
        if i == length -1:
            break
        head = route[i]
        tail = route[i+1]
        if head[0] == tail[0]:
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
    # construct_c += 1
    # if construct_c == 1:
        # endflag =True
    # construct_c += 1
    # print tempStack
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
                 endflag = True
        
        headSet = splitDict.get(i[0][0],None)
        tailSet = splitDict.get(i[1][0],None)
        if tailSet != None and endflag == False:
            tempStack.pop()
            construct(tailSet)
            tempStack.pop()
        elif endflag == True:
            x_p = [i[0] for i in tempStack]
            tempStack_cpy = [i for i in tempStack]
            # global reconstructionIdx
            if tuple(x_p) not in reconstructionInput_p :
                reconstructionOutput['Reconstruct_'+str(reconstructionIdx)] = tempStack_cpy
                reconstructionIdx += 1
                # reconstructionOutputSet.add(tuple(tempStack))
            # if len(tempStack) <= 2 or tuple(tempStack) in reconstructionOutputSet:
            #     pass
            # else:
            #     reconstructionOutputSet.add(tuple(tempStack))
            # print 'end#',tempStack
            # for i in xrange(len(tempStack)):
            # tempStack.pop()
        else:
            x_p = [i[0] for i in tempStack]
            tempStack_cpy = [i for i in tempStack]
            # global reconstructionIdx
            if tuple(x_p) not in reconstructionInput_p :
                # print tempStack
                reconstructionOutput[''+str(reconstructionIdx)] = tempStack_cpy
                reconstructionIdx += 1
                reconstructionOutputSet.add(tuple(tempStack))
            for i in xrange(2):
                tempStack.pop()


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
    longs = []
    lats = []
    for POI in POIs:
        pid = POI[0]
        PATS = POI[2]
        timescore = POI[3]
        time = POI[1]
        socialINF = 0.0
        recommendPOI.add((pid,float(time)))

        # category = POIDict[pid]['category']
        # for cate in category.split(','):
        #     recommendCategory.add(cate)

        # latitude = POIDict[pid]['latitude']
        # longitude = POIDict[pid]['longitude']
        # lats.append(latitude)
        # longs.append(longitude)

        
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
    # conn_string = "host='192.168.100.200' dbname='moonorblue' user='moonorblue' password='4321'"
    # conn = pg.connect(conn_string)

    # minlat, minlong, maxlat, maxlong = getMinAndMax(lats,longs)    
    # print minlong,minlat,maxlong,maxlat
    # print orignal_rid

    # qCover = "SELECT (st_area(st_intersection(st_makeenvelope("+minlong+","+minlat+","+maxlong+","+maxlat+",4326), b.geom))/st_area(b.geom))*100 FROM ca_route b WHERE b.rid = '" + \
    #         str(orignal_rid) + "' AND st_area(st_makeenvelope("+minlong+","+minlat+","+maxlong+","+maxlat+",4326)) != 0 AND st_area(b.geom) != 0;"
    # qCover = "SELECT st_area(st_makeenvelope("+minlong+","+minlat+","+maxlong+","+maxlat+",4326));"
    # curr.execute(qCover)
    # qCover_row = conn.query(qCover).getresult() 

    cover = 0.0
    # for row_c in qCover_row:
    #     cover = row_c[0]
    #     # print row_c[1]
    # # print cover
    # if cover == 0.0:
    #     return

    # conn.close()

    avg_rScore = float(rScore) / POICount
    # POI hitness
    poi_hitCount = 0
    # for p in recommendPOI:
    #     if p in orignalPOI:
    #         poi_hitCount += 1
    poiHit = 0
    # print recommendPOI,orignalPOI
    # category hitness (need edit for CA)

    #edit distance
    

    # sorted_recommendPOI = [i[0] for i in sorted(recommendPOI, reverse=False, key=lambda tup: tup[1])]
    # sorted_orignalPOI = [i[0] for i in sorted(orignalPOI, reverse=False, key=lambda tup: tup[1])]
    # editdistance = levenshtein(sorted_orignalPOI,sorted_recommendPOI)    
    editdistance = 0

    hitCount = 0
    # for cate_r in recommendCategory:
    #     if cate_r in orignalCategory:
    #         hitCount += 1
    categoryHit = 0
    ScoringTime = timer.time() - scoring_start_time
    ProcessTime = timer.time() - process_start_time

    reconstructionFlag = True
    tup = uid,orignal_rid, select_rid, rScore, avg_rScore, categoryHit, cover, poi_hitCount, poiHit, socialFlag, ScoringTime, ProcessTime, Total_PATS, Total_Timescore, Total_SocialINF,float(Total_PATS)/POICount, float(Total_Timescore)/POICount, float(Total_SocialINF)/POICount,editdistance,reconstructionFlag
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
        
        # category = POIDict[pid]['category']
        # for cate in category.split(','):
        #     recommendCategory.add(cate)

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
    poiHit = 0
    # print recommendPOI,orignalPOI
    # category hitness (need edit for CA)

    #edit distance
    

    # sorted_recommendPOI = [i[0] for i in sorted(recommendPOI, reverse=False, key=lambda tup: tup[1])]
    # sorted_orignalPOI = [i[0] for i in sorted(orignalPOI, reverse=False, key=lambda tup: tup[1])]
    # editdistance = levenshtein(sorted_orignalPOI,sorted_recommendPOI)    
    editdistance = 0

    hitCount = 0
    # for cate_r in recommendCategory:
    #     if cate_r in orignalCategory:
    #         hitCount += 1
    categoryHit = 0
    ScoringTime = timer.time() - scoring_start_time
    ProcessTime = timer.time() - process_start_time

    reconstructionFlag = False
    tup = uid,orignal_rid, select_rid, rScore, avg_rScore, categoryHit, cover, poi_hitCount, poiHit, socialFlag, ScoringTime, ProcessTime, Total_PATS, Total_Timescore, Total_SocialINF,float(Total_PATS)/POICount, float(Total_Timescore)/POICount, float(Total_SocialINF)/POICount,editdistance,reconstructionFlag

    return tup
    
pro = [0.9,1.0]

# pro = [0.025]
conn_string = "host='192.168.100.200' dbname='moonorblue' user='moonorblue' password='4321'"
conn = pg.connect(conn_string)
query = "SELECT a.poi,a.region_minlong,a.region_minlat,a.region_maxlong,a.region_maxlat,a.uid,a.rid,a.geom FROM fb_route a,fb_checkincount b WHERE b.uid = a.uid AND st_area(a.geom) != 0  ORDER BY b.checkincount,a.rid ;"
# query = "SELECT a.poi,a.region_minlong,a.region_minlat,a.region_maxlong,a.region_maxlat,a.uid,a.rid,a.geom FROM ca_route a WHERE st_area(a.geom) != 0 LIMIT 1;"
rows = conn.query(query).getresult() 

for p in pro: 
   
    conn_string = "host='192.168.100.200' dbname='moonorblue' user='moonorblue' password='4321'"
    conn = pg.connect(conn_string)

    log = open('/home/moonorblue/exp/topk/fb/expV6_fb_parallel_skyline_total_user_checkincount_log_'+str(p),'a')

    # select all route from top users
    # query = "SELECT a.poi,a.region_minlong,a.region_minlat,a.region_maxlong,a.region_maxlat,a.uid,a.rid,a.geom FROM ca_route a,ca_checkincount b WHERE b.uid = a.uid AND st_area(a.geom) != 0 ORDER BY b.checkincount LIMIT 10 ;"
    # query = "SELECT a.poi,a.region_minlong,a.region_minlat,a.region_maxlong,a.region_maxlat,a.uid,a.rid,a.geom FROM ca_route a WHERE st_area(a.geom) != 0 ;"
    # query = "SELECT a.poi,a.region_minlong,a.region_minlat,a.region_maxlong,a.region_maxlat,a.uid,a.rid,a.geom FROM fb_route a,fb_user b WHERE b.uid = a.uid AND st_area(a.geom) != 0 ORDER BY b.friendcount ;"
    # query = "SELECT a.poi,a.region_minlong,a.region_minlat,a.region_maxlong,a.region_maxlat,a.uid,a.rid,a.geom  FROM fb_route a WHERE a.rid = '74235' ;" 
    start_time = timer.time()
    # cur.execute(query)
    # rows = [r for r in cur]
    log.write(str(p)+'\n')
    log.write("Query all route"+": %s seconds " % str(timer.time() - start_time)+"\n"+"######################################\n")
    # print "Query all route"+": %s seconds " % str(timer.time() - start_time)+"\n"+"######################################\n"
    
    avgReconstructTime = 0.0
    avgOri = 0.0
    avgLength = 0.0

    FBsInfIdxDict = json.load(open('/home/moonorblue/socialINF/FB/idxDict'))
    FBsInfMatrix = json.load(open('/home/moonorblue/socialINF/FB/matrixList'))

    POIDict = json.load(open('/home/moonorblue/exp/materials/FB_POIDict'))
    RelationDict = json.load(open('/home/moonorblue/exp/materials/FB_relationDict'))
    length = len(rows)
    StopNumbers = Set([100,500,1000]) 
    progressCount = 1
    # avgReconstruct = 0.0
    for row in rows:
        if progressCount > 1000:
            break


        qByRegion = "SELECT poi,rid,(st_area(st_intersection(geom,'" + str(row[7])+ "'))/st_area('"+str(row[7])+"'))*100 FROM fb_route WHERE geom && '"+str(row[7])+"' AND st_area(geom) != 0 AND st_area('"+str(row[7])+"') != 0 AND (st_area(st_intersection(geom, '"+str(row[7])+"'))/st_area('"+str(row[7])+"')) != 0"
        qByRegion_start_time = timer.time()
        qByRegion_rows = conn.query(qByRegion).getresult()

        if len(qByRegion_rows) > 10000:
            continue

        log.write("Start # "+str(progressCount)+"/1000"+"\n")
        print 'fb ',str(p)+" Start # "+str(progressCount)+"/"+str(length)+"\n"
        start_time = timer.time()
        # poi information
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
            # category = POIDict[pid]['category']
            # for cate in category.split(','):
            #     orignalCategory.add(cate)
        minlong = float(row[1])
        minlat = float(row[2])
        maxlong = float(row[3])
        maxlat = float(row[4])

        # selecet intersect routes
        ################2
        # qByRegion = "SELECT poi,rid,(st_area(st_intersection(geom,'" + str(row[7])+ "'))/st_area('"+str(row[7])+"'))*100 FROM fb_route WHERE geom && '"+str(row[7])+"' AND st_area(geom) != 0 AND st_area('"+str(row[7])+"') != 0 AND (st_area(st_intersection(geom, '"+str(row[7])+"'))/st_area('"+str(row[7])+"')) != 0"
        # qByRegion_start_time = timer.time()
        # qByRegion_rows = conn.query(qByRegion).getresult()
       
        # reconstruction
        reconstruction_start = timer.time()
        # if len(qByRegion_rows) < 1000:
        splitDict = {}
        # reconstructionInput = Set([])
        reconstructionInput = []
        reconstructionOutput = {}
        reconstructionOutputSet = Set([])
        reconstructionIdx = 0


        scoreD = {}
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
                    time = float(POI['time'])
                    category = POIDict[pid]['category']
                    score += (PATS+timescore)
                    localInput.append((pid,time,PATS,timescore,category))
                else:
                    continue

            scoreD[c] = score
            c += 1
            # splitIntoHeadDict(tuple(localInput))
            # reconstructionInput.add(tuple(localInput))
            reconstructionInput.append(tuple(localInput))
        sorted_scoreD = sorted(scoreD.items(), key=operator.itemgetter(1),reverse=True)
        limit = p * len(sorted_scoreD)
        # print int(limit)
        chosedInput = []     
        reconstructionInput_p = []
        # print sorted_scoreD 
        for i in xrange(int(limit)):
            chosedInput.append(sorted_scoreD[i][0])
        # print chosedInput
        for i in chosedInput:
            # print i 
            splitIntoHeadDict(reconstructionInput[i])
            t = [x[0] for x in reconstructionInput[i]]
            reconstructionInput_p.append(tuple(t))
        # reconstructionInput_p = []
        # for i in reconstructionInput:
        # for i in ch
            # t = [x[0] for x in i]
            # reconstructionInput_p.append(tuple(t))
        reconstructionInput_p = Set(reconstructionInput_p)
        
        # print splitDict

        for i in splitDict:
            tempStack = []
            construct_c = 0
            construct(splitDict[i]) 

        reconstructionTime = timer.time() - reconstruction_start
        # print 'Reconstruction'+ ": %s seconds " % str(reconstructionTime)
        avgReconstructTime += reconstructionTime
        # print 'Original: ',len(reconstructionInput)
        avgOri += len(reconstructionInput)
        # print 'Length:',len(reconstructionOutput)
        avgLength += len(reconstructionOutput)
        # print 'PerRoute'+ ": %s seconds " % str(reconstructionTime/len(reconstructionOutput))
        # avgReconstruct += reconstructionTime/len(reconstructionOutput)
        # print reconstructionOutput
        reconstructionOutPutList = [(i,reconstructionOutput[i]) for i in reconstructionOutput]
        
        log.write('Total '+str(len(qByRegion_rows))+' covered routes \n')
        log.write("Query by region of rid #:"+str(row[6])+": %s seconds " % str(timer.time() - qByRegion_start_time)+"\n")
        log.write("Reconstruction time: %s seconds " % str(reconstructionTime)+'\n')
        # print 'Total '+str(len(qByRegion_rows))+' covered routes \n'
        # print "Query by region of rid #:"+str(row[6])+": %s seconds " % str(timer.time() - qByRegion_start_time)+"\n"
        uid = row[5]
        orignal_rid = str(row[6])
        ###get relation users
        
        fids = RelationDict.get(uid,[])
        fids = Set(fids)
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
        # shuffle(result)  
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
            skylineT = (t[12],t[13],t[14])
            skylineT_avg = (t[15],t[16],t[17])
            skylineInputDict[(rid,skylineT)] = idxCount
            skylineInputDict_avg[(rid,skylineT_avg)] = idxCount
            skylineInputValue.append((rid,skylineT))
            skylineInputValue_avg.append((rid,skylineT_avg))
            idxCount += 1

        

        
        #skyline multi
        # skyline_start = timer.time()
        # pool_skyline = Pool(8)
        # r = pool_skyline.map(cal_dominate,itertools.izip(skylineInputValue, itertools.repeat(skylineInputValue)))
        # skyline_total = timer.time()-skyline_start 
        # r = [i for i in r if i is not None]
        # resultData = [result[skylineInputDict[i]] for i in r]
        # pool_skyline.close()
        # pool_skyline.join()

        # skyline_start_avg = timer.time()
        # pool_skyline = Pool(8)
        # r = pool_skyline.map(cal_dominate,itertools.izip(skylineInputValue_avg, itertools.repeat(skylineInputValue_avg)))
        # skyline_avg = timer.time()-skyline_start_avg
        # r = [i for i in r if i is not None]
        # resultData_avg = [result[skylineInputDict_avg[i]] for i in r]
        # pool_skyline.close()
        # pool_skyline.join()

        #skyline sequential
        r = []
        skyline_start = timer.time()
        for i in skylineInputValue:
            # if len(r) >= 100:
                # break
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
            # if len(r) >= 100:
                # break
            all_dominate = True
            for j in skylineInputValue_avg:
                if if_dominate(i[1],j[1]) == False:
                    all_dominate = False
                    break
            if all_dominate:
                r.append(i) 

        resultData_avg = [result[skylineInputDict_avg[i]] for i in r]

        skyline_avg = timer.time()-skyline_start_avg
       
        log.write("Average scoring time: "+str(float(ScoringTime)/len(qByRegion_rows))+" seconds \n")
        log.write("Average process time: "+str(float(ProcessTime)/len(qByRegion_rows))+" seconds \n")
        log.write("Result time: "+str(result_time)+" seconds \n")
        log.write("Result_r time: "+str(result_r_time)+" seconds \n")
        log.write("Skyline_total time: "+str(skyline_total)+" seconds \n")
        log.write("Skyline_avg time: "+str(skyline_avg)+" seconds \n")

         
        totalTime = timer.time() - start_time

        with open('/home/moonorblue/exp/topk/fb/expV6_fb_parallel_skyline_total_user_checkincount_'+str(p)+'.csv', 'a') as w:
            for d in resultData:
                w.write(str(d[0]) + ',' + str(d[1]) + ',' + str(d[2]) +
                        ',' + str(d[3]) + ',' + str(d[4]) + ',' + str(d[5]) +','+str(d[6])+','+str(d[7])+','+str(d[8])+','+str(d[9])+','+str(d[18])+','+str(d[12])+','+str(d[13])+','+str(d[14])+ '\n')

            w.close()
        with open('/home/moonorblue/exp/topk/fb/expV6_fb_parallel_skyline_avg_user_checkincount_'+str(p)+'.csv', 'a') as w:
            for d in resultData_avg:
                w.write(str(d[0]) + ',' + str(d[1]) + ',' + str(d[2]) +
                        ',' + str(d[3]) + ',' + str(d[4]) + ',' + str(d[5]) +','+str(d[6])+','+str(d[7])+','+str(d[8])+','+str(d[9])+','+str(d[18])+','+str(d[15])+','+str(d[16])+','+str(d[17])+ '\n')

            w.close()
        with open('/home/moonorblue/exp/topk/fb/expV6_fb_parallel_skyline_user_checkincount_time_'+str(p)+'.csv', 'a') as y:
            y.write(str(orignal_rid)+','+str(len(qByRegion_rows))+','+str(totalTime)+','+str(skyline_total)+','+str(skyline_avg)+','+str(reconstructionTime)+','+str(result_r_time)+','+str(result_time)+'\n')
            y.close()
        # with open('/home/moonorblue/exp/topk/ca/expV6_ca_parallel_skyline_avg_user_checkincount_time_'+str(p)+'.csv', 'a') as y:
        #     y.write(str(orignal_rid)+','+str(len(qByRegion_rows))+','+str(totalTime)+','+str(skyline_avg)+'\n')
        #     y.close()
        if progressCount in StopNumbers:
            shutil.copyfile('/home/moonorblue/exp/topk/fb/expV6_fb_parallel_skyline_total_user_checkincount_'+str(p)+'.csv', '/home/moonorblue/exp/topk/fb/expV6_fb_parallel_skyline_total_user_checkincount_'+str(p)+'_'+str(progressCount)+'.csv')
            shutil.copyfile('/home/moonorblue/exp/topk/fb/expV6_fb_parallel_skyline_avg_user_checkincount_'+str(p)+'.csv', '/home/moonorblue/exp/topk/fb/expV6_fb_parallel_skyline_avg_user_checkincount_'+str(p)+'_'+str(progressCount)+'.csv')
            shutil.copyfile('/home/moonorblue/exp/topk/fb/expV6_fb_parallel_skyline_user_checkincount_time_'+str(p)+'.csv', '/home/moonorblue/exp/topk/fb/expV6_fb_parallel_skyline_user_checkincount_time_'+str(p)+'_'+str(progressCount)+'.csv')
        
        log.write("Total time of rid#:"+str(orignal_rid)+": %s seconds " % str(totalTime)+"\n")
        log.write("Finish # "+str(progressCount)+"/"+str(length)+" \nEstimated remaining time: "+str(totalTime*(length-progressCount))+" seconds  \n" +"######################################\n")
        log.write('\n\n')
        # print "Total time of rid#:"+str(orignal_rid)+": %s seconds " % str(timer.time() - start_time)+"\n"+"######################################\n"
        # print '#:',progressCount,'/',length,"--- %s seconds ---" % str(timer.time() - start_time)
        progressCount += 1

    # print 'final: ',str(avgReconstruct / 10) 
    # conn.close()
    # print p
    # print avgReconstructTime/10,float(avgOri)/10,float(avgLength)/10
print 'Finish!'




