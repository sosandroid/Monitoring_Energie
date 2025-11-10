#!/usr/bin/python
# -*- coding: utf-8 -*-
##############################
# Récupère le calendrier tempo depuis l'API de https://www.api-couleur-tempo.fr
#
# V 0.0.1
# 10/2025
##############################
## Documentation de l'API : https://www.api-couleur-tempo.fr/api
#
#
# Exemple de données récupérées en 4 appels :
# {
#   "today_code": 1,
#   "today_couleur": "Bleu",
#   "tomorrow_code": 1,
#   "tomorrow_couleur": "Bleu",
#   "periode": "2025-2026",
#   "bissextile": false,
#   "dernierJourInclus": "2025-10-12",
#   "joursBleusConsommes": 42,
#   "joursBlancsConsommes": 0,
#   "joursRougesConsommes": 0,
#   "joursBleusRestants": 258,
#   "joursBlancsRestants": 43,
#   "joursRougesRestants": 22,
#   "bleuHC": 0.1232,
#   "bleuHP": 0.1494,
#   "blancHC": 0.1391,
#   "blancHP": 0.173,
#   "rougeHC": 0.146,
#   "rougeHP": 0.6468,
#   "dataGouvId": 113,
#   "tarifForce": false,
#   "dateDebut": "2025-08-01"
# }

from . import utils
from pathlib import Path

def get_tempo_data():
    url_today = "https://www.api-couleur-tempo.fr/api/jourTempo/today"
    url_tomorrow = "https://www.api-couleur-tempo.fr/api/jourTempo/tomorrow"
    url_stats = "https://www.api-couleur-tempo.fr/api/stats"
    url_tarifs = "https://www.api-couleur-tempo.fr/api/tarifs"
    
    # Faire les requêtes API
    data_today = utils.getApiData(url_today)
    data_tomorrow = utils.getApiData(url_tomorrow)
    data_stats = utils.getApiData(url_stats)
    data_tarifs = utils.getApiData(url_tarifs)
    if data_today is None or data_tomorrow is None or data_stats is None or data_tarifs is None:
        return None
    return {
        "today_code": data_today['codeJour'],
        "today_couleur": data_today['libCouleur'],
        "tomorrow_code": data_tomorrow['codeJour'],
        "tomorrow_couleur": data_tomorrow['libCouleur'],
        **data_stats,
        **data_tarifs
    }

def get_tempo_html(conf):
    # Génère le HTML du calendrier tempo
    tempo = {"__tempohtml__":"", "__couleurj__":"", "__couleurj1__":""}
    data = get_tempo_data()
    # if data is None:
    #     return ""
    
    
    
    template = utils.loadTextFile(Path(conf['rootPath']) / conf['app']['tempotemplate'])
    tempo['__tempohtml__'] = utils.replaceTextInTemplate(template, {
            "__couleurj__": data['today_couleur'],
            "__couleurj1__": data['tomorrow_couleur'],
            "__prixhprouge__": str(data['rougeHP']),
            "__prixhpblanc__": str(data['blancHP']),
            "__nbblancs__": str(data['joursBlancsRestants']),
            "__nbrouges__": str(data['joursRougesRestants']),
            "__stylej__": conf['csscouleurs'][data['today_code']],
            "__stylej1__": conf['csscouleurs'][data['tomorrow_code']]
        })
    tempo['__couleurj__'] = data['today_couleur']
    tempo['__couleurj1__'] = data['tomorrow_couleur']
    tempo['today_code'] = data['today_code']
    tempo['tomorrow_code'] = data['tomorrow_code']
    return tempo