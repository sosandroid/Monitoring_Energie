#!/usr/bin/python
# -*- coding: utf-8 -*-
##############################
# Récupère le calendrier tempo depuis une date et sauvegarde dans un fichier jSON
#
# V 0.0.1
# 11/2023
##############################

import time
from datetime import datetime
import json
import requests
from urllib.parse import urlencode, quote_plus

APIJoursURL = "https://particulier.edf.fr/services/rest/referentiel/searchTempoStore?dateRelevant="
jours_tempo = dict()
tstp = 1680300060  #1er avril 2023 00:01:00
today = datetime.now().timestamp()

def getApiData(api_url):
    return requests.get(api_url).json()

def saveJsonFile(data, name):
    with open(name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def timestampToStringFormat(tstp, form):
    return datetime.fromtimestamp(tstp).strftime(form)

def timestampToSqlDate(tstp):
    return timestampToStringFormat(tstp, "%Y-%m-%d")

def getJoursTempo(tstp):
    tempo = getApiData(APIJoursURL + timestampToSqlDate(tstp))
    globals()['jours_tempo'][timestampToSqlDate(tstp)] = tempo['couleurJourJ']
    globals()['jours_tempo'][timestampToSqlDate(tstp + 86400)] = tempo['couleurJourJ1']
    
if __name__ == "__main__":
    while tstp < today:
        getJoursTempo(tstp)
        tstp += 86400 * 2
    
    saveJsonFile(jours_tempo, "jours_tempo.json")
    
