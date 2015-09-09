import psycopg2
import itertools
from os import listdir
import json
from sets import Set


conn_string = "host='192.168.100.200' dbname='moonorblue' user='moonorblue' password='4321'"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()


def insertRoute_FB(tuples,cur):
    args_str = ','.join(cur.mogrify("(%s,%s,%s,%s,%s,%s,%s)", t) for t in tuples)
    cur.execute(
        "INSERT INTO fb_route (rid,poi,region_minlat,region_minlong,region_maxlat,region_maxlong,uid) VALUES" + args_str)

# def insertPOI_FB(tuples,cur):
#     args_str = ','.join(cur.mogrify("(%s,%s,%s,%s,%s)", t) for t in tuples)
#     cur.execute(
#         "INSERT INTO fb_poi (pid,category,lat,long,visiters) VALUES" + args_str)


# def insertRoute_CA(tuples,cur):
#     args_str = ','.join(cur.mogrify("(%s,%s,%s,%s,%s,%s,%s)", t) for t in tuples)
#     cur.execute(
#         "INSERT INTO ca_route (rid,poi,region_minlat,region_minlong,region_maxlat,region_maxlong,uid) VALUES" + args_str)


# def insertPOI_CA(tuples,cur):
#     args_str = ','.join(cur.mogrify("(%s,%s,%s,%s,%s)", t) for t in tuples)
#     cur.execute(
#         "INSERT INTO ca_poi (pid,category,lat,long,visiters) VALUES" + args_str)

# def insertRelation_CA(tuples,cur):
#     args_str = ','.join(cur.mogrify("(%s,%s)", t) for t in tuples)
#     cur.execute(
#         "INSERT INTO ca_relation (uid,fids) VALUES" + args_str)

# def insertRelation_FB(tuples,cur):
#     args_str = ','.join(cur.mogrify("(%s,%s)", t) for t in tuples)
#     cur.execute(
#         "INSERT INTO fb_relation (uid,fids) VALUES" + args_str)

def getMinAndMax(lats, longs):
    return min(lats), min(longs), max(lats), max(longs)


CAPath = '/home/moonorblue/routes/CA/WithScore/'
FBPath = '/home/moonorblue/routes/FB/WithScore/'
CAsInfLocDict = json.load(open('/home/moonorblue/socialINF/CA/locDict'))
CAsInfIdxDict = json.load(open('/home/moonorblue/socialINF/CA/idxDict'))
FBsInfLocDict = json.load(open('/home/moonorblue/socialINF/FB/locDict'))
FBsInfIdxDict = json.load(open('/home/moonorblue/socialINF/FB/idxDict'))
CAsInfMatrix = json.load(open('/home/moonorblue/socialINF/CA/matrixList'))
FBsInfMatrix = json.load(open('/home/moonorblue/socialINF/FB/matrixList'))


rev_CAsInfIdxDict = {CAsInfIdxDict[k]: k for k in CAsInfIdxDict}
rev_FBsInfIdxDict = {FBsInfIdxDict[k]: k for k in FBsInfIdxDict}

length = len(CAsInfMatrix)

# w = open('/home/moonorblue/exp/materials/CA_relationDict','w')

# scoreDict = {}
# for i in xrange(length):
#     uid = rev_CAsInfIdxDict[i]
#     fids = []
#     for j in xrange(length):
#         fid = rev_CAsInfIdxDict[j]
#         score = CAsInfMatrix[i][j]
#         if score > 0.0:
#             fids.append(fid)
#     scoreDict[uid] = fids
# w.write(json.dumps(scoreDict))
# w.close()
# # print 'insertRelation_CA'
# # insertRelation_CA(scoreTuples,cursor)
# # print 'conn.commit()'
# # conn.commit()

# length = len(FBsInfMatrix)

# w = open('/home/moonorblue/exp/materials/FB_relationDict','w')

# scoreDict = {}
# for i in xrange(length):
#     uid = rev_FBsInfIdxDict[i]
#     fids = []
#     for j in xrange(length):
#         fid = rev_FBsInfIdxDict[j]
#         score = FBsInfMatrix[i][j]
#         if score > 0.0:
#             fids.append(fid)
#     # sT = str(uid),json.dumps(fids)
#     scoreDict[uid] = fids
# w.write(json.dumps(scoreDict))
# w.close()
# # print 'insertRelation_FB'
# # insertRelation_FB(scoreTuples,cursor)
# # print 'conn.commit()'
# poiSet = Set([])
# w = open('/home/moonorblue/exp/materials/CA_POIDict','w')
# idcount = 0
# routeTuples = []
# poiDict = {}
# for user in listdir(CAPath):
#     # print user
#     f = open(CAPath + user)
#     j = json.load(f)
#     routes = j['route']
#     for r in routes:
#         n = []
#         rid = idcount
#         longs = []
#         lats = []
#         for rr in r:
#             # routes
#             pid = rr['pid']
#             PATS = rr['PATS']
#             time = rr['time']
#             timeScore = rr['timeScore']
            
#             try:
#                 longs.append(float(rr['longitude']))
#                 lats.append(float(rr['latitude']))
#             except:
#                 print 'coordinate error, continue'
#                 continue


