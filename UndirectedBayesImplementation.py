    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # SCANNER AND BINS COMBINED FOR UNDIRECTED GRAPH
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
totalAuthors = 317080
edgeTotal = 1049866
binAmt = 10
biggest = 0
with open("Dataset\com-dblp.ungraph.txt") as f:
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
tupleAdjacencyMatrix = [[0 for x in xrange(binAmt + 1)] for y in xrange(biggest + 1)]
binwidth = biggest/binAmt + 1
with open("Dataset\com-dblp.ungraph.txt") as g:
    lineNum = 1
    for line in g:
        if(lineNum < 5):
            lineNum += 1
        else:
            val, val2 = line.split()
            firstPos = int(val)
            secondPos = int(val2)
            firstBin = firstPos/binwidth
            secondBin = secondPos/binwidth
            if(firstBin == binAmt):
                firstBin -= 1
            if(secondBin == binAmt):
                secondBin -= 1
            tupleAdjacencyMatrix[firstPos][secondBin] += 1
            tupleAdjacencyMatrix[firstPos][10] += 1
            tupleAdjacencyMatrix[secondPos][firstBin] += 1
            tupleAdjacencyMatrix[secondPos][10] += 1
dictionary = {}
j = 0
for a in xrange(biggest):
    if(tupleAdjacencyMatrix[a][10] > 0):
        dictionary[j] = a
        j += 1
for a in xrange(biggest, 0, -1):
    if(tupleAdjacencyMatrix[a][10] == 0):
        del tupleAdjacencyMatrix[a]

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # IMPLEMENT BAYES
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # Use Bayes Algorithm on the data not in training set and also set up evaluation data

import random
def implement_holdout_bayes(coeff):
    testDataMat = [[0 for x in xrange(binAmt + 1)] for y in xrange(totalAuthors)]
    trainingDataMat = [[0 for x in xrange(binAmt + 1)] for y in xrange(totalAuthors)]
    colSum = [0 for x in xrange(binAmt)]
    maxRow = 0
    tMaxRow = 0
    tDataEdges = 0
    for a in range(totalAuthors):
        checker = random.uniform(0,1)
        if(checker > coeff):
            for b in xrange(binAmt):
                testDataMat[maxRow][b] = tupleAdjacencyMatrix[a][b]
            testDataMat[maxRow][10] = a
            maxRow += 1
        else:
            for b in xrange(binAmt):
                trainingDataMat[tMaxRow][b] += tupleAdjacencyMatrix[a][b]
                colSum[b] += tupleAdjacencyMatrix[a][b]
                tDataEdges += tupleAdjacencyMatrix[a][b]
            trainingDataMat[tMaxRow][10] = a
            tMaxRow += 1
    biggestProb = 0
    biggestProbCol = 0
    biggestProbVis = [0 for x in xrange(maxRow)]
    for a in xrange(maxRow):
        for b in xrange(binAmt):
            numerator = testDataMat[a][b] * colSum[b]
            if (numerator > biggestProb):
                biggestProb = numerator
                biggestProbCol = b + 1
        biggestProbVis[a] = biggestProbCol
        biggestProb = 0
    biggestTrainProb = 0
    biggestProbTrainingVis = [0 for x in xrange(tMaxRow)]
    for a in xrange(tMaxRow):
        for b in xrange(binAmt):
            numerator = trainingDataMat[a][b] * colSum[b]
            if (numerator > biggestTrainProb):
                biggestTrainProb = numerator
                biggestProbCol = b + 1
        biggestProbTrainingVis[a] = biggestProbCol
        biggestTrainProb = 0
    return biggestProbVis, biggestProbTrainingVis, maxRow, totalAuthors - maxRow, testDataMat, trainingDataMat

def implement_bootstrap_bayes():
    copyOfDict = dictionary.copy()
    colSum = [0 for x in xrange(binAmt)]
    bootstrapTestMat = [[0 for x in xrange(binAmt + 1)] for y in xrange(totalAuthors)]
    bootstrapTrainingMat = [[0 for x in xrange(binAmt + 1)] for y in xrange(totalAuthors)]
    for a in xrange(totalAuthors):
        randomVal = random.uniform(0, totalAuthors)
        rowVal = int(randomVal)
        for b in xrange(binAmt):
            bootstrapTrainingMat[a][b] = tupleAdjacencyMatrix[rowVal][b]
            colSum[b] += tupleAdjacencyMatrix[rowVal][b]
        bootstrapTrainingMat[a][10] = rowVal
        copyOfDict[rowVal] = -1
    tDataRows = 0
    for a in xrange(totalAuthors - 1):
        if(copyOfDict[a] >= 0):
            for b in xrange(binAmt):
                bootstrapTestMat[tDataRows][b] = tupleAdjacencyMatrix[a][b]
                bootstrapTestMat[tDataRows][10] = a
            tDataRows += 1
    biggestProb = 0
    biggestProbCol = 0
    biggestProbVisTest = [0 for x in xrange(tDataRows)]
    for a in xrange(tDataRows):
        for b in xrange(binAmt):
            numerator = bootstrapTestMat[a][b] * colSum[b]
            if (numerator > biggestProb):
                biggestProb = numerator
                biggestProbCol = b + 1
        biggestProbVisTest[a] = biggestProbCol
        biggestProb = 0
    biggestProbVisTraining = [0 for x in xrange(totalAuthors)]
    for a in xrange(totalAuthors):
        for b in xrange(binAmt):
            numerator = bootstrapTrainingMat[a][b] * colSum[b]
            if (numerator > biggestProb):
                biggestProb = numerator
                biggestProbCol = b + 1
        biggestProbVisTraining[a] = biggestProbCol
        biggestProb = 0
    return biggestProbVisTest, biggestProbVisTraining, tDataRows, bootstrapTestMat, bootstrapTrainingMat



    # IMPLEMENT BAYES

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # EVALUATION MEASURES
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # Check classes given to values outside of training data against themselves if they were in training data

