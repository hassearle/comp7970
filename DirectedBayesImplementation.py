#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# SCANNER
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # indexes authors
    # finds largest/smallest author
dictionary = {}
prevVal = ""
with open("C:\Users\Tyler\Documents\School 17-18\Big Data 17\Dataset\CA-GrQc2.txt") as f:          # opens file
    totalAuthors = 5242
    edgeTotal = 28980
    j = 0
    big = 0
    small = 0
    for line in f:                                                  # loops thru db
        val, trash = line.split()                                   #
        if val != prevVal:                                          # indexes every author once
            dictionary[j] = int(val)
            if j == 0:                                              # sets big&small to first author
                big = dictionary[j]
                small = dictionary[j]

            if dictionary[j] > big:                                # finds the largest author name
                    big = dictionary[j]
            if dictionary[j] < small:                              # finds the smallest author name
                small = dictionary[j]

            prevVal = val
            j += 1
        
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= 
# BINS 
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
with open("C:\Users\Tyler\Documents\School 17-18\Big Data 17\Dataset\CA-GrQc2.txt") as g:           # opens file
    totalRange = big - small                                                                        # db range
    binAmt = 10
    binwidth = totalRange/binAmt                                                    # num of authors that make up 1 bin
    currentBin = 0
    prevBin = 0
    dbRow = -1
    prevVal = ""
    intMatrix = [[0 for x in xrange(binAmt)] for y in xrange(totalAuthors)]         # matrix[author][coAuthor Bins]
    binTotal = [0 for x in xrange(binAmt)]                                          # binTotal gives total of each bin                                                                                  # row 2: binA = 1+2, binB = 4+1,...
    rowSum = [0 for x in xrange(totalAuthors)]                                   # rowSum gives total of each row
    for i in range(0, totalAuthors):
        for j in range(0, binAmt):
            intMatrix[i][j] = 0
    for line in g:
        val, other = line.split()
        coauthVal = int(other)
        currentBin = (coauthVal - small - 1)/binwidth
        if(val != prevVal):
            dbRow += 1
        if(dbRow < totalAuthors):
            if(currentBin == binAmt):                               # checks for overflow
                currentBin -= 1
            intMatrix[dbRow][currentBin] += 1
            rowSum[dbRow] += 1                                   # adds the total of the row


            if(prevBin != currentBin):
                binTotal[currentBin] += intMatrix[dbRow][currentBin]
                prevBin = currentBin

        prevVal = val


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
            denominator = rowSum[testDataMat[a][10]] * tDataEdges
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
evalBiggestProbMat = [[0 for x in xrange(2)] for y in xrange(totalAuthors)]
for a in xrange(totalAuthors):
    for b in xrange(binAmt):
        evalNum = evalColMatrix[b] * intMatrix[a][b]
        if(evalNum > evalBiggestProb):
            evalBiggestProb = evalNum
            evalBiggestProbCol = b + 1
    evalBiggestProbMat[a][0] = evalBiggestProbCol
    evalBiggestProbMat[a][1] = dictionary[a]
    evalBiggestProb = 0.0


def eval(mRow, testProbMatrix, TDMat):
    totalCorrect = 0
    for a in xrange(mRow):
        if(testProbMatrix[a] == evalBiggestProbMat[TDMat[a][10]][0]):
            totalCorrect += 1
    accuracy = float(totalCorrect)/float(mRow)
    return accuracy

def checkHome():
    homeMat = [0 for x in xrange(binAmt)]
    totHighestProbInEachBin = [0 for x in xrange(binAmt)]
    qtyTuplesInEachBin = [0 for x in xrange(binAmt)]
    stayHomeLikelihoodMat = [0 for x in xrange(binAmt)]
    for a in xrange(totalAuthors):
        checker = evalBiggestProbMat[a][1] / binwidth
        if (checker == 10):
            checker -= 1
        if (checker == (evalBiggestProbMat[a][0] - 1)):
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
for a in xrange(kRuns):
    numRuns = 10
    accuracy = 0.0
    coefficient = coeffMat[a]
    start = timeit.default_timer()
    coeff = float(coefficient)
    evalTime = 0.0
    bayesTime = 0.0
    for b in xrange(numRuns):
        biggestProbMat, maxRow, testDataMat = implement_bayes(coeff)
        accuracy += eval(maxRow, biggestProbMat, testDataMat)
    stop = timeit.default_timer()
    timeTaken += (stop - start)
    print "Run number:", a + 1
    print "--------------"
    print "Ratio of training data to total data:        ", coeffMat[a]
    print "Time for this run:                           ", stop - start
    print "Number of test data tuples:                  ", int(math.ceil((1 - coeffMat[a]) * totalAuthors))
    print "Correctly identified tuples", numRuns, "run avg%:     ",accuracy * (100.0/numRuns)
    if(a < 9):
        print "-------------------------------------------------------------------"
    else:
        print "-------------------------------------------------------------------------------"
checkHome()
print "Total run time:  ", timeTaken
print "------------------------------"