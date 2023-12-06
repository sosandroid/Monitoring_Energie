#!/usr/bin/python
# -*- coding: utf-8 -*-
##############################
# S'occupe de la meteo
#
# V 0.0.1
# 11/2023
##############################
from pathlib import Path
import utils

def buildOwmUrl(conf):
    return utils.makeUrlQuery(conf['owm']['forcast_url'], conf['owm']['params'])

def getOwmData(conf):
    data = utils.getApiData(buildOwmUrl(conf))
    return data

def getOneWeatherCardData(data, conf):
    # Fill wather card template
    results = dict()
    results['heure'] = utils.hourFromTimestamp(data['dt']) if ("dt" in data.keys()) else "0"
    results['icon'] = data['weather'][0]['icon'] if ("weather" in data.keys()) else "00"
    results['cond'] = data['weather'][0]['description'] if ("weather" in data.keys()) else "-"
    results['temp'] = data['main']['temp']
    results['pression'] = data['main']['pressure']
    results['humidite'] = data['main']['humidity']
    results['pluie'] = data['rain']['3h'] if ("rain" in data.keys()) else "0"
    results['iconimg'] = getIconInlineImg(conf, results['icon'])

    template = utils.loadTextFile(str(Path(__file__).parent.absolute() / conf['app']['meteotemplateinline']))

    template = template.replace("__cond__", results['cond'])
    template = template.replace("__heure__", results['heure'])
    template = template.replace("__temp__", str(results['temp']))
    template = template.replace("__press__", str(results['pression']))
    template = template.replace("__humid__", str(results['humidite']))
    template = template.replace("__press__", str(results['pression']))
    template = template.replace("__rain__", str(results['pluie']))
    template = template.replace("__icon__", results['iconimg'])

    return {'icon': results['icon'], 'card': template}

def getIconInlineImg(conf, icon):
    # get icon as base64 image from json
    icons = utils.loadJsonFile(str(Path(__file__).parent.absolute() / conf['app']['messageicons-img']))
    return str(icons[icon])

def getWeatherCards(conf):
    # Fill all wather card templates
    weather = {"__meteohtml__":"", "__heure__":"", "__sunset__":"", "__sunrise__":""}
    data = utils.getApiData(buildOwmUrl(conf))
    
    for card in data['list']:
        res = getOneWeatherCardData(card, conf)
        weather['__meteohtml__'] += res['card']
    
    weather['__heure__'] = utils.currenttime()
    weather['__sunset__'] = utils.timeFromTimestamp(data['city']['sunset'])
    weather['__sunrise__'] = utils.timeFromTimestamp(data['city']['sunrise'])

    return weather
    
    


