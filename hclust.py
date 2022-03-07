#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from scipy.cluster.hierarchy import linkage, dendrogram, cut_tree, set_link_color_palette
import pylab
import csv

# returns scene id from index
def to_ind(names, x):
  if x < len(names):
    return names[int(x)]
  else:
    return "_"

# returns the cluster that contains a given scene at a given step
def get_cluster_from_scene(cdf, scene, step):
  clid = cdf.at[scene, step] # cluster id 
  clist = cdf[cdf[step] == clid].index.to_list()
  return clist

# add a scene to a given cluster and returns the new cluster with i+1 scenes
def add_scene_to_cluster(cdf, scene_list, start_step):
  clsize = len(scene_list)
  step = start_step
  while step < len(cdf.columns):
    cl = get_cluster_from_scene(cdf, scene_list[0],step)
    if len(cl) > clsize:
      return (step, cl)
    step += 1
  return (-1,scene_list)

# return the new cluster of 2 elements created at the specified step. Or an empty list
def get_new_cluster(cdf, step):
  for el in range(1,len(cdf)):
    col1 = cdf[cdf[step] == el]
    if len(col1.index) == 0:
      return []
    if len(col1.index) != 2:
      continue
    col0 = cdf[cdf[step-1] == el]
    if len(col1) != len(col0):
      return col1.index.to_list()

#return the new cluster of 2 elements created at the specified index of linkage matrix. Or an empty list
def get_new_cluster2(Zdf, ind):
  if ind >= len(Zdf):
    return []
  x = Zdf.iloc[ind][[4,5]]
  if x[4] == "_" or x[5] == "_":
    return get_new_cluster2(Zdf, ind+1)
  return [x[4],x[5]]

# check if a list of scenes is contained in a cluster array
def clusters_contain(clusters, scene_list):
  for el in clusters:
    vals = list(el.values())
    if vals[0] == scene_list:
      return True
  return False


# LOAD DATASET
df = pd.read_csv("cbe_matrix14s.csv", index_col=0)
ds = df.to_numpy()

# CREATE LINKAGE MATRIX
Z = linkage(ds, method='single', metric='cosine', optimal_ordering=False)
Zdf = pd.DataFrame(Z)
Zdf.sort_values(by=[2], inplace=True)
names = df.index.to_list()
Zdf[4] = Zdf[0].apply(lambda x: to_ind(names, x))
Zdf[5] = Zdf[1].apply(lambda x: to_ind(names, x))

# CREATE DENDROGRAM
set_link_color_palette(None)
fig = pylab.figure(figsize=(80,500))

def llf(id):
    return df.index[id]

dendro = dendrogram(Z,  leaf_label_func=llf, leaf_rotation=0, leaf_font_size =12, orientation = 'right')
fig.savefig('dendro.png')

# WRITE CDF MATRIX
cdf = pd.DataFrame(cut_tree(Z), index=df.index)
cdf.to_csv("cdf.csv")

# CREATE CLUSTER CHAINS
clusters = []
for i in range(0,len(Zdf.index)):
  print('.', end = '')
  if i % 50 == 0:
    print('\n[' + str(i) + '] ', end = '')
  cl = get_new_cluster2(Zdf, i)
  if len(cl) == 0:
    break
  if clusters_contain(clusters, cl):
    continue
  cldict = {}
  cldict[i] = cl
  clen = 2
  j = i+1
  while j < len(cdf):
    st, cl = add_scene_to_cluster(cdf, cl,j)
    if st == -1:
      break
    if len(cl) > clen+10:
      break
    cldict[st] = cl
    clen = len(cl)
    j = st+1
  clusters.append(cldict)

# WRITE CLUSTER CHAINS TO FILE
with open('clists.csv', 'w') as f:
  writer = csv.writer(f)
  for el in clusters:
    clist = []
    k = el.keys()
    for ki in k:
      for s in el[ki]:
        if s not in clist:
          clist.append(s)
    writer.writerow(clist)