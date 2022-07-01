import term_weight_clustering as twc
import term_weight_similarity as tws
import pandas as pd

df = pd.read_csv("products.csv")
df = df.iloc[:, [0]]
df.dropna(inplace=True)
print(df.head())
productList = df.values.tolist()

productList2 = []
for value in productList:
    for item in value:
        productList2.append(item)


clusters = twc.clusterize(productList2)

for a in clusters:
    for b in a:
        print(b, end='\n')
    print('\n\n\n\n')

s1 = 'PAO ITALIANO KG'
s2 = 'OLEO DE SOJA LEVE 900ML'
sim = tws.tws_similarity(s1, s2)
print(f"Similarity between {s1} and {s2} : {sim}")