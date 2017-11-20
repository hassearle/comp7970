#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= 
# SCANNER 
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # indexes authors
    # finds largest/smallest author

dictionary = {}
prevVal = ""
with open("C:\Users\Tyler\Documents\School 17-18\Big Data 17\Dataset\CA-GrQc2.txt") as f:          # opens file
    totalAuthors = 5242
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

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # SPLIT DATASET
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # split dataset into training/test data

splitRatio = .3
splitTotal = splitRatio * totalAuthors
trainingColMatrix = [0 for x in xrange(binAmt)]
trainingMatTotal = 0
for a in range(0, int(splitTotal)):
    for b in range(0, binAmt):
        trainingColMatrix[b] += intMatrix[a][b]
print trainingColMatrix
for c in range(0, binAmt):
    trainingMatTotal += trainingColMatrix[c]
print trainingMatTotal
del a, b, c, f, g, i, j, line, other, trash, x, y, big, small, coauthVal, currentBin, dbRow, prevVal, prevBin, splitRatio



    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # IMPLEMENT BAYES
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # Use Bayes Algorithm on the data not in trianing set

biggestProb = 0.0
biggestProbCol = 0
fldivision = 0.0
biggestProbVis = [0 for x in xrange(0, 5242)]
for a in range(int(splitTotal), 5242):
    for b in range(0, 10):
        denominator = binRowSum[a] * trainingMatTotal
        numerator = trainingColMatrix[b] * intMatrix[a][b]
        fldivision = float(numerator)/float(denominator)
        if (fldivision > biggestProb):
            biggestProb = fldivision
            biggestProbCol = b + 1
    biggestProbVis[a] = biggestProbCol
    #print dictionary[a]
    #print intMatrix[a]
    #print biggestProbCol
    #print trainingColMatrix
    biggestProb = 0.0
    # IMPLEMENT BAYES
for x in range(0, 5242):
    print intMatrix[x]
    print binRowSum[x]
    print biggestProbVis[x]