#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scipy.cluster.hierarchy import linkage, fcluster
from sklearn.metrics import silhouette_score
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("cbe_matrix14s.csv", index_col=0)
df = df.div(df.sum(axis=1), axis=0)

Z = linkage(df, method='single', metric='cosine')

dfscore = pd.DataFrame({"nclust": range(2,1011)})
silscores = []
for n in dfscore['nclust']:
    labels = fcluster(Z, n, criterion="maxclust")
    sil = silhouette_score(df,labels, metric="cosine")
    silscores.append(sil)
dfscore['SIL'] = silscores

plt.plot(dfscore['nclust'],dfscore['SIL'])
plt.xticks(np.arange(0, dfscore['nclust'].iloc[-1], 100))
plt.yticks(np.arange(0, 0.5, 0.05))
plt.xlabel("Number of clusters")
plt.ylabel("Silhouette coefficient")
plt.grid()
plt.savefig("silhouette.png", dpi=600)