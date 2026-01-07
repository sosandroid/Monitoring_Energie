#!/usr/bin/python
# -*- coding: utf-8 -*-
##############################
# S'occupe de la des prévisions tempo
#
# V 0.0.1
# 01/2026
##############################
from pathlib import Path
from . import utils
from datetime import datetime

def getOpenDpeData(conf):
    data = utils.getApiData(conf['opendpe']['base_url'])
    if data is None:
        return None
    # Return only first 7 days
    if(datetime.now().hour <= 10):
        return data[0:7]
    else:
        return data[1:7]

def openDpeDataAdapter(conf):
    data = getOpenDpeData(conf)
    if data is None:
        return None

    color_map = {'bleu': 1,'blanc': 2,'rouge': 3}
    weekdays_fr = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']
    
    for day in data:
        # couleur -> code (default 0 = undetermined)
        couleur_raw = (day.get('couleur') or '').strip().lower()
        couleur_code = 0
        for key, code in color_map.items():
            if key in couleur_raw:
                couleur_code = code
                break
        day['codeJour'] = couleur_code
        
        # date string -> day of week short name
        date_str = day.get('date')
        if date_str:
            dt = datetime.strptime(date_str, '%Y-%m-%d')
            #day['timestamp'] = int(dt.timestamp())
            day['jour_court'] = weekdays_fr[dt.weekday()]
        
        #probability
        day['probability'] = str(int(float(day.get('probability', 0)) * 100)) + " %"

    return data
    

def getOneTempoForcastCard(day, conf):
    # Fill one tempo forecast card template
    results = dict()
    #results['__date__'] = day.get('date', '-')
    results['__jour_court__'] = day.get('jour_court', '-')
    #results['__couleur__'] = day.get('couleur', '-')
    results['__code_couleur_jour__'] = conf['csscouleurs'][day.get('codeJour', '0')]
    results['__probability__'] = day.get('probability', '0 %')

    template = utils.loadTextFile(Path(conf['rootPath']) / conf['app']['tempoForecastCardTemplate'])
    return utils.replaceTextInTemplate(template, results)

def getTempoForecast(conf):
    # Génère le HTML du calendrier tempo
    tempo = {"__tempoforcasthtml__":""}
    data = openDpeDataAdapter(conf)
    if data is None:
        return tempo
    
    cards = ""
    for day in data:
        card_html = getOneTempoForcastCard(day, conf)
        cards += card_html
    
    template = utils.loadTextFile(Path(conf['rootPath']) / conf['app']['tempoForecastTemplate'])
    tempo['__tempoforcasthtml__'] = utils.replaceTextInTemplate(template, {'__tempocards__': cards})
    
    return tempo
