#!/usr/bin/python
# -*- coding: utf-8 -*-
##############################
# S'occupe de la meteo
#
# V 0.0.1
# 11/2023
##############################
from pathlib import Path
from . import utils

def buildOwmUrl(conf):
    return utils.makeUrlQuery(conf['owm']['forcast_url'], conf['owm']['params'])

def getOwmData(conf):
    data = utils.getApiData(buildOwmUrl(conf))
    return data

def getOneWeatherCardData(data, conf):
    # Fill weather card template
    results = dict()
    results['__heure__'] = utils.hourFromTimestamp(data['dt']) if ("dt" in data.keys()) else "0"
    results['__icon__'] = data['weather'][0]['icon'] if ("weather" in data.keys()) else "00"
    results['__cond__'] = data['weather'][0]['description'] if ("weather" in data.keys()) else "-"
    results['__temp__'] = data['main']['temp']
    results['__pression__'] = data['main']['pressure']
    results['__humidite__'] = data['main']['humidity']
    results['__pluie__'] = data['rain']['3h'] if ("rain" in data.keys()) else "0"
    results['__iconimg__'] = getIconInlineImg(conf, results['__icon__'])
    results['__city__'] = conf['owm']['params']['q'] if 'q' in conf['owm']['params'] else ""

    template = utils.loadTextFile(Path(conf['rootPath']) / conf['app']['meteocardtemplate'])
    utils.replaceTextInTemplate(template, results)
    
    return {'icon': results['__icon__'], 'card': utils.replaceTextInTemplate(template, results)}

def getIconInlineImg(conf, icon):
    # get icon as base64 image from json
    icons = utils.loadJsonFile(Path(conf['rootPath']) / conf['app']['messageicons-img'])
    return str(icons[icon])

def getWeatherCards(recipient, conf):
    # Fill all weather card templates
    weather = {"__meteohtml__":"", "__sunset__":"", "__sunrise__":""}
    conf['owm']['params']['lat'] = recipient['location']['lat']
    conf['owm']['params']['lon'] = recipient['location']['lon']
    data = utils.getApiData(buildOwmUrl(conf))
    
    if data is None or 'list' not in data:
        return weather
    
    cards = ""
    for card in data['list']:
        res = getOneWeatherCardData(card, conf)
        cards += res['card']
    
    template = utils.loadTextFile(Path(conf['rootPath']) / conf['app']['meteotemplate'])
    weather['__meteohtml__'] = utils.replaceTextInTemplate(template, {'__meteocards__': cards, '__city__': data['city']['name']})
    
    weather['__sunset__'] = utils.timeFromTimestamp(data['city']['sunset'])
    weather['__sunrise__'] = utils.timeFromTimestamp(data['city']['sunrise'])

    return weather
    
    