evalColMatrix = [0 for x in xrange(binAmt)]
for a in xrange(totalAuthors):
    for b in xrange(binAmt):
        evalColMatrix[b] += tupleAdjacencyMatrix[a][b]
evalBiggestProb = 0.0
evalBiggestProbCol = 0
evalBiggestProbMat = [[0 for x in xrange(2)] for y in xrange(totalAuthors)]
for a in xrange(totalAuthors):
    for b in xrange(binAmt):
        evalNum = evalColMatrix[b] * tupleAdjacencyMatrix[a][b]
        if evalNum > evalBiggestProb:
            evalBiggestProb = evalNum
            evalBiggestProbCol = b + 1
    evalBiggestProbMat[a][0] = evalBiggestProbCol
    if(a < 317079):
        evalBiggestProbMat[a][1] = dictionary[a]
    evalBiggestProb = 0.0


def checkAccuracy(testProbMatrix, mRow, TDMat):
    totalCorrect = 0
    for a in xrange(mRow):
        if testProbMatrix[a] == evalBiggestProbMat[TDMat[a][10]][0]:
            totalCorrect += 1
    if(mRow == 0):
        mRow += 1
    accuracy = float(totalCorrect)/float(mRow)
    return accuracy

def checkTrainingAccuracy(trainingProbMatrix, totRow, trainMat):
    totalCorrect = 0
    for a in xrange(totRow):
        if trainingProbMatrix[a] == evalBiggestProbMat[trainMat[a][10]][0]:
            totalCorrect += 1
    if(totRow == 0):
        totRow += 1
    accuracy = float(totalCorrect)/float(totRow)
    return accuracy


def checkHome():
    homeMat = [0 for x in xrange(binAmt)]
    totHighestProbInEachBin = [0 for x in xrange(binAmt)]
    qtyTuplesInEachBin = [0 for x in xrange(binAmt)]
    stayHomeLikelihoodMat = [0 for x in xrange(binAmt)]
    for a in xrange(totalAuthors):
        checker = evalBiggestProbMat[a][1] / binwidth
        if checker == 10:
            checker -= 1
        if checker == (evalBiggestProbMat[a][0] - 1):
            homeMat[checker] += 1
        totHighestProbInEachBin[evalBiggestProbMat[a][0] - 1] += 1
        qtyTuplesInEachBin[checker] += 1
    homeDominanceMat = [0 for x in xrange(binAmt)]
    for a in xrange(binAmt):
        homeDominanceMat[a] = 100.0 * (float(homeMat[a]) / float(totHighestProbInEachBin[a]))
        stayHomeLikelihoodMat[a] = 100.0 * (float(homeMat[a]) / float(qtyTuplesInEachBin[a]))
    for a in xrange(binAmt):
        print "Probability a tuple in bin", a + 1, "stays in its own bin:                   ", "%.2f" % stayHomeLikelihoodMat[a], "%"
        print "Probability a tuple in highest probability bin", a + 1, "is in its home bin: ", "%.2f" % homeDominanceMat[a], "%"
        print "-------------------------------------------------------------------------------"

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
bootstrapAccuracy = 0.0
bootstrapTrainingAccuracy = 0.0
for a in xrange(kRuns):
    numRuns = 3
    holdoutAccuracy = 0.0
    holdoutTrainingAccuracy = 0.0
    coefficient = coeffMat[a]
    start = timeit.default_timer()
    coeff = float(coefficient)
    for b in xrange(numRuns):
        biggestProbMat, biggestProbTrainingMat, maxRow, tMaxRow, testDataMat, trainDataMat = implement_holdout_bayes(coeff)
        bootstrapProbMat, bootstrapTrainMat, tDataRows, testMat, trainMat = implement_bootstrap_bayes()
        bootstrapAccuracy += checkAccuracy(bootstrapProbMat, tDataRows, testMat)
        bootstrapTrainingAccuracy += checkTrainingAccuracy(bootstrapTrainMat, totalAuthors, trainMat)
        holdoutAccuracy += checkAccuracy(biggestProbMat, maxRow, testDataMat)
        holdoutTrainingAccuracy += checkTrainingAccuracy(biggestProbTrainingMat, tMaxRow, trainDataMat)
    stop = timeit.default_timer()
    timeTaken += (stop - start)
    print "Run number:", a + 1
    print "--------------"
    print "Ratio of training data to total data:                        ", coeffMat[a]
    print "Time for this run:                                           ", stop - start
    print "Number of test data tuples:                                  ", int(math.ceil((1 - coeffMat[a]) * totalAuthors))
    print "Correctly identified tuples in holdout", numRuns, "run avg%:           ",holdoutAccuracy * (100.0/numRuns)
    print "Correctly identified train tuples in holdout", numRuns, "run avg%:     ", holdoutTrainingAccuracy * (100.0/numRuns)
    print "-------------------------------------------------------------------------------"
checkHome()
print "Correctly identified tuples in bootstrap test data", numRuns * kRuns, "run avg%      ", bootstrapAccuracy * (100.0 / (numRuns * kRuns))
print "Correctly identified tuples in bootstrap training data", numRuns * kRuns, "run avg%  ", bootstrapTrainingAccuracy * (100.0 / (numRuns * kRuns))
print "Total run time:  ", timeTaken
print "------------------------------"

