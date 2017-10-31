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
    print big
    print small
    
