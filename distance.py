# last upddated 1/26/2024

import math
import numpy
import sys
sys.path.append("..")
from detector import detector

x = []
y = []
eq = numpy.polyfit(x, y, 2)

def getDistance(result):#(x1, y1, x2, y2):
    px = result[2] #result[2][0] - result[1][0] #int(math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2))
    cm = eq[0]*px**2 + eq[1]*px + eq[2]
    return cm

while True:
    go = input("Collect? (y/n) ")
    if go == "y":
        r = detector.returnResults()
        if r[0] == "cup":
            print((r[2][0] - r[1][0]))
        else:
            print("cup not in view")