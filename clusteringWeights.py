import numpy as np
from sqlalchemy import null
import weightSImilarity as ws
import pandas as pd

def cluster(productList):
    clusters = []
    for product in productList:
        if not clusters:
            clusters.append([product])
        mostSimilar = null
        similarity = 0
        for cluster in clusters:
            if (ws.clusterSimilarity(cluster, product) > similarity):
                mostSimilar = cluster
                similarity = ws.clusterSimilarity(cluster, product)

        if similarity < 1.25:
            clusters.append([product])
        else:
            mostSimilar.append(product)

        productList.remove(product)

    return clusters
        

df = pd.read_csv("products.csv")
df = df.iloc[:, [0]]
df.dropna(inplace=True)
print(df.head())
productList = df.values.tolist()

productList2 = []
for value in productList:
    for item in value:
        productList2.append(item)


clusters = cluster(productList2)

for a in clusters:
    print(a, end="\n\n")


    



