from UtilsAEPCM import xlsread
from UtilsAEPCM import plotAEPCM
from TranslationAEPCM import membershipfunctionsAEPCM
from ManipulationAEPCM import AEPCMAggregate
from RetranslationAEPCM import AEPCMSimilarity
import pandas as pd
import numpy as np

if __name__ == "__main__":
    dataFilePath = "C:\\Prashant-Personal-PC\\D\\Research_papers_and_books\\8.8.CWWOther\\Book2.xls"
    A, words = xlsread(dataFilePath)
    CentroidsAEPCM = np.zeros((len(words)), dtype=float)
    MFsAEPCM = np.zeros((len(words), 3), dtype=float)

    #Translation AEPCM
    for i in range(len(words)):
        MFsAEPCM[i, :], CentroidsAEPCM[i] = membershipfunctionsAEPCM(5, 0, 10, A[i])
    plotAEPCM(words, MFsAEPCM, "FOUDataPlot.png")

    df1 = pd.DataFrame(np.transpose(words))
    df2 = pd.DataFrame(MFsAEPCM)
    df = pd.concat([df1, df2], axis=1)
    df.to_excel(excel_writer="C:\\Prashant-Personal-PC\\D\\Research_papers_and_books\\8.8.CWWOther\\Results\\MFs-AEPCM.xlsx")


    #Manipulation AEPCM
    Xs = [29, 0, 1]  # [tiny,little, sizeable]
    Ws = [26, 16, 2]  # [small, medium, large]
    YLWAEPCM = AEPCMAggregate(MFsAEPCM[Xs, :], MFsAEPCM[Ws, :])
    print("YLWA", YLWAEPCM)
    tempYLWAEPCM = np.array(YLWAEPCM)
    tempYLWAEPCM = tempYLWAEPCM.reshape((1, 3))
    plotAEPCM([r'$Y_{LWA}$'], tempYLWAEPCM, "YLWAEPCMPlot.png")

    # Retranslation
    S = np.zeros((len(words)), dtype=float)
    for i in range(len(words)):
        S[i] = AEPCMSimilarity(YLWAEPCM, MFsAEPCM[i, :])

    indices = list()
    for i in range(len(S)):
        if S[i] == S.min():
            indices.append(i)
    print(indices)

    decode = list()
    for ele in indices:
        decode.append(words[ele])
    print(decode)

    df1 = pd.DataFrame(['YLWAEPCM'])
    df2 = pd.DataFrame(YLWAEPCM)
    df3 = pd.DataFrame(['Indices'])
    df4 = pd.DataFrame([indices])
    df5 = pd.DataFrame(['Linguistic'])
    df6 = pd.DataFrame([decode])
    df = pd.concat([df1, df2, df3, df4, df5, df6], axis=1)
    df.to_excel(excel_writer="C:\\Prashant-Personal-PC\\D\\Research_papers_and_books\\8.8.CWWOther\\Results\\test1.xlsx")
