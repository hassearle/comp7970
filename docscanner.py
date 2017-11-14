dictionary = {}
prevVal = ""
with open("C:\Users\Tyler\Documents\School 17-18\Big Data 17\Dataset\CA-GrQc2.txt") as f:
    j = 0
    for line in f:
        val, trash = line.split()
        if(val != prevVal):
            dictionary[j] = int(val)
            prevVal = val
            j = j + 1
    big = dictionary[0]
    small = dictionary[0]
    for i in range(0, 5242):
        if(dictionary[i] > big):
            big = dictionary[i]
        if(dictionary[i] < small):
            small = dictionary[i]
with open("C:\Users\Tyler\Documents\School 17-18\Big Data 17\Dataset\CA-GrQc2.txt") as g:
    totalRange = big - small
    binWidth = totalRange/10
    currentBin = 0
    rowTotal = 0
    binSplit = 0.3
    dbPlace = -1
    prevVal = ""
    intMatrix = [[0 for x in xrange(11)] for y in xrange(5243)]
    for i in range(0, 5243):
        for j in range(0, 11):
            intMatrix[i][j] = 0
    for line in g:
        val, other = line.split()
        coauthVal = int(other)
        currentBin = (coauthVal - small - 1)/binWidth
        if(val != prevVal):
            intMatrix[dbPlace][10] = rowTotal
            rowTotal = 0
            dbPlace = dbPlace + 1
        if(dbPlace < 5242):
            if(currentBin == 10):
                currentBin -= 1
            intMatrix[dbPlace][currentBin] += 1
            rowTotal += 1
        if(dbPlace < 5242 * binSplit):
            intMatrix[5242][currentBin] += 1
        prevVal = val
    biggestProb = 0.0
    biggestProbCol = 0
    for a in range(0, 5242):
        for b in range(0, 10):
            denominator = intMatrix[a][10] * intMatrix[5242][b]
            if(denominator == 0):
                denominator += 100000
            numerator = 0.0 + intMatrix[a][b]
            if(numerator/denominator > biggestProb):
                biggestProb = numerator/denominator
                biggestProbCol = b
        print dictionary[a]
        print intMatrix[a]
        print biggestProbCol
        print intMatrix[5242]
        biggestProb = 0.0


