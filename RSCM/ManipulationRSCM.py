import numpy as np


def RSCMAggregate(X, partitions):
    rscmup = np.zeros((len(X)), dtype=float)
    for i in range(len(X)):
        rscmup[i] = X[i] + 1

    rscmwt = [0] * len(rscmup)
    clases1 = []
    for j in rscmup:
        if j not in clases1:
            clases1.append(j)
    noclases = len(clases1)

    for j in range(len(clases1)):
        ele = clases1[j]
        count = 0
        for k in range(len(rscmup)):
            if ele == rscmup[k]:
                count = count + 1
        if count != 0:
            wt = 1 / (noclases * count)
            for k in range(len(rscmup)):
                if ele == rscmup[k]:
                    rscmwt[k] = wt
        else:
            wt = 1 / noclases
            for k in range(len(rscmup)):
                if ele == rscmup[k]:
                    rscmwt[k] = wt

    #Wnew = np.zeros((len(rscmwt)), dtype=float)

    rscmupsort = sorted(rscmup, reverse=True)
    Wnewsort = sorted(rscmwt, reverse=True)
    ind = rscm_recursion(rscmupsort, Wnewsort, partitions)
    return ind-1

def rscm_recursion(up, wt, g):
    if len((up)) == 2:
        ind = min(g, up[1] + round((((wt[0] - wt[1] + 1) / 2) * (up[0] - up[1]))))
    else:
        sumvar = 0
        wtnew = []
        upnew = []
        for i in range(1, len(wt)):
            sumvar = sumvar + wt[i]
        for i in range(1, len(wt)):
            wtnew.append((wt[i]) / sumvar)
        for i in range(1, len(up)):
            upnew.append(up[i])
        ind1 = rscm_recursion(upnew, wtnew, g)
        upnew1 = []
        wtnew1 = []
        wtnew1.append(wtnew[0])
        wtnew1.append(1 - wtnew[0])
        upnew1.append(up[0])
        upnew1.append(ind1)
        ind = rscm_recursion(upnew1, wtnew1, g)
    return ind
