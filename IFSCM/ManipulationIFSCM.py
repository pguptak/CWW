import numpy as np
from functools import reduce
import operator


def IFSCMAggregate(X, W, XNon, WNon):

    #Products of membership functions linguistic terms with respective weights
    ProductVector = np.zeros((len(X), 3), dtype=float)
    for i in range(len(X)):
        for j in range(3):
            ProductVector[i][j] = X[i][j] * W[i][j]

    #Products of non membership functions linguistic terms with respective weights
    ProductVectorNon = np.zeros((len(XNon), 3), dtype=float)
    for i in range(len(XNon)):
        for j in range(3):
            ProductVectorNon[i][j] = XNon[i][j] * WNon[i][j]

    #Collective prefernce vector calculation membership function
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

    # Collective preference vector calculation nonmembership function
    sum_left_non = 0
    sum_middle_non = 0
    sum_right_non = 0
    for i in range(len(ProductVectorNon)):
        sum_left_non = sum_left_non+ ProductVectorNon[i][0]
        sum_middle_non = sum_middle_non + ProductVectorNon[i][1]
        sum_right_non = sum_right_non + ProductVectorNon[i][2]
    lc_non = round(sum_left_non / len(ProductVectorNon), 2)
    mc_non = round(sum_middle_non / len(ProductVectorNon), 2)
    rc_non = round(sum_right_non / len(ProductVectorNon), 2)

    return [lc, mc, rc], [lc_non, mc_non, rc_non]
