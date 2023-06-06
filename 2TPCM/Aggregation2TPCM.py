import numpy as np


def TPCMAggregate(X, W, partitions):

    numerator = 0
    denominator = 0

    for i in range(len(X)):
        numerator = numerator+(X[i]*W[i])
        denominator = denominator+W[i]

    beta = numerator/denominator

    return beta

