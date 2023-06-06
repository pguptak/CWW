
import numpy as np
from Utils import xlsread
from Utils import centroidIT2
from Utils import plotIT2
from EncoderIA import IA
from EncoderEIA import EIA
from EncoderHMA import HMA
from CWWEngine import LWA
from Decoder import Jaccard
import pandas as pd

if __name__ == "__main__":
    dataFilePath = "C:\\Prashant-Personal-PC\\D\\Research_papers_and_books\\8.8.CWWOther\\DATACOPY.xls"
    # Encoder of PerC
    A, words = xlsread(dataFilePath)
    row, col = A.shape
    MFs = np.zeros((int(col / 2), 9), dtype=float)
    nums = [None] * int(col / 2)
    C = np.zeros((int(col / 2), 3), dtype=float)
    for i in range(int(col / 2)):
        L = A[:, 2 * i]
        R = A[:, 2 * i + 1]
        MFs[i, :], nums[i] = HMA(L, R)
        C[i, :] = centroidIT2(MFs[i, :])

    df1 = pd.DataFrame(np.transpose(words))
    df2 = pd.DataFrame(MFs)
    df = pd.concat([df1, df2], axis=1)
    df.to_excel(excel_writer="C:\\Prashant-Personal-PC\\D\\Research_papers_and_books\\8.8.CWWOther\\Results\\test.xlsx")

    # Plot the MFs
    plotIT2(words, MFs, "FOUDataPlot.png")

    #CWW Engine
    Xs = [29, 0, 1]  # [tiny,little, sizeable]
    Ws = [26, 16, 2]  # [small, medium, large]
    YLWA, _, _, _, _ = LWA(MFs[Xs, :], MFs[Ws, :], 21)
    print("YLWA", YLWA)
    tempYLWA = np.array(YLWA)
    tempYLWA = tempYLWA.reshape((1, 9))
    plotIT2([r'$\tilde{Y}_{LWA}$'], tempYLWA, "CWWPlot.png")

    #Decoder
    S = np.zeros(int(col / 2), dtype=float)
    for i in range(int(col / 2)):
        S[i] = Jaccard(YLWA, MFs[i, :])

    index = np.argmax(S)
    maxS = np.max(S)
    decode = words[index]  # decoding
    print("MaxS:", maxS, " Decode:", decode)

    df1 = pd.DataFrame(['YLWA'])
    df2 = pd.DataFrame(YLWA)
    df3 = pd.DataFrame(['MaxS:'])
    df4 = pd.DataFrame([maxS])
    df5 = pd.DataFrame(['Decode:'])
    df6 = pd.DataFrame([decode])
    df = pd.concat([df1, df2, df3, df4, df5, df6], axis=1)
    df.to_excel(excel_writer="C:\\Prashant-Personal-PC\\D\\Research_papers_and_books\\8.8.CWWOther\\Results\\test1.xlsx")


