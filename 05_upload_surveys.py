#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from citric import Client
from natsort import natsorted
import glob
import os
import pandas as pd

LS_URL = ""
SURV_DIR = ""

list_of_files = natsorted( filter( os.path.isfile, glob.glob(SURV_DIR + '/**/*', recursive=True) ) )

df = pd.DataFrame(columns=['fname','survid'])

with Client(LS_URL, "", "") as client:
    for i in range(100):    
        with open(list_of_files[i], "rb") as f:
            survey_id = client.import_survey(f, "txt")
        print("New survey:", survey_id)
        client.activate_survey(survey_id)
        df = df.append({'fname':list_of_files[i], 'survid': str(survey_id)},ignore_index=True)

df.to_csv("active_surveys.csv")