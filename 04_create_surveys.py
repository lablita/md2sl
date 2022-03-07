#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import csv


def create_page1(sc_list, width=320, height=240):
    html = ""
    for i in range(0,len(sc_list)):
        html += '<div class="ckeditor-html5-video" style="text-align: left; float: left; margin-right: 10px; border: 4px solid green; background-color: limegreen;">'
        html += '<video controls="controls" controlslist="nodownload" height="' + str(height) + '" src="http://lablita.it/app/actionsim/mp4/' + sc_list[i] + '.mp4" width="' + str(width) + '"> </video></div>'
    html += '<br style="clear:both" /><p> </p><p><strong>Valuta la similarità tra questi due eventi:</strong></p>'
    return html

def create_page2(sc_list, ind, width1=200, height1=150, width2=320, height2=240):
    html = '<script>jQuery(document).ready(function(){\n x = "{H' + str(ind+1) + '}".replace(/<\/?[^>]+(>|$)/g, "").trim();\n for (let i = 1; i < x.length; i++) {\n if(parseInt(x.charAt(i)) > 2) {\n document.getElementById("v".concat(i+1)).style.borderColor = "red"; document.getElementById("v".concat(i+1)).style.backgroundColor = "indianred";\n }\n }\n }\n );\n </script>\n'
    for i in range(0,len(sc_list)-1):
        html += '<div id="v' + str(i) + '" class="ckeditor-html5-video" style="text-align: left; float: left; margin: 10px; border: 4px solid green; background-color: limegreen;">'
        html += '<video controls="controls" controlslist="nodownload" height="' + str(height1) + '" src="http://lablita.it/app/actionsim/mp4/' + sc_list[i] + '.mp4" width="' + str(width1) + '"> </video></div>'
    html += '<br style="clear:both" /><p> </p><hr />'
    html += '<div id="v' + str(len(sc_list)-1) + '" class="ckeditor-html5-video" style="text-align: left; float: left; margin-right: 10px;">'
    html += '<video controls="controls" controlslist="nodownload" height="' + str(height2) + '" src="http://lablita.it/app/actionsim/mp4/' + sc_list[len(sc_list)-1] + '.mp4" width="' + str(width2) + '"> </video></div>'
    html += '<br style="clear:both" /><p> </p><hr /><p><strong>Valuta la similarità rispetto al gruppo di eventi in verde:</strong></p>'
    return html


dfT = pd.read_csv('../limesurvey/limesurvey_template.txt', sep='\t')
df2T = dfT.iloc[81:89]
cnt = 1
with open('clists.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        df = dfT.copy()
        ind = df.loc[df['name'] == 'surveyls_title'].index.to_list()[0]
        df.at[ind,'text'] = str(cnt) + " - Event similarity test"
        ind = df.loc[df['name'] == 'Q0'].index.to_list()[0]
        html = df.at[ind,'text']
        html = create_page1([row[0],row[1]])
        df.at[ind,'text'] = html
        
        df2 = df2T.copy()
        df.drop(range(81,89), inplace=True)
        #print(df2)
        for i in range(0,len(row)-2):
            if i == 0:
                df2.at[83,"text"] = create_page2(row[0:i+3], i)
                df = df.append(df2)
            else:
                df2["id"] = df2["id"].apply(lambda x: x + 5)
                df2.at[83,"text"] = create_page2(row[0:i+3], i)
                df2.at[81,"type/scale"] = int(df2.at[81,"type/scale"]) + 1
                df2.at[83,"name"] = "Q" + str(i+1)
                df2.at[82,"name"] = "H" + str(i+1)
                df2.at[82,"text"] = "{join(H" + str(i) + ",Q" + str(i) + ")}"
                df2.at[82,"hidden"] = 1
                df2.at[88,"name"] = "E" + str(i+1)
                df = df.append(df2)
        df.to_csv('../limesurvey/surveys/' + str(cnt) + '_' + row[0] + '.txt', sep='\t', index=False, float_format='%.0f')
        cnt += 1