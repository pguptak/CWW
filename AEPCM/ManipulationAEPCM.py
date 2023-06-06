import numpy as np
from functools import reduce
import operator


def AEPCMAggregate(X, W):

    #Products of linguistic terms with respective weights
    ProductVector = np.zeros((len(X), 3), dtype=float)
    for i in range(len(X)):
        for j in range(3):
            ProductVector[i][j] = X[i][j] * W[i][j]

    #Collective prefernce vector calculation
    sum_left = 0
    sum_middle = 0
    sum_right = 0
    for i in range(len(ProductVector)):
        sum_left = sum_left + ProductVector[i][0]
        sum_middle = sum_middle + ProductVector[i][1]
        sum_right = sum_right + ProductVector[i][2]
    lc = round(sum_left/len(ProductVector), 2)
    mc = round(sum_middle/len(ProductVector), 2)
    rc = round(sum_right/len(ProductVector), 2)
    return [lc, mc, rc]
