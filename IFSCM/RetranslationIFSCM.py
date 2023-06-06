import math


def IFSCMSimilarity(A, B, ANon, BNon):
    s1 = 0.2 * pow((A[0] - B[0]), 2)
    s2 = 0.6 * pow((A[1] - B[1]), 2)
    s3 = 0.2 * pow((A[2] - B[2]), 2)
    s = math.sqrt(s1+s2+s3)

    s1Non = 0.2 * pow((ANon[0] - BNon[0]), 2)
    s2Non = 0.6 * pow((ANon[1] - BNon[1]), 2)
    s3Non = 0.2 * pow((ANon[2] - BNon[2]), 2)
    sNon = math.sqrt(s1Non+s2Non+s3Non)
    return s, sNon