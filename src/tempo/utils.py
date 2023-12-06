#!/usr/bin/python
# -*- coding: utf-8 -*-
##############################
# fonctions utiles
#
# V 0.0.1
# 11/2023
##############################

import time
from datetime import datetime
import json
import requests
from urllib.parse import urlencode, quote_plus

def loadJsonFile(file):
    with open(file, encoding='utf-8') as fic:
        return json.load(fic)
    
def loadTextFile(file):
    with open(file, encoding='utf-8') as fic:
        return ''.join(fic.readlines())

def getApiData(api_url):
    return requests.get(api_url).json()

def saveJsonFile(data, name):
    with open(name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def saveLastRun(data):
    saveJsonFile(data, "run.json")

def makeUrlQuery(url, params):
    return url + urlencode(params, quote_via=quote_plus)

def timestampToStringFormat(tstp, form):
    return datetime.fromtimestamp(tstp).strftime(form)

def hourFromTimestamp(tstp):
    return timestampToStringFormat(tstp, "%H")

def timeFromTimestamp(tstp):
    return timestampToStringFormat(tstp, "%H:%M")

def currenttime():
    return timeFromTimestamp(datetime.now().timestamp())

def timestampTodayMidnight():
    today = timestampToStringFormat(datetime.now().timestamp(), "%Y-%m-%d 00:00:00")
    return time.mktime(datetime.strptime(today, "%Y-%m-%d %H:%M:%S").timetuple())