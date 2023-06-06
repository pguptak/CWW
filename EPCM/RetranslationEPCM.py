import math


def EPCMSimilarity(A, B):
    s1 = 0.2 * pow((A[0] - B[0]), 2)
    s2 = 0.6 * pow((A[1] - B[1]), 2)
    s3 = 0.2 * pow((A[2] - B[2]), 2)
    s = math.sqrt(s1+s2+s3)
    return s