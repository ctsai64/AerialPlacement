# last updated 12/29/2023

import sys
sys.path.append("..")
from detector import detector

def getPosition(result):
    return result[3][0]
    # if x > 330:
    #    return ['l', x - 330]
    # elif x < 310:
    #     return ['r', 310 - x]
    # else:
    #    return ["s"]


#while True:
#    go = input("Go?")
#    if go == "y":
#        re = detector.pops()
#        if re[0] == 'cup':
#            print(find(re[3][0]))
#            print(re)
