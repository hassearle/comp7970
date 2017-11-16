        # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        # SCANNER
        # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        # indexes authors
        # finds largest/smallest author

dictionary = {}
prevVal = ""
with open("C:\Users\Tyler\Documents\School 17-18\Big Data 17\Dataset\CA-GrQc2.txt") as f:  # opens file
    totalAuthors = 5242
    j = 0
    for line in f:  # loops thru db
        val, trash = line.split()  #
        if (val != prevVal):  # indexes every author once
            dictionary[j] = int(val)
            if j == 0:  # sets big&small to first author
                big = dictionary[j]
                small = dictionary[j]

            if (dictionary[j] > big):  # finds the largest author name
                big = dictionary[j]
            if (dictionary[j] < small):  # finds the smallest author name
                small = dictionary[j]

            prevVal = val
            j += 1

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # BINS
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

with open("C:\Users\Tyler\Documents\School 17-18\Big Data 17\Dataset\CA-GrQc2.txt") as g:  # opens file

    binAmt = 10  # number of bins to partition db
    totalRange = big - small  # db range
    binwidth = totalRange / binAmt  # num of authors that make up 1 bin
    currentBin = 0
    dbRow = -1
    prevVal = ""
    intMatrix = [[0 for x in xrange(binAmt)] for y in xrange(totalAuthors)]  # matrix[author][coAuthor Bins]
    binTotal = [[0 for x in xrange(binAmt)] for y in xrange(totalAuthors)]  # binTotal += for each row
    # ie:
    # row 1: binA = 1, binB = 4,...
    # row 2: binA = 1+2, binB = 4+1,...
    binRowSum = [0 for x in xrange(totalAuthors)]  # sum of bins 1-10 for each row
    for i in range(0, totalAuthors):
        for j in range(0, binAmt):
            intMatrix[i][j] = 0
    for line in g:
        val, other = line.split()
        coauthVal = int(other)
        currentBin = (coauthVal - small - 1) / binwidth
        if (val != prevVal):
            dbRow = dbRow + 1
        if (dbRow < totalAuthors):
            if (currentBin == binAmt):  # checks for overflow
                currentBin -= 1
            intMatrix[dbRow][currentBin] += 1
            binRowSum[dbRow] += 1  # adds the total of the row
        prevVal = val

        # sum of bins

    count = 0
    for t in range(0, totalAuthors):
        count += 1
        print intMatrix[t], binRowSum[t], count


    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # SPLIT DATASET
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # split dataset into training/test data

splitRatio = .3
splitTotal = splitRatio * totalAuthors
trainingColMatrix = [0 for x in xrange(binAmt)]
for a in range(0, int(splitTotal)):
    for b in range(0, binAmt):
        trainingColMatrix[b] += intMatrix[a][b]
print trainingColMatrix
del a
del b

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # IMPLEMENT BAYES
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # Use Bayes Algorithm on the data not in trianing set

biggestProb = 0.0
biggestProbCol = 0
for a in range(int(splitTotal), 5242):
    for b in range(0, 10):
        denominator = binRowSum[a] * trainingColMatrix[b]
        numerator = 0.0 + intMatrix[a][b]
        if (numerator / denominator > biggestProb):
            biggestProb = numerator / denominator
            biggestProbCol = b
    print dictionary[a]
    print intMatrix[a]
    print biggestProbCol + 1
    print trainingColMatrix
    biggestProb = 0.0