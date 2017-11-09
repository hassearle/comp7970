#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= 
# SCANNER 
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # indexes authors
    # finds largest/smallest author

dictionary = {}
prevVal = ""
with open("/root/code/comp7970/Dataset/CA-GrQc.txt") as f:          # opens file
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
        

with open("/root/code/comp7970/Dataset/CA-GrQc.txt") as g:
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
