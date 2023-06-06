from UtilsEPCM import xlsread
from UtilsEPCM import plotEPCM
from TranslationEPCM import membershipfunctionsEPCM
from ManipulationEPCM import EPCMAggregate
from RetranslationEPCM import EPCMSimilarity
import pandas as pd
import numpy as np

if __name__ == "__main__":
    dataFilePath = "C:\\Prashant-Personal-PC\\D\\Research_papers_and_books\\8.8.CWWOther\\Book2.xls"
    A, words = xlsread(dataFilePath)
    CentroidsEPCM = np.zeros((len(words)), dtype=float)
    MFsEPCM = np.zeros((len(words), 3), dtype=float)

    #Encoder EPCM
    for i in range(len(words)):
        MFsEPCM[i, :], CentroidsEPCM[i] = membershipfunctionsEPCM(5, 0, 10, A[i])
    plotEPCM(words, MFsEPCM, "FOUDataPlot.png")

    df1 = pd.DataFrame(np.transpose(words))
    df2 = pd.DataFrame(MFsEPCM)
    df = pd.concat([df1, df2], axis=1)
    df.to_excel(excel_writer="C:\\Prashant-Personal-PC\\D\\Research_papers_and_books\\8.8.CWWOther\\Results\\MFs-EPCM.xlsx")


    #Manipulation EPCM
    Xs = [29, 0, 1]  # [tiny,little, sizeable]
    YLWAEPCM = EPCMAggregate(MFsEPCM[Xs, :])
    print("YLWA", YLWAEPCM)
    tempYLWAEPCM = np.array(YLWAEPCM)
    tempYLWAEPCM = tempYLWAEPCM.reshape((1, 3))
    plotEPCM([r'$Y_{LWA}$'], tempYLWAEPCM, "YLWAEPCMPlot.png")

    #Retranslation
    S = np.zeros((len(words)), dtype=float)
    for i in range(len(words)):
        S[i] = EPCMSimilarity(YLWAEPCM, MFsEPCM[i, :])

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
