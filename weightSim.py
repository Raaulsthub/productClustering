import pandas as pd 
import numpy as np
from sklearn import cluster
import stringdist as sd

# Calculates WeightSimilarity between two products description strings
def productSimilarity(prod1, prod2):
    # similarity starts at zero
    sim = 0
    # separating terms of a string
    prod1List = prod1.split(' ')
    prod2List = prod2.split(' ')
    # tests if the first terms(most important) are equal
    if (prod1List[0] == prod2List[0]):
        sim+=1.5
    # tests if both first terms have length greater than 3 (avoids levenshtein and LCS inconsistency)
    elif (min(len(prod1List[0]), len(prod2List[0])) >= 3):
        # tests if there is a big levenshtein similarity between the first terms
        if ((1 - (sd.levenshtein(prod1List[0], prod2List[0])) / min(len(prod1List[0]), len(prod2List[0]))) > 0.8):
            sim += 1.25
        # tests if there is a big Longuest Common Subsequence similarity between the first terms
        elif ((lcs(prod1List[0], prod2List[0]) / min(len(prod1List[0]), len(prod2List[0]))) > 0.8):
            sim += 1.25
    # pops the first terms out of the product and sends the remaining terms to a less important similarity evaluation (smaller weights)
    sim += bigSimilarSusbtring(prod1List.pop(0), prod2List.pop(0))
    return sim


# Calculates average similarity between a product and a cluster
def clusterSimilarity(cluster, product):
    similarity = 0
    for i in cluster:
        if str(i) != 'nan':
            similarity += productSimilarity(i, product)
    return similarity/len(cluster)

# Less significative similarity evaluation (smaller weights)
def bigSimilarSusbtring(prod1List, prod2List):
    sim = 0
    for i in (prod1List):
        for j in (prod2List):
            if (i == j):
                if (len(i) > 5):
                    sim += 0.25
                else:
                    sim += 0.1
            elif (min(len(i), len(j)) > 5):
                if ((1 - (sd.levenshtein(i, j)) / max(len(i), len(j))) > 0.8):
                    sim += 0.15
                elif ((lcs(i, j) / max(len(i), len(j))) > 0.8):
                    sim += 0.15
    return sim


# Longest Common Subsequence Function (When doing the script ai wasn't able to find a lib with it, so i just copied into the script)
def lcs(X, Y):
    # find the length of the strings
    m = len(X)
    n = len(Y)

    # declaring the array for storing the dp values
    L = [[None] * (n + 1) for i in range(m + 1)]

    """Following steps build L[m + 1][n + 1] in bottom up fashion
    Note: L[i][j] contains length of LCS of X[0..i-1]
    and Y[0..j-1]"""
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif X[i - 1] == Y[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])

    # L[m][n] contains the length of LCS of X[0..n-1] & Y[0..m-1]
    return L[m][n]
# end of function lcs