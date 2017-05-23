import math
import sys

def iround(x):
        return int(round(x) - .5) + (x > 0)


total = len(sys.argv)
cmdargs = str(sys.argv)

if (total < 3):
        print ("Usage: python prepareDate csvFile csvOutFile divValue")
        sys.exit(0)


if (total == 4):
        divValue = int(sys.argv[3])
else: 
        divValue = 1000000

inFile = sys.argv[1]
outFile = sys.argv[2]

import csv

probSum = 0

d = dict()

with open(inFile, 'rb') as inFileCSV:
        csvReader = csv.reader(inFileCSV, delimiter=',', quotechar='|')
        for row in csvReader:
                if (len(row) == 2):
                        value = (int(row[0])/divValue)
                        prob = float(row[1])
                        probSum = probSum + prob
                        print (value, prob)
                        if value in d:
                                d[value] += prob
                        else:
                                d.update({value:prob})
                                


#print probSum

for key in d:
        print ("%d,%f"  % (key , (d[key]/probSum)))


with open(outFile, 'wb') as outFileCSV:
        write = csv.writer(outFileCSV, delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for key in d:
                string = ("%d,%f"  % (key , (d[key]/probSum)))
                write.writerow ([string])
        
