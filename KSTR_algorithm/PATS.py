import numpy as np
from scipy.sparse import dok_matrix
from os import listdir
import json


def fromIdxDictToGetScore(reverseIdxDict, scoreMatrix):
    finalScoreDict = {}
    for i in reverseIdxDict:
        finalScoreDict[reverseIdxDict[i]] = round(scoreMatrix[i + 1, 0], 4)

    return finalScoreDict


def matrixMulti(scoreMatrix,dataset):
    size = scoreMatrix.shape[0]
    initialMatrix = dok_matrix((size + 1, 1))
    for i in xrange(size + 1):
        initialMatrix[i, 0] = 1

    for i in xrange(100):
        print dataset,' Multi #:',i
        initialMatrix = scoreMatrix.dot(initialMatrix)
        initialMatrix_n = dok_matrix((size + 1, 1))
        initialMatrix_n[0, 0] = 1
        for m in xrange(initialMatrix.shape[0]):
            initialMatrix_n[m + 1, 0] = initialMatrix[m, 0]
        initialMatrix = initialMatrix_n

    return initialMatrix


def constructScoreMatrix(scoreDict, idToidxDict, alpha):
    size = len(scoreDict)
    S = dok_matrix((size - 1, size))
    for k in scoreDict:
        S[idToidxDict[k[0]], idToidxDict[k[1]] + 1] = scoreDict[k]
    for i in xrange(size - 1):
        S[i, 0] = 1 - alpha
    return S


def calEdgeScore(pairCountsDict, startCountsDict, alpha):
    scoreDict = {}
    for pair in pairCountsDict:
        countsFromStartNode = startCountsDict[pair[0]]
        countsFromStartToEndNode = pairCountsDict[pair]
        score = alpha * (float(countsFromStartToEndNode) / countsFromStartNode)
        scoreDict[pair] = score

    return scoreDict


def extractEdgePairs(AllTrajectores):
    pairCountsDict = {}
    startCountsDict = {}
    idToidxDict = {}
    idxCount = 0
    for r in AllTrajectores:
        previous = ''
        for i in xrange(len(r)):
            if str(r[i]) not in idToidxDict:
                idToidxDict[str(r[i])] = idxCount
                idxCount += 1

            if i == 0:
                previous = str(r[i])
                continue
            else:
                pair = (previous, str(r[i]))
                if pair not in pairCountsDict:
                    pairCountsDict[pair] = 1
                else:
                    pairCountsDict[pair] += 1

                if previous not in startCountsDict:
                    startCountsDict[previous] = 1
                else:
                    startCountsDict[previous] += 1

                previous = str(r[i])

    return pairCountsDict, startCountsDict, idToidxDict


def loadRoutes(version, dataset, day):
    totalR = []

    if version == '1':
        ver = 'routes'
    else:
        ver = 'routesV2'

    path = '/home/moonorblue/' + ver + '/' + dataset + '/' + day + '/'
    for user in listdir(path):
        f = open(path + user)
        j = json.load(f)
        for r in j['route']:
            if len(j['route'][r]) > 1:
                route = []
                for d in j['route'][r]:
                    route.append(d['pid'])
                totalR.append(route) 
                

    return totalR


if __name__ == '__main__':

    l = ['FB','GWL','FS']
    # l = ['CA']
    for d in l:
        print '####loadRoutes'
        totalRoutes = loadRoutes('1', d, '1')

        pairCountsDict, startCountsDict, idToidxDict = extractEdgePairs(
            totalRoutes)
        print '####calEdgeScore'
        scoreDict = calEdgeScore(pairCountsDict, startCountsDict, 0.7)
        print '####constructScoreMatrix'
        scoreMatrix = constructScoreMatrix(scoreDict, idToidxDict, 0.7)
        print '####matrixMulti'
        finalMatrix = matrixMulti(scoreMatrix,d)
        reverseIdxDict = {idToidxDict[k]: k for k in idToidxDict}
        print '####fromIdxDictToGetScore' 
        finalSocreDict = fromIdxDictToGetScore(reverseIdxDict, finalMatrix)

        w = open('/home/moonorblue/PATS/' + d + '/' + 'result', 'w')
        w.write(json.dumps(finalSocreDict))
        w.close()
