from Utils2TPCM import xlsread
from Utils2TPCM import plot2TPCM
from Utils2TPCM import plot2TPCMbeta
from InformationGathering2TPCM import membershipfunctions2TPCM
from Aggregation2TPCM import TPCMAggregate
from Exploitation2TPCM import TPCMSimilarity
import pandas as pd
import numpy as np

if __name__ == "__main__":
    dataFilePath = "D:\Research_papers_and_books\8.8.CWWOther\Book2.xls"
    A, words = xlsread(dataFilePath)
    Centroids2TPCM = np.zeros((len(words)), dtype=float)
    MFs2TPCM = np.zeros((len(words), 3), dtype=float)
    MFs2TPCMcomp = np.zeros((len(words)), dtype=float)

    #Information gathering   2TPCM
    for i in range(len(words)):
        MFs2TPCM[i, :], Centroids2TPCM[i], MFs2TPCMcomp[i] = membershipfunctions2TPCM(5, 0, 10, A[i])
    plot2TPCM(words, MFs2TPCM, "FOUDataPlot.png")

    df1 = pd.DataFrame(np.transpose(words))
    df2 = pd.DataFrame(MFs2TPCM)
    df = pd.concat([df1, df2], axis=1)
    df.to_excel(excel_writer="D:\Research_papers_and_books\8.8.CWWOther\Results\MFs-2TPCM.xlsx")


    #Aggregation 2TPCM
    Xs = [29, 0, 1]  # [tiny,little, sizeable]
    Ws = [26, 16, 2]  # [small, medium, large]
    YLWA2TPCM = TPCMAggregate(MFs2TPCMcomp[Xs], MFs2TPCMcomp[Ws], 5)
    print("YLWA", YLWA2TPCM)
    tempYLWA2TPCM = np.array(YLWA2TPCM)
    tempYLWA2TPCM = tempYLWA2TPCM.reshape((1, 1))
    plot2TPCMbeta([r'$Y_{LWA}$'], tempYLWA2TPCM, "YLWA2TPCMPlot.png")

    #Exploitation 2TPCM
    beta2TPCM = YLWA2TPCM
    alpha2TPCM = beta2TPCM-round(beta2TPCM)
    S = np.zeros((len(words)), dtype=float)
    for i in range(len(words)):
        S[i] = TPCMSimilarity(round(beta2TPCM), MFs2TPCMcomp[i])

    indices = list()
    for i in range(len(S)):
        if S[i] == 1:
            indices.append(i)
    print(indices)

    decode = list()
    for ele in indices:
        decode.append(words[ele])
    print(decode)

    df1 = pd.DataFrame(['Alpha2TPCM'])
    df2 = pd.DataFrame(alpha2TPCM)
    df3 = pd.DataFrame(['Indices'])
    df4 = pd.DataFrame([indices])
    df5 = pd.DataFrame(['Linguistic'])
    df6 = pd.DataFrame([decode])
    df = pd.concat([df1, df2, df3, df4, df5, df6], axis=1)
    df.to_excel(excel_writer="D:\Research_papers_and_books\8.8.CWWOther\Results\test1.xlsx")
