#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

surv_dir = "limesurvey/exports"
surv_id_file = "active_surveys.csv"
steps_file = "cdf.csv"
raters = ['st','cc','vs','pv','lg','bz']
list_of_files = glob.glob(surv_dir + '/**/*', recursive=True) 

df_id = pd.read_csv(surv_id_file, index_col=0)
df_id['fname'] = df_id['fname'].apply(lambda x : x[x.rfind('_')+1:len(x)-4])
df_id['csize'] = 0


for f in list_of_files:
    sid = f[f.rfind("/")+1:len(f)-4]
    dfi = pd.read_csv(f, sep=';')
    dfi = dfi.loc[:, dfi.columns.str.startswith('Q')]
    dfi = dfi[dfi.Q00.isin(raters)]
    dfi.drop_duplicates(subset=['Q00'], keep='first', inplace=True) 
    dfi.index = dfi['Q00']
    dfi = dfi.drop(['Q00'], axis=1)
    dfi = dfi.fillna(3)
    m = dfi.mean(axis=0)
#    mcut = [m[0]]
    mcut = []
    ok = False
    for v in m[::-1]:
        if not ok and v <= 2.5:
            mcut.append(v)
            ok = True
        elif ok:
            mcut.append(v)
            
#    for v in m[1:]:
#        if v <= 2.5:
#            mcut.append(v)
#        else:
#            break
    df_id.at[df_id.index[df_id['survid']==int(sid)][0], 'csize'] = len(mcut)+1


df_step = pd.read_csv(steps_file, index_col = 0)
df_id['min_step'] = -1
df_id['max_step'] = -1
for ind, row in df_id.iterrows():
    sid = row['fname']
    smin = smax = -1
    serr = 2000
    for el in df_step.head():
        iid = df_step.at[sid,el]
        ns = len(df_step[df_step[el]==iid])
        ierr = abs(ns-row['csize'])
        if ierr < serr:
            smin = int(el)
            smax = int(el)
            serr = ierr
        elif ierr == serr:
            smax = int(el)
        else:
            break
    df_id.at[ind,'min_step'] = smin
    df_id.at[ind,'max_step'] = smax
df_id.to_csv("survey_thresh.csv")

vgood = pd.Series(index=df_step.columns)
for t in vgood.index:
    print(t)
    ngood = len(df_id[(df_id['min_step'] <= int(t)) & (df_id['max_step'] >= int(t))])
    vgood[t] = ngood

plot0 = vgood.plot(xticks = np.arange(0, 1010, 100), yticks = np.arange(0, 50, 5), grid=True, xlabel="Number of algorithm steps", ylabel="Correct clusters")
fig0 = plot0.get_figure()
fig0.savefig("correct_clusters0.png", dpi=600)
plt.close()

vgood2 = vgood.iloc[::-1]
vgood2.index = [1010-int(i) for i in vgood2.index]  
vgood2.to_csv("nclust_report.csv")
plot = vgood2.plot(xticks = np.arange(0, 1010, 100), yticks = np.arange(0, 50, 5), grid=True, xlabel="Number of clusters", ylabel="Correct clusters")
fig = plot.get_figure()
fig.savefig("correct_clusters1.png", dpi=600)