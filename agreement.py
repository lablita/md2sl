#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.stats import inter_rater as irr

surv_dir = "../limesurvey/exports"
surv_id_file = "active_surveys.csv"
steps_file = "cdf.csv"
raters = ['st','cc','vs','pv','lg','bz']
list_of_files = glob.glob(surv_dir + '/**/*', recursive=True) 

df_id = pd.read_csv(surv_id_file, index_col=0)
df_id['fname'] = df_id['fname'].apply(lambda x : x[x.rfind('_')+1:len(x)-4])
df_id['agr'] = 0.0

dfagr = pd.DataFrame(index = raters)

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
    mcut = []
    ok = False
    for v in m[::-1]:
        if not ok and v <= 2.5:
            mcut.append(v)
            ok = True
        elif ok:
            mcut.append(v)
    df_id.at[df_id.index[df_id['survid']==int(sid)][0], 'csize'] = len(mcut)+1
    
    dfi['nc'] = 0
    dfit = dfi.T
    if dfit.columns.isin(raters).all() and len(dfit.columns) == len(raters):
        for r in raters:
            nc = len(dfit.loc[dfit[r] <= 2, :])
            dfi.at[r,'nc'] = nc
        dfinc = dfi['nc'].T
        dfagr[sid] = dfinc
    agg = irr.aggregate_raters(dfagr.T)
    agr = irr.fleiss_kappa(agg[0],method='fleiss')
    df_id.at[df_id.index[df_id['survid']==int(sid)][0], 'agr'] = agr
df_id.plot(x='csize', y='agr', kind='hist', grid=True, bins=20, label="Agreement")
plt.xlabel("Fleiss Kappa value")
plt.savefig("agreement.png", dpi=600)