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
    page = urllib.request.urlopen('http://www.meteociel.fr/modeles/gefs_table.php?x=0&y=0&lat=48.8621&lon=2.33936&run='+heurerun+'&ext=fr&mode=0&sort=0')
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
    nom_du_run = jour_date + heurerun

    with open('data/'+nom_du_run+'.gefs', 'wb') as fp:
        pickle.dump(tableau, fp)

    print(tableau)


scrapTableau("00")
scrapTableau("06")
scrapTableau("12")
scrapTableau("18")

"""
with open ('outfile', 'rb') as fp:
    itemlist = pickle.load(fp)
"""
