#!/usr/bin/python
# -*- coding: utf-8 -*-
##############################
# Envoi de mail à travers un SMTP 
#
# V 0.0.1
# 10/2025
##############################

from . import utils
from datetime import datetime, timedelta
from pathlib import Path

def get_forecast_solar(location):
    # Récupère les données de forecast solaire pour un emplacement donné
    url_solar = "https://api.forecast.solar/estimate/watthours/day/" + location['lat'] + "/" + location['lon'] + "/" + location['declination'] + "/" + location['azimuth'] + "/" + location['kwpeak']
    data_solar = utils.getApiData(url_solar)
    
    if data_solar is not None and 'result' in data_solar:
        today = datetime.today().strftime('%Y-%m-%d')
        tomorrow = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
        return {
            "__solar_today__": str(data_solar['result'][today]/1000),
            "__solar_tomorrow__": str(data_solar['result'][tomorrow]/1000)
        }
    return None

def get_forecast_solar_html(recipient, conf):
    # Génère le HTML du forecast solaire pour un destinataire donné
    if recipient['hasphotovoltaics']:
        data_solar = get_forecast_solar(recipient['location'])
        if data_solar is not None:
            template = utils.loadTextFile(Path(conf['rootPath']) / conf['app']['forecastsolartemplate'])
            return utils.replaceTextInTemplate(template, data_solar)
    return ""