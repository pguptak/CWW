
def membershipfunctionsSMCM(partitions, left, right, A):
    partitions = partitions
    left = left
    right = right
    A = A

    Centroidspartitions = list()

    temp = list()
    # Calculating centroids
    x = (right - left) / (partitions - 1)
    for i in range(partitions):
        Centroidspartitions.append(left + (i * x))

    for i in range(len(Centroidspartitions)):
        temp.append((A - Centroidspartitions[i]) * (A - Centroidspartitions[i]))
    minindex = temp.index(min(temp))

    Linguistictermindex = minindex

    return Linguistictermindex