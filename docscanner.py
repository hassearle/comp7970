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
    binwidth = totalRange/10
    currentBin = 0
    dbPlace = -1
    prevVal = ""
    intMatrix = [[0 for x in xrange(10)] for y in xrange(5242)]
    for i in range(0, 5242):
        for j in range(0, 10):
            intMatrix[i][j] = 0
    for line in g:
        val, other = line.split()
        coauthVal = int(other)
        currentBin = (coauthVal - small - 1)/binwidth
        if(val != prevVal):
            dbPlace = dbPlace + 1
        if(dbPlace < 5242):
            if(currentBin == 10):
                currentBin -= 1
            intMatrix[dbPlace][currentBin] += 1
        prevVal = val
    for t in range(0, 5242):
        print intMatrix[t]
