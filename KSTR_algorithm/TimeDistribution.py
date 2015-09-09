import time
import datetime
import json
from os import listdir
import scipy.stats as stats
import numpy as np
import math


def getTimeListFromDict(data):
    f = open('/home/moonorblue/TimeDistribution/' + data + '/' + 'result')
    ListDict = {}
    j = json.load(f)
    for p in j:
        pid = p
        pDict = j[p]
        newList = []
        for i in pDict:
            for c in xrange(int(pDict[i])):
                newList.append(int(i))
        ListDict[pid] = newList
    return ListDict


def getNormDisPDFScore(pid, timeListDict, timeHour):
    timeHour = int(timeHour)
    pidTimeList = timeListDict[pid]
    if len(pidTimeList) == 1:
        return 1
    else:

        ary = np.array(pidTimeList)
        mode = int(stats.mode(ary)[0])
        if mode >= 18 or mode <= 6:

            for i in xrange(len(ary)):
                if ary[i] <= 6:
                    ary[i] += 24

            if timeHour <= 6:
                timeHour += 24

        mean = ary.mean()
        std = ary.std()
        if std == 0:
            return 1

        min_inter = 9999
        mean_target = 0
        for x in ary:
            temp_inter = abs(x - mean)
            if temp_inter < min_inter:
                min_inter = temp_inter
                mean_target = x

        mean_target_pdf = stats.norm(mean, std).pdf(mean_target)
        score = (stats.norm(mean, std).pdf(timeHour)) / (mean_target_pdf)
        if math.isnan(score):
            print ary
            print mean
            print std
            print mean_target
            print mean_target_pdf
        return score


if __name__ == '__main__':

    # l = ['CA']
    l = ['CA', 'FB', 'GWL', 'FS']
    for d in l:
        print d
        timeListDict = getTimeListFromDict(d)
        path = '/home/moonorblue/routes/' + d + '/1/'
        for user in listdir(path):

            f = open(path + user)
            j = json.load(f)
            uid = j['uid']
            routes = []
            flag = False
            for r in j['route']:
                if len(j['route'][r]) > 1:
                    flag = True
                    route = []
                    for x in j['route'][r]:
                        pId = x['pid']
                        pTime = x['time']
                        pTimeToHour = datetime.datetime.fromtimestamp(
                            float(pTime)).strftime('%H')
                        timeScore = getNormDisPDFScore(
                            pId, timeListDict, pTimeToHour)
                        route.append(
                            {'pid': pId, 'time': pTime, 'timeScore': timeScore})
                    routes.append(route)
            if flag == True:
                jsonF = {'uid': uid, 'route': routes}
                w = open(
                    '/home/moonorblue/TimeDistribution/' + d + '/' + uid + '.json', 'w')
                w.write(json.dumps(jsonF))
                w.close()

      