    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # SCANNER AND BINS COMBINED FOR UNDIRECTED GRAPH
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
totalAuthors = 317080
edgeTotal = 1049866
binAmt = 10
biggest = 0
with open("C:\Users\Tyler\Documents\School 17-18\Big Data 17\Dataset\com-dblp.ungraph.txt") as f:
    lineNum = 1
    for line in f:
        if(lineNum < 5):
            lineNum += 1
        else:
            val, val2 = line.split()
            if(int(val) > biggest):
                biggest = int(val)
            if(int(val2) > biggest):
                biggest = int(val2)
intMatrix = [[0 for x in xrange(binAmt + 1)] for y in xrange(biggest + 1)]
binWidth = biggest/binAmt + 1
with open("C:\Users\Tyler\Documents\School 17-18\Big Data 17\Dataset\com-dblp.ungraph.txt") as g:
    lineNum = 1
    for line in g:
        if(lineNum < 5):
            lineNum += 1
        else:
            val, val2 = line.split()
            firstPos = int(val)
            secondPos = int(val2)
            firstBin = firstPos/binWidth
            secondBin = secondPos/binWidth
            if(firstBin == binAmt):
                firstBin -= 1
            if(secondBin == binAmt):
                secondBin -= 1
            intMatrix[firstPos][secondBin] += 1
            intMatrix[firstPos][10] += 1
            intMatrix[secondPos][firstBin] += 1
            intMatrix[secondPos][10] += 1
dictionary = {}
j = 0
for a in xrange(biggest):
    if(intMatrix[a][10] > 0):
        dictionary[j] = a
        j += 1
for a in xrange(biggest, 0, -1):
    if(intMatrix[a][10] == 0):
        del intMatrix[a]

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # IMPLEMENT BAYES
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # Use Bayes Algorithm on the data not in training set and also set up evaluation data

import random
def implement_bayes(coeff):
    testDataMat = [[0 for x in xrange(binAmt + 1)] for y in xrange(totalAuthors)]
    colSum = [0 for x in xrange(binAmt)]
    maxRow = 0
    tDataEdges = 0
    for a in range(totalAuthors):
        checker = random.uniform(0,1)
        if(checker > coeff):
            for b in xrange(10):
                testDataMat[maxRow][b] = intMatrix[a][b]
            testDataMat[maxRow][10] = a
            maxRow += 1
        else:
            for b in xrange(10):
                colSum[b] += intMatrix[a][b]
                tDataEdges += intMatrix[a][b]
    biggestProb = 0.0
    biggestProbCol = 0
    biggestProbVis = [0 for x in xrange(maxRow)]
    for a in xrange(maxRow):
        for b in xrange(binAmt):
            denominator = intMatrix[a][10] * tDataEdges
            numerator = testDataMat[a][b] * colSum[b]
            fldivision = float(numerator)/float(denominator)
            if (fldivision > biggestProb):
                biggestProb = fldivision
                biggestProbCol = b + 1
        biggestProbVis[a] = biggestProbCol
        biggestProb = 0.0
    return biggestProbVis, maxRow, testDataMat
    # IMPLEMENT BAYES

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # EVALUATION MEASURES
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # Check classes given to values outside of training data against themselves if they were in training data

evalColMatrix = [0 for x in xrange(binAmt)]
for a in xrange(totalAuthors):
    for b in xrange(binAmt):
        evalColMatrix[b] += intMatrix[a][b]
evalBiggestProb = 0.0
evalBiggestProbCol = 0
evalBiggestProbMat = [0 for x in xrange(totalAuthors)]
for a in xrange(totalAuthors):
    for b in xrange(binAmt):
        evalNum = evalColMatrix[b] * intMatrix[a][b]
        if(evalNum > evalBiggestProb):
            evalBiggestProb = evalNum
            evalBiggestProbCol = b + 1
    evalBiggestProbMat[a] = evalBiggestProbCol
    evalBiggestProb = 0.0


def eval(mRow, testProbMatrix, TDMat):
    totalCorrect = 0
    for a in xrange(mRow):
        if(testProbMatrix[a] == evalBiggestProbMat[TDMat[a][10]]):
            totalCorrect += 1
    accuracy = float(totalCorrect)/float(mRow)
    return accuracy

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # TIMING AND ACCURACY CHECK
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # Run Bayes on randomized sets of training and test data 10 times for each ratio of training data to total data. Check timing on each

import timeit
import math
timeTaken = 0.0
kRuns = 10
coeffMat = [0.01, 0.05, 0.1, 0.25, 0.4, 0.6, 0.75, 0.9, 0.95, 0.99]
timingMat = [0 for x in xrange(10)]
for a in xrange(kRuns):
    numRuns = 10
    accuracy = 0.0
    coefficient = coeffMat[a]
    start = timeit.default_timer()
    thisRun = timeit.default_timer()
    coeff = float(coefficient)
    evalTime = 0.0
    bayesTime = 0.0
    for b in xrange(numRuns):
        startBayes = timeit.default_timer()
        biggestProbMat, maxRow, testDataMat = implement_bayes(coeff)
        stopBayes = timeit.default_timer()
        bayesTime += stopBayes - startBayes
        startEval = timeit.default_timer()
        accuracy += eval(maxRow, biggestProbMat, testDataMat)
        stopEval = timeit.default_timer()
        evalTime += (stopEval - startEval)
    timingMat[a] = evalTime
    stop = timeit.default_timer()
    thisStop = timeit.default_timer()
    timeTaken += (stop - start)
    print "Run number:", a + 1
    print coeffMat[a], "ratio of training data/total data"
    print thisStop - thisRun, "seconds"
    print bayesTime, "Seconds for Bayes"
    print evalTime, "Seconds for evaluation"
    print "Number of test data tuples:", int(math.ceil((1 - coeffMat[a]) * totalAuthors))
    print accuracy * (100.0/numRuns), "% correctly identified tuples on average over", numRuns, "runs"
    print "XXXXXXXXXXXXX"
print timeTaken, "total seconds taken for all runs"

