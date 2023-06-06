import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt


def xlsread(path):
    dataframe = pd.read_excel(path)
    wordlist = dataframe[dataframe.columns[0]]
    Arr = dataframe[dataframe.columns[1]]
    wordList1 = list()
    Arr1 = list()
    for i in range(0, len(wordlist)):
        wordList1.append(wordlist[i])
    for i in range(0, len(Arr)):
        Arr1.append(Arr[i])
    return Arr1, wordList1


def plotIFSCM(words, MF, NMF, fileName):
    if len(words) == 1:
        fig = plt.figure(random.randint(1, 100))
        plt.rcParams["font.family"] = 'times new roman'
        plt.rcParams["font.weight"] = 'bold'
        plt.rcParams['axes.titlepad'] = 0
        plt.rcParams['axes.titlesize'] = 12
        subPlotSize = findsubPlotGrid(len(words))
        for i in range(len(words)):
            ax = plt.subplot(subPlotSize[1], subPlotSize[0], i + 1)
            xpts1 = [MF[i, 0], MF[i, 1], MF[i, 1], MF[i, 2]]
            ypts1 = [0, 1, 1, 0]
            xpts2 = [NMF[i, 0], NMF[i, 1], NMF[i, 1], NMF[i, 2]]
            ypts2 = [1, 0, 0, 1]
            ax.plot(xpts1, ypts1, linestyle="--", color="blue")
            ax.plot(xpts2, ypts2, linestyle="--", color="black")
            ax.set(title=words[i])
            ax.set_xticks([0, 15, 30, 45, 60])
            ax.set_yticks([0, 1])

        plt.xticks([0, 15, 30, 45, 60])
        plt.yticks([0, 1])
        plt.axis([0, 60, 0, 1])
        plt.tight_layout(w_pad=0.001, h_pad=0.001)
        plt.show()

        """if fileName.find('.') != -1:
            fileName = fileName + ".png"

        plt.tight_layout()
        plt.savefig(fileName)
        """
    else:
        fig = plt.figure(random.randint(1, 100))
        plt.rcParams["font.family"] = 'times new roman'
        plt.rcParams["font.weight"] = 'bold'
        plt.rcParams['axes.titlepad'] = 0
        plt.rcParams['axes.titlesize'] = 12
        subPlotSize = findsubPlotGrid(len(words))
        for i in range(len(words)):
            ax = plt.subplot(subPlotSize[1], subPlotSize[0], i + 1)
            xpts1 = [MF[i, 0], MF[i, 1], MF[i, 1], MF[i, 2]]
            ypts1 = [0, 1, 1, 0]
            xpts2 = [NMF[i, 0], NMF[i, 1], NMF[i, 1], NMF[i, 2]]
            ypts2 = [1, 0, 0, 1]
            ax.plot(xpts1, ypts1, linestyle="--", color="blue")
            ax.plot(xpts2, ypts2, linestyle="--", color="black")
            ax.set(title=words[i])
            ax.set_xticks([0, 2.5, 5.0, 7.5, 10])
            ax.set_yticks([0, 1])

        plt.xticks([0, 0, 2.5, 5.0, 7.5, 10])
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
