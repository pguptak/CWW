import numpy as np


def membershipfunctionsAEPCM(partitions, left, right, A):
    partitions = partitions
    left = left
    right = right
    A = A
    Centroidspartitions = list()
    MFlinguistictermorweight = np.zeros((1, 3), dtype=float)
    temp = list()

    # Calculating centroids
    x = (right - left) / (partitions - 1)
    for i in range(partitions):
        Centroidspartitions.append(left + (i * x))

    for i in range(len(Centroidspartitions)):
        temp.append((A - Centroidspartitions[i]) * (A - Centroidspartitions[i]))
    minindex = temp.index(min(temp))
    if minindex == 0:
        MFlinguistictermorweight = [left, left, (minindex + 1) * x]
    elif minindex == partitions-1:
        MFlinguistictermorweight = [(minindex - 1) * x, right, right]
    else:
        MFlinguistictermorweight = [(minindex - 1) * x, minindex * x, (minindex + 1) * x]

    return MFlinguistictermorweight, MFlinguistictermorweight[1]