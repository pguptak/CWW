import numpy as np


def SMCMAggregate(X, W, partitions):
    smcmup = np.zeros((len(X)), dtype=float)
    smcmwt = np.zeros((len(W)), dtype=float)
    Wnew = np.zeros((len(W)), dtype=float)

    for i in range(len(X)):
        smcmup[i] = X[i]+1
    for i in range(len(W)):
        smcmwt[i] = W[i]+1

    sumvar = 0
    for i in range(len(smcmwt)):
        sumvar = sumvar+smcmwt[i]
    for i in range(len(W)):
        Wnew[i] = smcmwt[i]/sumvar

    smcmupsort = sorted(smcmup, reverse=True)
    Wnewsort = sorted(Wnew, reverse=True)
    ind = smcm_recursion(smcmupsort, Wnewsort, partitions)
    return ind-1

def smcm_recursion(up, wt, g):
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
        ind1 = smcm_recursion(upnew, wtnew, g)
        upnew1 = []
        wtnew1 = []
        wtnew1.append(wtnew[0])
        wtnew1.append(1 - wtnew[0])
        upnew1.append(up[0])
        upnew1.append(ind1)
        ind = smcm_recursion(upnew1, wtnew1, g)
    return ind
