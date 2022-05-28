from math import prod
import pandas as pd 
import numpy as np
from sklearn import cluster
import stringdist as sd
import functions

def productSimilarity(prod1, prod2):
    sim = 0
    prod1List = prod1.split(' ')
    prod2List = prod2.split(' ')
    if (prod1List[0] == prod2List[0]):
        sim+=1
    elif ((1 - (sd.levenshtein(prod1List[0], prod2List[0])) / max(len(prod1List[0]), len(prod2List[0]))) > 0.8):
        sim += 0.90
    elif ((functions.lcs(prod1List[0], prod2List[0]) / max(len(prod1List[0]), len(prod2List[0]))) > 0.8):
        sim += 0.90
    sim += functions.bigSimilarSusbtring(prod1List.pop(0), prod2List.pop(0))
    return sim

def clusterSimilarity(cluster, product):
    similarity = 0
    for i in cluster:
        if str(i) != 'nan':
            similarity += productSimilarity(i, product)
    return similarity/len(cluster)

clusterDf = pd.read_csv("clusters.csv")
#clusterDf.ex
print(clusterDf.head(10))

product = input(str("DIGITE O NOME DO PRODUTO: "))

similarCluster = 0
similarity = 0

for column in clusterDf.transpose().values.tolist():
    current = clusterSimilarity(column, product)
    if current > similarity:
        similarCluster = column
        similarity = current

print(similarCluster)

#print(f"'BATATA BRANCA', 'BATATA BRANCA GRANEL' - {productSimilarity('BATATA BRANCA', 'BATATA BRANCA GRANEL')}")
#print(f"'BATATA ROSADA CRFO K', 'BATATA BRANCA' = {productSimilarity('BATATA ROSADA CRFO K', 'BATATA BRANCA')} ")
#print(f"'CENOURA EMB KG', 'BATATA ROSADA CRFO K' - {productSimilarity('CENOURA EMB KG', 'BATATA ROSADA CRFO K')}")
