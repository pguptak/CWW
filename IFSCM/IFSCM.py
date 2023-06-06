from UtilsIFSCM import xlsread
from TranslationIFSCM import membershipfunctionsIFSCM
from UtilsIFSCM import plotIFSCM
from ManipulationIFSCM import IFSCMAggregate
from RetranslationIFSCM import IFSCMSimilarity
import pandas as pd
import numpy as np

if __name__ == "__main__":
    dataFilePath = "C:\\Prashant-Personal-PC\\D\\Research_papers_and_books\\8.8.CWWOther\\Book2.xls"
    A, words = xlsread(dataFilePath)

    #Translation AEPCM
    CentroidsIFSCM = np.zeros((len(words)), dtype=float)
    MFsIFSCM = np.zeros((len(words), 3), dtype=float)
    NonMFsIFSCM = np.zeros((len(words), 3), dtype=float)
    for i in range(len(words)):
        MFsIFSCM[i, :], CentroidsIFSCM[i], NonMFsIFSCM[i, :] = membershipfunctionsIFSCM(5, 0, 10, A[i])

    plotIFSCM(words, MFsIFSCM, NonMFsIFSCM, "FOUDataPlot.png")
    #plotNonIFSCM(words, NonMFsIFSCM, "FOUDataPlot.png")

    df1 = pd.DataFrame(np.transpose(words))
    df2 = pd.DataFrame(MFsIFSCM)
    df = pd.concat([df1, df2], axis=1)
    df.to_excel(excel_writer="C:\\Prashant-Personal-PC\\D\\Research_papers_and_books\\8.8.CWWOther\\Results\\MFs-IFSCM.xlsx")

    df1 = pd.DataFrame(np.transpose(words))
    df2 = pd.DataFrame(NonMFsIFSCM)
    df = pd.concat([df1, df2], axis=1)
    df.to_excel(excel_writer="C:\\Prashant-Personal-PC\\D\\Research_papers_and_books\\8.8.CWWOther\\Results\\NonMFs-IFSCM.xlsx")

    # Manipulation AEPCM
    Xs = [29, 0, 1]  # [tiny,little, sizeable]
    Ws = [26, 16, 2]  # [small, medium, large]
    YLWIFSCM, YLWIFSCMNon = IFSCMAggregate(MFsIFSCM[Xs, :], MFsIFSCM[Ws, :], NonMFsIFSCM[Xs, :], NonMFsIFSCM[Ws, :])
    print("YLWA", YLWIFSCM)
    tempYLWIFSCM = np.array(YLWIFSCM)
    tempYLWIFSCM = tempYLWIFSCM.reshape((1, 3))

    print("YLWANon", YLWIFSCMNon)
    tempYLWIFSCMNon = np.array(YLWIFSCMNon)
    tempYLWIFSCMNon = tempYLWIFSCMNon.reshape((1, 3))

    plotIFSCM([r'$Y_{LWA}$'], tempYLWIFSCM, tempYLWIFSCMNon, "YLWAEPCMPlot.png")

    # Retranslation
    S = np.zeros((len(words)), dtype=float)
    SNon = np.zeros((len(words)), dtype=float)

    for i in range(len(words)):
        S[i], SNon[i] = IFSCMSimilarity(YLWIFSCM, MFsIFSCM[i, :], YLWIFSCMNon, NonMFsIFSCM[i, :])

    indices = list()
    indicesNon = list()

    for i in range(len(S)):
        if S[i] == S.min():
            indices.append(i)
        if SNon[i] == SNon.min():
            indicesNon.append(i)
    print(indices)
    print(indicesNon)

    decode = list()
    decodeNon = list()

    for ele in indices:
        decode.append(words[ele])

    for ele in indicesNon:
        decodeNon.append(words[ele])

    print(decode)
    print(decodeNon)

    df1 = pd.DataFrame(['YLWIFSCM'])
    df2 = pd.DataFrame(YLWIFSCM)
    df3 = pd.DataFrame(['Indices'])
    df4 = pd.DataFrame([indices])
    df5 = pd.DataFrame(['Linguistic'])
    df6 = pd.DataFrame([decode])
    df7 = pd.DataFrame(['YLWIFSCMNON'])
    df8 = pd.DataFrame(YLWIFSCMNon)
    df9 = pd.DataFrame(['IndicesNon'])
    df10 = pd.DataFrame([indicesNon])
    df11 = pd.DataFrame(['LinguisticNon'])
    df12 = pd.DataFrame([decodeNon])
    df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12], axis=1)

    df.to_excel(excel_writer="C:\\Prashant-Personal-PC\\D\\Research_papers_and_books\\8.8.CWWOther\\Results\\test1.xlsx")
