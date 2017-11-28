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
    for line in f:                                                  # loops thru db
        val, trash = line.split()                                   #
        if(val != prevVal):                                         # indexes every author once
            dictionary[j] = int(val)
            if j == 0:                                              # sets big&small to first author
                big = dictionary[j]
                small = dictionary[j]

            if(dictionary[j] > big):                                # finds the largest author name
                    big = dictionary[j]
            if(dictionary[j] < small):                              # finds the smallest author name
                small = dictionary[j]

            prevVal = val
            j += 1
        
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= 
# BINS 
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
with open("C:\Users\Tyler\Documents\School 17-18\Big Data 17\Dataset\CA-GrQc2.txt") as g:           # opens file
    totalRange = big - small                                                                        # db range
    binAmt = 10
    binwidth = totalRange/binAmt                                                                    # num of authors that make up 1 bin
    currentBin = 0
    prevBin = 0
    dbRow = -1
    prevVal = ""
    intMatrix = [[0 for x in xrange(binAmt)] for y in xrange(totalAuthors)]         # matrix[author][coAuthor Bins]
    binTotal = [0 for x in xrange(binAmt)]                                          # binTotal += for each row
                                                                                    # ie:
                                                                                    # row 1: binA = 1, binB = 4,...
                                                                                    # row 2: binA = 1+2, binB = 4+1,...
    binRowSum = [0 for x in xrange(totalAuthors)]                                   # sum of bins 1-10 for each row
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
            binRowSum[dbRow] += 1                                   # adds the total of the row


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
            denominator = binRowSum[testDataMat[a][10]] * tDataEdges
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

import timeit
timeTaken = 0.0
kRuns = 10
accuracyMat = [0 for x in xrange(kRuns)]
for a in xrange(kRuns):
    accuracy = 0.0
    coefficient = raw_input("Enter coefficient as a decimal: ")
    start = timeit.default_timer()
    coeff = float(coefficient)
    for b in xrange(10):
        biggestProbMat, maxRow, testDataMat = implement_bayes(coeff)
        accuracy += eval(maxRow, biggestProbMat, testDataMat)
    stop = timeit.default_timer()
    timeTaken += (stop - start)
    print accuracy/10.0
    accuracyMat[a] = accuracy/10.0
print timeTaken