#!/usr/bin/python
# -*- coding: utf-8 -*-
##############################
# Prépare les données pour envoi via Mailjet
#
# V 0.0.1
# 11/2023
##############################
from pathlib import Path
from datetime import datetime
from mailjet_rest import Client as mjclient
import utils

def mjMessages(conf, data):
    # Prepare the messages JSON to be sent to Mailjet as bulkmail
    mes = utils.loadJsonFile(str(Path(__file__).parent.absolute() / conf['app']['messagestemplate']))
    data['__stylej__'] = conf['csscouleurs'][data['__couleurj__']]
    data['__stylej1__'] = conf['csscouleurs'][data['__couleurj1__']]

    mes['Globals']['HTMLPart'] = mjFormatMessage(utils.loadTextFile(str(Path(__file__).parent.absolute() / conf['app']['mailhtmltemplate'])), data)
    mes['Globals']['TextPart'] = mjFormatMessage(utils.loadTextFile(str(Path(__file__).parent.absolute() / conf['app']['mailtxttemplate'])), data)
    mes['Globals']['Subject'] = conf['subjectEmail']['matin'] if(datetime.now().hour < 12) else conf['subjectEmail']['demain']
    mes['Globals']['Subject'] = mjFormatMessage(mes['Globals']['Subject'], data)

    return mes

def mjFormatMessage(template, data):
    # Final template fillin
    template = template.replace("__couleurj__", data['__couleurj__'])
    template = template.replace("__couleurj1__", data['__couleurj1__'])
    template = template.replace("__nbrouges__", str(data['__nbrouges__']))
    template = template.replace("__nbblancs__", str(data['__nbblancs__']))
    template = template.replace("__meteohtml__", data['__meteohtml__'])
    template = template.replace("__heure__", data['__heure__'])
    template = template.replace("__sunset__", data['__sunset__'])
    template = template.replace("__sunrise__", data['__sunrise__'])
    template = template.replace("__stylej__", data['__stylej__'])
    template = template.replace("__stylej1__", data['__stylej1__'])
    return template



def mjSendMail(conf, messages):
    # Send real message
    api_key = conf['mailjet']['apikey']
    api_secret = conf['mailjet']['apisecret']
    # utils.saveJsonFile(messages, "result.json")
    mj = mjclient(auth=(api_key, api_secret), version='v3.1')
    result = mj.send.create(data=messages)
    return result.json()