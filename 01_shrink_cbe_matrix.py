#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from sklearn.decomposition import TruncatedSVD

df14 = pd.read_csv('cbe_matrix14.csv', index_col=0)

truncatedSVD=TruncatedSVD(300)
x = truncatedSVD.fit_transform(df14)
df14s = pd.DataFrame(x, index=df14.index)
df14s.to_csv('cbe_matrix14s.csv')
