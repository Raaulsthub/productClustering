import pandas as pd
import stringdist as sd
import term_weight_similarity as tws


# manually writen clusters
clusterDf = pd.read_csv("clusters.csv")
# clusterDf.ex
print(clusterDf.head(10))

product = input(str("DIGITE O NOME DO PRODUTO: "))
print(product)

similarCluster = 0
similarity = 0

for column in clusterDf.transpose().values.tolist():
    current = tws.cluster_similarity(column, product)
    if current > similarity:
        similarCluster = column
        similarity = current

print(similarCluster)

print(f"'BATATA BRANCA', 'BATATA BRANCA GRANEL' - {tws.tws_similarity('BATATA BRANCA', 'BATATA BRANCA GRANEL')}")
print(f"'BATATA ROSADA CRFO K', 'BATATA BRANCA' - {tws.tws_similarity('BATATA ROSADA CRFO K', 'BATATA BRANCA')} ")
print(f"'CENOURA EMB KG', 'BATATA ROSADA CRFO K' - {tws.tws_similarity('CENOURA EMB KG', 'BATATA ROSADA CRFO K')}")
