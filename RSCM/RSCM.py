from UtilsRSCM import xlsread
from UtilsRSCM import plotRSCM
from TranslationRSCM import membershipfunctionsRSCM
from ManipulationRSCM import RSCMAggregate
from RetranslationRSCM import RSCMSimilarity
import pandas as pd
import numpy as np

if __name__ == "__main__":
    dataFilePath = "D:\Research_papers_and_books\8.8.CWWOther\Book2.xls"
    A, words = xlsread(dataFilePath)

    #Encoder RSCM
    MFsRSCM = np.zeros((len(words)), dtype=float)
    for i in range(len(words)):
        MFsRSCM[i] = membershipfunctionsRSCM(5, 0, 10, A[i])
    plotRSCM(words, MFsRSCM, "FOUDataPlot.png")

    df1 = pd.DataFrame(np.transpose(words))
    df2 = pd.DataFrame(MFsRSCM)
    df = pd.concat([df1, df2], axis=1)
    df.to_excel(excel_writer="D:\Research_papers_and_books\8.8.CWWOther\Results\MFs-RSCM.xlsx")

    #Manipulation RSCM
    Xs = [29, 0, 1]  # [tiny,little, sizeable]
    YLWARSCM = RSCMAggregate(MFsRSCM[Xs], 5)
    print("YLWA", YLWARSCM)
    tempYLWARSCM = np.array(YLWARSCM)
    tempYLWARSCM = tempYLWARSCM.reshape((1, 1))
    plotRSCM([r'$Y_{LWA}$'], tempYLWARSCM, "YLWAEPCMPlot.png")

    # Retranslation RSCM
    S = np.zeros((len(words)), dtype=float)
    for i in range(len(words)):
        S[i] = RSCMSimilarity(YLWARSCM, MFsRSCM[i])

    indices = list()
    for i in range(len(S)):
        if S[i] == 1:
            indices.append(i)
    print(indices)

    decode = list()
    for ele in indices:
        decode.append(words[ele])
    print(decode)

    df1 = pd.DataFrame(['YLWARSCM'])
    df2 = pd.DataFrame([YLWARSCM])
    df3 = pd.DataFrame(['Indices'])
    df4 = pd.DataFrame([indices])
    df5 = pd.DataFrame(['Linguistic'])
    df6 = pd.DataFrame([decode])
    df = pd.concat([df1, df2, df3, df4, df5, df6], axis=1)
    df.to_excel(excel_writer="D:\Research_papers_and_books\8.8.CWWOther\Results\test1.xlsx")