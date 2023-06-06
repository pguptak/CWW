import numpy as np


def membershipfunctions2TPCM(partitions, left, right, A):
    partitions = partitions
    left = left
    right = right
    A = A

    Centroidspartitions = list()
    MFlinguisticterm = np.zeros((1, 9), dtype=float)
    temp = list()

    # Calculating centroids
    x = (right - left) / (partitions - 1)
    for i in range(partitions):
        Centroidspartitions.append(left + (i * x))

    for i in range(len(Centroidspartitions)):
        temp.append((A - Centroidspartitions[i]) * (A - Centroidspartitions[i]))
    minindex = temp.index(min(temp))
    Linguistictermindex = minindex
    if minindex == 0:
        MFlinguisticterm = [left, left, (minindex+1)*x]
    elif minindex == partitions-1:
        MFlinguisticterm = [(minindex-1)*x, right, right]
    else:
        MFlinguisticterm = [(minindex-1)*x, minindex*x, (minindex+1)*x]

    return MFlinguisticterm, MFlinguisticterm[1], Linguistictermindex
