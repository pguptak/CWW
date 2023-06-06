import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt


def xlsread(path):
    dataframe = pd.read_excel(path)
    cn = dataframe.columns
    wordList = list()
    for i in range(0, len(cn), 2):
        wordList.append(cn[i])
    Arr = np.asarray(dataframe)
    return Arr, wordList


def EKM(xPoint, wLower, wUpper, maxFlag):
    if np.max(wUpper) == 0.0 or np.max(xPoint) == 0.0:
        y = 0.0
        return y
    if np.max(wLower) == 0.0:
        if maxFlag > 0:
            y = np.max(xPoint)
        else:
            y = np.min(xPoint)
        return y
    if xPoint.shape[0] == 1:
        y = xPoint
        return y
    # combine zero firing intervals
    for iLoop in range(wUpper.shape[0] - 1, -1, -1):
        if wUpper[iLoop] == 0.0:
            xPoint = np.delete(xPoint, iLoop)
            wLower = np.delete(wLower, iLoop)
            wUpper = np.delete(wUpper, iLoop)
    xIndex = np.argsort(xPoint)
    xSort = np.array(sorted(xPoint))
    lowerSort = wLower[xIndex]
    upperSort = wUpper[xIndex]

    l = list()
    for p in range(xSort.shape[0] - 1, -1, -1):
        if xSort[p] == 0.0:
            l.append(p)

    l = np.array(l)
    if l.shape[0] == 0:
        k = 0
    else:
        k = l[0]

    if k > 0:
        xSort[0] = 0
        lowerSort[0] = np.sum(lowerSort[0:k])
        upperSort[0] = np.sum(upperSort[0:k])
        for p in range(1, k):
            xSort = np.delete(xSort, p)

        for p in range(1, k):
            lowerSort = np.delete(lowerSort, p)

        for p in range(1, k):
            upperSort = np.delete(upperSort, p)

    ly = xSort.shape[0]

    if maxFlag < 0:
        k = round(ly / 2.4)
        temp = np.hstack((upperSort[0:k], lowerSort[k:ly + 1]))
    else:
        k = round(ly / 1.7)
        temp = np.hstack((lowerSort[0:k], upperSort[k:ly + 1]))

    ######################################33
    a = np.dot(temp, xSort)
    b = np.sum(temp)
    y = float(a) / float(b)

    l = list()
    for p in range(xSort.shape[0]):
        if xSort[p] > y:
            l.append(p)

    l = np.array(l)

    if l.shape[0] == 0:
        kNew = -1
    else:
        kNew = l[0] - 1

    k = k - 1

    while k != kNew and kNew != -1:
        mink = min(k, kNew)
        maxk = max(k, kNew)
        temp = upperSort[mink + 1:maxk + 1] - lowerSort[mink + 1:maxk + 1]  # mink+1:maxk+2
        b = b - float(np.sign(kNew - k)) * np.sign(maxFlag) * np.sum(temp)
        a = a - float(np.sign(kNew - k)) * np.sign(maxFlag) * np.dot(temp, xSort[mink + 1:maxk + 1])
        y = float(a) / float(b)
        k = kNew
        l = list()
        for p in range(xSort.shape[0]):
            if xSort[p] > y:
                l.append(p)

        l = np.array(l)
        if l.shape[0] == 0:
            kNew = -1

        else:
            kNew = l[0] - 1

    return y


def mg(x, xMF, uMF):
    if len(xMF) != len(uMF):
        raise Exception('xMF and uMF must have the same length.')

    index = np.argsort(xMF)
    xMF.sort()

    uMF = uMF[index]

    u = np.zeros(x.shape[0])

    for i in range(x.shape[0]):
        if x[i] <= xMF[0] or x[i] >= xMF[-1]:
            u[i] = 0
        else:
            l = list()
            for j in range(xMF.shape[0]):
                if xMF[j] < x[i]:
                    l.append(j)

            if len(l) == 0:
                left = 0
            else:
                left = l[-1]

            right = left + 1
            u[i] = uMF[left] + float(uMF[right] - uMF[left]) * (x[i] - xMF[left]) / float(xMF[right] - xMF[left])
    return u


