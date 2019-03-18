import numpy as np 

def getRandIdx(size, num, replace = False):
    lst = list(range(size))
    return np.random.choice(lst,num, replace)
