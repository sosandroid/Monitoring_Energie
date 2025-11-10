#!/usr/bin/python
# -*- coding: utf-8 -*-
##############################
# Récupère les données Tempo et les transmets par e-mail
#
# V 0.0.1 11/2023 - fonctionne avec API EDF et Mailjet
# V 0.0.2 10/2025 - passage à SMTP simple et couleur tempo API
# V 0.0.3 11/2025 - ajout forecast solaire | multi-recherche météo et forecast solaire
# 
##############################

from datetime import datetime
from pathlib import Path
#import time

#import libs as libs  # Pour que les modules dans libs soient reconnus
import libs.smtp as smtp
import libs.owm as owm
import libs.utils as utils
import libs.tempo as tempo
import libs.forecastsolar as forecastsolar



# --------------------------------------------------------------------------- #
# Globals
# --------------------------------------------------------------------------- #

version = "v0.0.3"

RootPath             = Path(__file__).parent.absolute()
Config               = utils.loadJsonFile(str(RootPath / 'json/config-perso.json'))
Config['rootPath']   = str(RootPath)
lastRunJson          = utils.loadJsonFile(str(RootPath / 'run.json'))
lastJourStatus       = tempo.get_tempo_html(Config)

debug                = True
debug_sauvMail       = True  # sauvegarde les mails au format html pour vérification
toSendMail           = False # indique si l'on doit faire le traitement pour les e-mails
reallySendMail       = False  # à mettre à False pour tests sans envoi de mail

def resetLastRun():
    # remets à zéro les compteurs si on est un nouveau jour
    if(globals()['lastRunJson']['date'] < utils.timestampTodayMidnight()):
        globals()['lastRunJson']['j'] = 0
        globals()['lastRunJson']['j1'] = 0

def updateLastRun(j, j1):
    # met à jour le json de suivi
    globals()['lastRunJson']['j'] = j
    globals()['lastRunJson']['j1'] = j1
    globals()['lastRunJson']['date'] = datetime.now().timestamp()

    # sauvegarde le json
    if globals()['debug']:
        print(f"Debug: Sauvegarde du fichier run.json : {globals()['lastRunJson']}")
    utils.saveLastRun(globals()['lastRunJson'], globals()['Config'])
	
def needForUpdateCheck():
    # récupère les données et vérifie si elles ont changé depuis le dernier check
    if globals()['lastJourStatus'] is not None:
        jour = globals()['lastJourStatus']['today_code']
        jour1 = globals()['lastJourStatus']['tomorrow_code']

        resetLastRun()

        # si les données ont changé, on met à jour le json et on prépare l'envoi de mail si besoin
        if (globals()['lastRunJson']['j'] != jour) or (globals()['lastRunJson']['j1'] != jour1):
            updateLastRun(jour, jour1)
            globals()['toSendMail'] = True
            
def dataforEmail(recipient):
    data = dict()
        
    data['__heure__'] = utils.currenttime()
    data['__tempohtml__'] = globals()['lastJourStatus']['__tempohtml__']
    data['__couleurj__'] = globals()['lastJourStatus']['__couleurj__']
    data['__couleurj1__'] = globals()['lastJourStatus']['__couleurj1__']
    data['__forecastsolarhtml__'] = forecastsolar.get_forecast_solar_html(recipient, globals()['Config'])
    data.update(owm.getWeatherCards(recipient, globals()['Config']))
    return data

def prepareEmailBody(recipient):
    data = dataforEmail(recipient)
    template = utils.loadTextFile(Path(globals()['Config']['rootPath']) / globals()['Config']['app']['mailhtmltemplate'])
    body_html = utils.replaceTextInTemplate(template, data)
    template = utils.loadTextFile(Path(globals()['Config']['rootPath']) / globals()['Config']['app']['mailtxttemplate'])
    body_text = utils.replaceTextInTemplate(template, data)
    body = {'html': body_html, 'text': body_text}
    
    if(datetime.now().hour <= 11):
        sujet = globals()['Config']['subjectEmail']['matin']
    else:
        sujet = globals()['Config']['subjectEmail']['demain']
    body['sujet'] = utils.replaceTextInTemplate(sujet, data)
      
    return body

# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
if __name__ == "__main__":

    if debug:
        print(f"Debug: {version} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        #print(f"Debug: RootPath = {globals()['Config']['rootPath']}")
        #print(f"Debug: Last run data = {globals()['lastRunJson']}")
        #print(f"Debug: Last jour status = {globals()['lastJourStatus']}")
        #print(f"Debug: config = {globals()['Config']}")
        #exit(0)
    
    needForUpdateCheck()
    if toSendMail or debug:
        i = 1
        for recipient in globals()['Config']['recipients']:
            if ((globals()['lastJourStatus']['today_code'] >= recipient['alert-level']) or (globals()['lastJourStatus']['tomorrow_code'] >= recipient['alert-level'])) or debug:
                msg = prepareEmailBody(recipient)
                if debug_sauvMail: 
                    utils.saveFile(msg['html'], Path(globals()['Config']['rootPath']) / f"email_{i}.html")
                    print(f"Sauvegarde du mail #{i} (alerte niveau {recipient['alert-level']})")
            
            if reallySendMail:
                smtp.envoyer_email_smtp(
                    globals()['Config']['smtp'],
                    recipient['emails'],
                    msg
                )
            i += 1
