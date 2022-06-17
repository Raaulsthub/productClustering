import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import pandas as pd
import sparse_dot_topn.sparse_dot_topn as ct
from torch import cudnn_is_acceptable
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def cluster(productList, model):
    X = []
    for product in productList:
        X.append(model.value(product))
    X = np.array(X).reshape(-1, 1)
    kmeans = KMeans(n_clusters=100, random_state=1).fit(X)
    y_kmeans = kmeans.fit_predict(X)
    return y_kmeans

# A class for matching one list of strings to another
class StringMatch():
    def __init__(self, source_names, target_names):
        self.source_names = source_names
        self.target_names = target_names
        self.ct_vect      = None
        self.tfidf_vect   = None
        self.vocab        = None
        
    def tokenize(self, analyzer='char_wb', n=3):
        # Create initial count vectorizer & fit it on both lists to get vocab
        self.ct_vect = CountVectorizer(analyzer=analyzer, ngram_range=(n, n))
        self.vocab   = self.ct_vect.fit(self.source_names + self.target_names).vocabulary_
        
        # Create tf-idf vectorizer
        self.tfidf_vect  = TfidfVectorizer(vocabulary=self.vocab, analyzer=analyzer, ngram_range=(n, n))
        
    def _awesome_cossim_top(self, w, ntop=1, lower_bound=0):
        self.source_names = [w]
        self.tokenize()
        A = self.tfidf_vect.fit_transform(self.source_names).tocsr()
        B = self.tfidf_vect.fit_transform(self.target_names).transpose().tocsr()
        
        M, _ = A.shape
        _, N = B.shape

        idx_dtype = np.int32

        nnz_max = M * ntop

        indptr = np.zeros(M+1, dtype=idx_dtype)
        indices = np.zeros(nnz_max, dtype=idx_dtype)
        data = np.zeros(nnz_max, dtype=A.dtype)

        ct.sparse_dot_topn(
            M, N, np.asarray(A.indptr, dtype=idx_dtype),
            np.asarray(A.indices, dtype=idx_dtype),
            A.data,
            np.asarray(B.indptr, dtype=idx_dtype),
            np.asarray(B.indices, dtype=idx_dtype),
            B.data,
            ntop,
            lower_bound,
            indptr, indices, data)

        return data[0]
    
    def compare(self, w1, w2):
        value1 = self._awesome_cossim_top(w1)
        value2 = self._awesome_cossim_top(w2)
        mse = np.square(np.subtract(value1, value2)).mean()
        return mse
        
    def value(self, w):
        return self._awesome_cossim_top(w)
      
df = pd.read_csv("products.csv")
df = df.iloc[:, [0]]
df.dropna(inplace=True)
productList = df.values.tolist()

productList2 = []
for value in productList:
    for item in value:
        productList2.append(item)

model = StringMatch(productList2, productList2)

y_kmeans = cluster(productList2, model)
for i, product in enumerate(productList2):
    print('Product:', product, 'Cluster:', y_kmeans[i])