#             # poi
#             if pid not in poiDict:
#                 visiters = []
#                 longitude = rr['longitude']
#                 latitude = rr['latitude']
#                 category = rr['category']
#                 if pid in CAsInfLocDict:
#                     visiterList = CAsInfLocDict[pid]
#                     for v in visiterList:
#                         visiters.append(v)
#             # insert poi tuple
#                 poiDict[pid] = {'category':str(category),'latitude':float(latitude),'longitude':float(longitude),'visiters':visiters}
#                 # poiT = int(pid), str(category), float(latitude), float(longitude), json.dumps(
#                     # visiters),user.split('.json')[0]
#                 # poiTuples.append(poiT)
#                 # print poiT
# w.write(json.dumps(poiDict))
# w.close()


# w = open('/home/moonorblue/exp/materials/FB_POIDict','w')
placeDataPath = '/home/moonorblue/placeData_new/'
idcount = 0
routeTuples = []
poiDict = {}
for user in listdir(FBPath):
    # print user
    f = open(FBPath + user)
    j = json.load(f)
    routes = j['route']
    for r in routes:
        n = []
        rid = idcount
        longs = []
        lats = []
        existPid = Set([])
        for rr in r:
            # routes
            pid = rr['pid']
            PATS = rr['PATS']
            time = rr['time']
            timeScore = rr['timeScore']
            category = rr['category']
            # pidJ = json.load(open(placeDataPath+pid))
            # name = pidJ['name'].encode('utf-8')
            
            try:
                longs.append(float(rr['longitude']))
                lats.append(float(rr['latitude']))
            except:
                print 'coordinate error, continue'
                continue
            pidJ = json.load(open(placeDataPath+pid))
            name = pidJ['name'].encode('utf-8')
            try:
                link = pidJ['link']
            except:
                link = ''
            try:
                likes = pidJ['likes']
            except:
                likes = '0'
            try:
                checkins = pidJ['checkins']
            except:
                checkins = '0'

            # poi
            # if pid not in poiDict:
            #     visiters = []
            #     longitude = rr['longitude']
            #     latitude = rr['latitude']
            #     category = rr['category']
            #     if pid in FBsInfLocDict:
            #         visiterList = FBsInfLocDict[pid]
            #         for v in visiterList:
            #             visiters.append(v)
            # insert poi tuple
                # poiDict[pid] = {'category':str(category),'latitude':float(latitude),'longitude':float(longitude),'visiters':visiters}
                # poiT = int(pid), str(category), float(latitude), float(longitude), json.dumps(
                    # visiters),user.split('.json')[0]
                # poiTuples.append(poiT)
                # print poiT
# w.write(json.dumps(poiDict))
# w.close()
            if pid not in existPid:
                existPid.add(pid)
                nd = {}
                nd['pid'] = pid
                nd['PATS'] = PATS
                nd['time'] = time
                nd['timeScore'] = timeScore
                nd['category'] = category
                nd['name'] = name
                nd['link'] = link
                nd['likes'] = likes
                nd['checkins'] = checkins
                n.append(nd)

        # insert route tuples
        if len(lats) != 0 and len(longs) != 0 and len(n) > 1:
            minlat, minlong, maxlat, maxlong = getMinAndMax(lats,longs)
            idcount += 1
            routeT = rid, json.dumps(n), minlat, minlong, maxlat, maxlong, user.split('.json')[0]
            routeTuples.append(routeT)
        # print routeT

# insert
# print 'insertPOI_CA'
# insertPOI_CA(poiTuples,cursor)
# print 'insertRoute_CA'
# insertRoute_CA(routeTuples,cursor)

# conn.commit()

# poiSet = Set([])

# idcount = 0
# routeTuples = []
# poiTuples = []
# for user in listdir(FBPath):
#     # print user
#     f = open(FBPath + user)
#     j = json.load(f)
#     routes = j['route']
#     for r in routes:
#         n = []
#         rid = idcount
#         longs = []
#         lats = []
#         for rr in r:
#             # routes
#             pid = rr['pid']
#             PATS = rr['PATS']
#             time = rr['time']
#             timeScore = rr['timeScore'] 
#             # print rr['longitude'],rr['latitude']

#             try:
#                 longs.append(float(rr['longitude']))
#                 lats.append(float(rr['latitude']))
#                 # print float(rr['longitude']),float(rr['latitude'])
#             except:
#                 # print 'coordinate error, continue'
#                 continue

#             longs.append(float(rr['longitude']))
#             lats.append(float(rr['latitude']))

#             # poi
#             if pid not in poiSet:
#                 # print rr
#                 poiSet.add(pid)
#                 visiters = []
#                 longitude = rr['longitude']
#                 latitude = rr['latitude']
#                 category = rr['category']
#                 # print longitude,latitude
#                 if pid in FBsInfLocDict:
#                     visiterList = FBsInfLocDict[pid]
#                     for v in visiterList:
#                         visiters.append(v)
#             # insert poi tuple
#                 poiT = int(pid), str(category), float(latitude), float(longitude), json.dumps(
#                     visiters)
#                 poiTuples.append(poiT)
#                 # print poiT

#             nd = {}
#             nd['pid'] = pid
#             nd['PATS'] = PATS
#             nd['time'] = time
#             nd['timeScore'] = timeScore
#             n.append(nd)

#         # insert route tuples
#         if len(lats) != 0 and len(longs) != 0:
#             minlat, minlong, maxlat, maxlong = getMinAndMax(lats,longs)
#             idcount += 1
#             routeT = rid, json.dumps(n), minlat, minlong, maxlat, maxlong, user.split('.json')[0]
#             routeTuples.append(routeT)
#         # print routeT

# # insert
# print 'insertPOI_FB'
# insertPOI_FB(poiTuples,cursor)
print 'insertRoute_FB'
insertRoute_FB(routeTuples,cursor)

conn.commit()
cursor.close()
# conn.close()