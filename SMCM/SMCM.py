from UtilsSMCM import xlsread
from UtilsSMCM import plotSMCM
from TranslationSMCM import membershipfunctionsSMCM
from ManipulationSMCM import SMCMAggregate
from RetranslationSMCM import SMCMSimilarity
import pandas as pd
import numpy as np

if __name__ == "__main__":
    dataFilePath = "C:\\Prashant-Personal-PC\\D\\Research_papers_and_books\\8.8.CWWOther\\Book2.xls"
    A, words = xlsread(dataFilePath)

    #Encoder SMCM
    MFsSMCM = np.zeros((len(words)), dtype=float)
    for i in range(len(words)):
        MFsSMCM[i] = membershipfunctionsSMCM(5, 0, 10, A[i])
    plotSMCM(words, MFsSMCM, "FOUDataPlot.png")

    df1 = pd.DataFrame(np.transpose(words))
    df2 = pd.DataFrame(MFsSMCM)
    df = pd.concat([df1, df2], axis=1)
    df.to_excel(excel_writer="C:\\Prashant-Personal-PC\\D\\Research_papers_and_books\\8.8.CWWOther\\Results\\MFs-SMCM.xlsx")

    #Manipulation SMCM
    Xs = [29, 0, 1]  # [tiny,little, sizeable]
    Ws = [26, 16, 2]  # [small, medium, large]
    YLWASMCM = SMCMAggregate(MFsSMCM[Xs], MFsSMCM[Ws], 5)
    print("YLWA", YLWASMCM)
    tempYLWASMCM = np.array(YLWASMCM)
    tempYLWASMCM = tempYLWASMCM.reshape((1, 1))
    plotSMCM([r'$Y_{LWA}$'], tempYLWASMCM, "YLWAEPCMPlot.png")

    # Retranslation
    S = np.zeros((len(words)), dtype=float)
    for i in range(len(words)):
        S[i] = SMCMSimilarity(YLWASMCM, MFsSMCM[i])

    indices = list()
    for i in range(len(S)):
        if S[i] == 1:
            indices.append(i)
    print(indices)

    decode = list()
    for ele in indices:
        decode.append(words[ele])
    print(decode)

    df1 = pd.DataFrame(['YLWASMCM'])
    df2 = pd.DataFrame([YLWASMCM])
    df3 = pd.DataFrame(['Indices'])
    df4 = pd.DataFrame([indices])
    df5 = pd.DataFrame(['Linguistic'])
    df6 = pd.DataFrame([decode])
    df = pd.concat([df1, df2, df3, df4, df5, df6], axis=1)
    df.to_excel(excel_writer="C:\\Prashant-Personal-PC\\D\\Research_papers_and_books\\8.8.CWWOther\\Results\\test1.xlsx")