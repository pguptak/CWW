import numpy as np


def membershipfunctionsIFSCM(partitions, left, right, A):
    partitions = partitions
    left = left
    right = right
    A = A
    Centroidspartitions = list()
    MFlinguistictermorweight = np.zeros((1, 3), dtype=float)
    NonMFlinguistictermorweight = np.zeros((1, 3), dtype=float)
    MFsall = np.zeros((partitions, 3), dtype=float)

    temp = list()

    # Calculating centroids
    x = (right - left) / (partitions - 1)
    for i in range(partitions):
        Centroidspartitions.append(left + (i * x))

    for i in range(partitions):
        if i == 0:
            MFsall[i, :] = [left, left, i * x]
        elif i == partitions-1:
            MFsall[i, :] = [(i - 1) * x, right, right]
        else:
            MFsall[i, :] = [(i - 1) * x, i * x, (i + 1) * x]

    for i in range(len(Centroidspartitions)):
        temp.append((A - Centroidspartitions[i]) * (A - Centroidspartitions[i]))
    minindex = temp.index(min(temp))

    if minindex == 0:
        MFlinguistictermorweight = [left, left, (minindex + 1) * x]
    elif minindex == partitions-1:
        MFlinguistictermorweight = [(minindex - 1) * x, right, right]
    else:
        MFlinguistictermorweight = [(minindex - 1) * x, minindex * x, (minindex + 1) * x]

    templ = 0
    tempm = 0
    tempr = 0
    for i in range(len(MFsall)):
        if i == minindex:
            continue
        else:
            templ = templ + MFsall[i][0]
            tempm = tempm + MFsall[i][1]
            tempr = tempr + MFsall[i][2]
    NonMFlinguistictermorweight = [templ/(partitions-1), tempm/(partitions-1), tempr/(partitions-1)]

    return MFlinguistictermorweight, MFlinguistictermorweight[1], NonMFlinguistictermorweight