def centroidIT2(MF):
    if MF.shape[0] != 9:
        raise Exception('The input vector must be a 9-point representation of an IT2 FS.')

    Xs = np.linspace(MF[0], MF[3], 100)
    UMF = mg(Xs, MF[0:4], np.array([0.0, 1.0, 1.0, 0.0]))
    LMF = mg(Xs, MF[4:8], np.array([0.0, float(MF[8]), float(MF[8]), 0.0]))
    Cl = EKM(Xs, LMF, UMF, -1)
    Cr = EKM(Xs, LMF, UMF, 1)
    Cavg = float(Cl + Cr) / 2.0
    return Cl, Cr, Cavg


def findIT2PlotPoint(**kwargs):
    # xUMF,uUMF,xLMF,uLMF,domain
    # actualArg=['xUMF','uUMF','xLMF','uLMF','domain']
    tempArg = list()
    tempValue = list()
    for key, value in kwargs.items():
        tempArg.append(key)
        tempValue.append(np.array(value))

    for t in tempArg:
        if (t[0] != 'xUMF' or t[1] != 'uUMF' or t[2] != 'uLMF' or t[3] != 'domain') and len(tempArg) == 4:
            raise Exception('The number of inputs must be 1, 2, 4 or 5.')
        if len(tempArg) > 2:
            if len(t[0]) != len(t[1]):
                raise Exception('xUMF and uUMF must have the same length.')
            if len(t[2]) != len(t[3]):
                raise Exception('xLMF and uLMF must have the same length.')
            if len(tempArg) == 4:
                domain = [min(tempValue[0]), max(tempValue[0])]
        elif len(tempArg) == 1:
            A = tempValue[0]
            domain = np.array([A[0], A[3]])
            xUMF = np.linspace(domain[0], domain[1], 100)
            xLMF = xUMF
            uUMF = mg(xUMF, A[0:4], np.array([0.0, 1.0, 1.0, 0.0]))
            uLMF = mg(xLMF, A[4:8], np.array([0.0, A[8], A[8], 0.0]))
        elif len(tempArg) == 2:
            A = tempValue[0]
            domain = tempValue[1]
            xUMF = np.linspace(domain[0], domain[1], 100)
            xLMF = xUMF
            uUMF = mg(xUMF, A[0:4], np.array([0.0, 1.0, 1.0, 0.0]))
            uLMF = mg(xLMF, A[4:8], np.array([0.0, A[8], A[8], 0.0]))

    return xUMF, uUMF, xLMF, uLMF

def plotIT2(words, MF, fileName):
    fig = plt.figure(random.randint(1, 100))
    plt.rcParams["font.family"] = 'times new roman'
    plt.rcParams["font.weight"] = 'bold'
    plt.rcParams['axes.titlepad'] = 0
    plt.rcParams['axes.titlesize'] = 12
    # plt.rcParams['axes.labelsize']= 'x-large'
    #plt.rcParams['text.latex.unicode'] = True
    subPlotSize = findsubPlotGrid(len(words))
    for i in range(len(words)):
        ax = plt.subplot(subPlotSize[1], subPlotSize[0], i + 1)
        xUMF, uUMF, xLMF, uLMF = findIT2PlotPoint(xUMF=MF[i, :])
        ax.fill(xUMF, uUMF, 'grey', xLMF, uLMF, 'w', alpha=1.0)
        ax.plot(xUMF, uUMF, linestyle="--", color="blue")
        ax.plot(xLMF, uLMF, linestyle="--", color="blue")
        ax.set(title=words[i])
        ax.set_xticks([0, 2.5, 5.0, 7.5, 10])
        ax.set_yticks([0, 1])

    plt.xticks([0, 2.5, 5.0, 7.5, 10])
    plt.yticks([0, 1])
    plt.axis([0, 10, 0, 1])
    plt.tight_layout(w_pad=0.001, h_pad=0.001)
    plt.show()

    """if fileName.find('.') != -1:
        fileName = fileName + ".png"

    plt.tight_layout()
    plt.savefig(fileName)
    """


def findsubPlotGrid(n):
    tempFaclist = list()
    for i in range(1, int(pow(n, 1 / 2)) + 1):
        if n % i == 0:
            tempFaclist.append([i, n / i])

    tempFaclist = np.array(tempFaclist).astype(int)
    index = np.argmax(np.min(tempFaclist, axis=1))
    return tempFaclist[index]
