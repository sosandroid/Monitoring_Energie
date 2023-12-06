#!/usr/bin/python
# -*- coding: utf-8 -*-
##############################
# Récupère les données Tempo et les transmets par e-mail
#
# V 0.0.1
# 11/2023
##############################

from datetime import datetime
from pathlib import Path


import utils
import owm
import mailmj



# --------------------------------------------------------------------------- #
# Globals
# --------------------------------------------------------------------------- #

version = "v0.0.1"

APIJoursURL          = "https://particulier.edf.fr/services/rest/referentiel/searchTempoStore?dateRelevant=" + datetime.now().strftime('%Y-%m-%d')
APICptJoursURL       = "https://particulier.edf.fr/services/rest/referentiel/getNbTempoDays?TypeAlerte=TEMPO"
Config               = utils.loadJsonFile(str(Path(__file__).parent.absolute() / 'config.json'))

lastRunJson          = utils.loadJsonFile(str(Path(__file__).parent.absolute() / 'run.json'))
lastJourStatus       = utils.getApiData(APIJoursURL)
lastJourCompteur     = dict()

debug                = False
debugdata            = False
toSendMail           = False

def resetLastRun():
    if(globals()['lastRunJson']['date'] < utils.timestampTodayMidnight()):
        globals()['lastRunJson']['j'] = 0
        globals()['lastRunJson']['j1'] = 0

def updateLastRun(j, j1):
    compteurs = utils.getApiData(APICptJoursURL)
    globals()['lastRunJson']['j'] = j
    globals()['lastRunJson']['j1'] = j1
    globals()['lastRunJson']['date'] = datetime.now().timestamp()
    globals()['lastRunJson']['cpt_bleu'] = compteurs['PARAM_NB_J_BLEU']
    globals()['lastRunJson']['cpt_blanc'] = compteurs['PARAM_NB_J_BLANC']
    globals()['lastRunJson']['cpt_rouge'] = compteurs['PARAM_NB_J_ROUGE']
    utils.saveLastRun(globals()['lastRunJson'])
	
def needForUpdateCheck():
    # decodes status from EDF
    if globals()['lastJourStatus']['couleurJourJ'] == "TEMPO_BLEU": jour = 1
    elif globals()['lastJourStatus']['couleurJourJ'] == "TEMPO_BLANC": jour = 2
    elif globals()['lastJourStatus']['couleurJourJ'] == "TEMPO_ROUGE": jour = 3
    else: jour = 0
    if globals()['lastJourStatus']['couleurJourJ1'] == "TEMPO_BLEU": jour1 = 1
    elif globals()['lastJourStatus']['couleurJourJ1'] == "TEMPO_BLANC": jour1 = 2
    elif globals()['lastJourStatus']['couleurJourJ1'] == "TEMPO_ROUGE": jour1 = 3
    else: jour1 = 0

    resetLastRun()

    if (globals()['lastRunJson']['j'] != jour) or (globals()['lastRunJson']['j1'] != jour1):
        updateLastRun(jour, jour1)
        if ((jour >= globals()['Config']['app']['alertlevel']) or (jour1 >= globals()['Config']['app']['alertlevel'])): globals()['toSendMail'] = True

def getCouleur(c):
    if(c==1):
        return "bleu"
    elif(c==2):
        return "blanc"
    elif (c==3):
        return "rouge"
    else:
        return "indetermine"

def dataforEmail():
    data = dict()
    data['__couleurj__'] = getCouleur(globals()['lastRunJson']['j'])
    data['__couleurj1__'] = getCouleur(globals()['lastRunJson']['j1'])
    data['__nbrouges__'] = globals()['lastRunJson']['cpt_rouge']
    data['__nbblancs__'] = globals()['lastRunJson']['cpt_blanc']
    data.update(owm.getWeatherCards(globals()['Config']))
    return data

# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
if __name__ == "__main__":

    needForUpdateCheck()
    if toSendMail:
        mailmj.mjSendMail(Config, mailmj.mjMessages(Config, dataforEmail()))