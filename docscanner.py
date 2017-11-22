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

with open("C:\Users\Tyler\Documents\School 17-18\Big Data 17\Dataset\CA-GrQc2.txt") as g:          # opens file
    
    binAmt = 10                                                     # number of bins to partition db
    totalRange = big - small                                        # db range
    binwidth = totalRange/binAmt                                    # num of authors that make up 1 bin
    currentBin = 0
    prevBin = 0
    dbRow = -1
    prevVal = ""
    intMatrix = [[0 for x in xrange(binAmt)] for y in xrange(totalAuthors)]     # matrix[author][coAuthor Bins]
    binTotal = [0 for x in xrange(binAmt)]      # binTotal += for each row 
                                                                                    # ie:
                                                                                    # row 1: binA = 1, binB = 4,...
                                                                                    # row 2: binA = 1+2, binB = 4+1,...
    binRowSum = [0 for x in xrange(totalAuthors)]                                                               # sum of bins 1-10 for each row
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
    del i
    for i in range(0, 5242):
        print intMatrix[i]

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # SPLIT DATASET
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # split dataset into training/test data

evalColMatrix = [0 for y in xrange(binAmt)]
for a in range(0, 5242):
    for b in range(0, binAmt):
        evalColMatrix[b] += intMatrix[a][b]

import random
coefficient = 99.0/100.0
holdoutMat = [[0 for x in xrange(10)] for y in xrange(5242)]
for a in range(0, 5242):
    for b in range(0, 10):
        currentPos = random.uniform(0,1)
        if(currentPos > coefficient):
            holdoutMat[a][b] = 1
        else:
            holdoutMat[a][b] = 0
for c in xrange(5242):
    print holdoutMat[c]
del a, b, c
holdoutColMat = [[0 for x in xrange(10)] for y in xrange(10)]
totalHAuth = [0 for x in xrange(10)]
totalToRun = [0 for x in xrange(10)]
for c in xrange(10):
    for a in range(0, totalAuthors):
        if(holdoutMat[a][c] == 0):
            for b in range(0, binAmt):
                holdoutColMat[c][b] += intMatrix[a][b]
                totalHAuth[c] += intMatrix[a][b]
        else:
            totalToRun[c] += 1
    print totalHAuth[c]
del a, b, c, f, g, i, j, line, other, trash, x, y, big, small, coauthVal, currentBin, dbRow, prevVal, prevBin




    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # IMPLEMENT BAYES
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # Use Bayes Algorithm on the data not in training set and also set up evaluation data

def implement_bayes(column):
    biggestProb = 0.0
    biggestProbCol = 0
    biggestProbVis = [0 for x in xrange(5242)]
    for a in range(0, 5242):
        for b in range(0, 10):
            denominator = binRowSum[a] * totalHAuth[column]
            numerator = holdoutColMat[column][b] * intMatrix[a][b]
            fldivision = float(numerator)/float(denominator)
            if (fldivision > biggestProb):
                biggestProb = fldivision
                biggestProbCol = b + 1
        biggestProbVis[a] = biggestProbCol
        biggestProb = 0.0
    return biggestProbVis
    # IMPLEMENT BAYES

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # EVALUATION MEASURES
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # Check classes given to values outside of training data against themselves if they were in training data

evalBiggestProb = 0.0
evalBiggestProbCol = 0
evalBiggestProbMat = [0 for t in xrange(0, 5242)]
for a in xrange(5242):
    for b in xrange(10):
        evalDenom = binRowSum[a] * edgeTotal
        evalNum = evalColMatrix[b] * intMatrix[a][b]
        fldivision = float(evalNum)/float(evalDenom)
        if(fldivision > evalBiggestProb):
            evalBiggestProb = fldivision
            evalBiggestProbCol = b + 1
        evalBiggestProbMat[a] = evalBiggestProbCol
        evalBiggestProb = 0.0


def eval(column, testProbMatrix):
    totalCorrect = 0
    totalPossible = totalToRun[column]
    for a in xrange(totalAuthors):
        if(holdoutMat[a][column] == 1):
            if(testProbMatrix[a] == evalBiggestProbMat[a]):
                totalCorrect += 1
    accuracy = float(totalCorrect)/float(totalPossible)
    return accuracy

for col in xrange(10):
    biggestProbCol = implement_bayes(col)
    for a in xrange(5242):
        print biggestProbCol[a]
        print intMatrix[a]
        print
    print eval(col, biggestProbCol)