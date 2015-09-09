import time
import datetime
import json
from os import listdir
import scipy.stats as stats
import numpy as np
import math

if __name__ == '__main__':

    # l = ['CA']
    placeCountDict = {}
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

                        if pId not in placeCountDict:
                            placeCountDict[str(pId)]={}
                            countDict=placeCountDict[str(pId)]
                            if pTimeToHour not in countDict:
                                countDict[pTimeToHour]=1
                            else:
                                countDict[pTimeToHour] += 1
                        else:
                            countDict=placeCountDict[str(pId)]
                            if pTimeToHour not in countDict:
                                countDict[pTimeToHour]=1
                            else:
                                countDict[pTimeToHour] += 1

        w=open('/home/moonorblue/TimeDistribution/' + d + '/' + 'result', 'w')
        w.write(json.dumps(placeCountDict))
        w.close()
