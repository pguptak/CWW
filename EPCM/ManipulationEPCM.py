import numpy as np
from functools import reduce
import operator


def EPCMAggregate(X):
    CollectivePreferenceVector = np.zeros((1, 3), dtype=float)
    sum_left = 0
    sum_middle = 0
    sum_right = 0
    for i in range(len(X)):
        sum_left = sum_left + X[i][0]
        sum_middle = sum_middle + X[i][1]
        sum_right = sum_right + X[i][2]
    lc = round(sum_left/len(X), 2)
    mc = round(sum_middle/len(X), 2)
    rc = round(sum_right/len(X), 2)
    return [lc, mc, rc]
