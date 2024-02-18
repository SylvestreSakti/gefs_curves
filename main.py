#!/usr/bin/env python3

import urllib.request
import re
import pickle
from datetime import date

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def scrapTableau(heurerun) :
    gefs_data = {"version" : "0.1","lieu" : "Paris"}
    modes = ["Temp 850hPa","Temp 500hPa","Pression","Precip","Cumuls","Temp. 2m","Z500","CAPE",
             "Vent 10m","Vent Rafales 10m","Vent 850hPa","Iso 0"]
    modes_id = [0,1,2,3,23,7,4,6,11,13,9,14]
    nom_du_run = ""

    for mode in range(len(modes)) :

            page = urllib.request.urlopen('http://www.meteociel.fr/modeles/gefs_table.php?x=0&y=0&lat=48.8621&lon=2.33936&run='
                                          +heurerun+'&ext=fr&mode='+str(modes_id[mode])+'&sort=0')
            print("Scraping page : " + 'http://www.meteociel.fr/modeles/gefs_table.php?x=0&y=0&lat=48.8621&lon=2.33936&run='
                                          +heurerun+'&ext=fr&mode='+str(modes_id[mode])+'&sort=0')
            page = str(page.read())


            table_start = page.find("""<table class""")
            table_end = page.find("</table>",table_start)

            html_table = page[table_start:table_end].split("</tr>")
            tableau = []
            for i in range(len(html_table)-2) :
                run = html_table[i+1].split("</td>")
                run = [cleanhtml(run[0])]+[float(cleanhtml(html)) for html in run[1:-1]]
                tableau += [run]

            echeance = tableau[0][0][0:10]
            jour_date = echeance.replace("-","")
            nom_du_run = jour_date + "_" + heurerun
            gefs_data["nom_du_run"] = nom_du_run
            gefs_data[modes[mode]] = tableau.copy()

    with open('data/'+nom_du_run+'.gefs', 'wb') as fp:
        pickle.dump(gefs_data, fp)

    print(gefs_data)


scrapTableau("00")
scrapTableau("06")
scrapTableau("12")
scrapTableau("18")
