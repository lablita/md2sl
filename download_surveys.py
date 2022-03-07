#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from limepy import download

base_url = ""
user_name = ""
password = ""
user_id = ""

outdir = "limesurvey/exports"
sids_file = open("limesurvey/sids_to_export", "r")
sids = sids_file.read().splitlines()
print(sids)
sids_file.close()

for sid in sids:
    print(sid)
    try:
        csv = download.get_responses(base_url, user_name, password, user_id, sid)
        path = Path(outdir + '/' + sid + '.csv')
        path.write_text(csv)
    except:
        continue