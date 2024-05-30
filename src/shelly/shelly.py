

# HTTP interface between Shelly device & EmonCMS
#  
# coded by: Emmanuel Havet

# --------------------------------------------------------------------------- #
# Dependencies
# --------------------------------------------------------------------------- #
import os
import requests
import json
from pathlib import Path
from configparser import ConfigParser
from datetime import datetime
from time import sleep
import time


# --------------------------------------------------------------------------- #
# Globals
# --------------------------------------------------------------------------- #

version = "v1.0.0"

ConfFile             = str(Path(__file__).parent.absolute() / 'shelly.conf')
Config               = None
Shellycfg            = None
Emoncfg              = None
data                 = None
Shellydata           = None
debug                = False
senddata             = False


# --------------------------------------------------------------------------- #
# Functions - configuration
# --------------------------------------------------------------------------- #

def getConfig(file):
    global Shellycfg, Emoncfg, debug, Config, senddata
    
    if os.path.isfile(file):
        Config = ConfigParser()
        Config.read(file)
        if (debug): print(Config.sections())
        Emoncfg = dict(Config['emoncms'])
        Emoncfg['enabled'] = str2bool(Emoncfg['enabled'])
        Shellycfg = dict(Config['shellypro3em'])
        Shellycfg['enabled'] = str2bool(Shellycfg['enabled'])
        debug = Config['general'].getboolean('debug') 
        senddata = Config['general'].getboolean('senddata')
        
        if (debug):
            print(f'Emoncfg: {Emoncfg}')
            print(f'Shellycfg: {Shellycfg}')
     
        return True
    else:
        print(f'No config file found {file}')
        return False

def setConfig():
    global Config, ConfFile
    with open(ConfFile, 'w') as configfile:
        Config.write(configfile)
    return
# --------------------------------------------------------------------------- #
# Functions - Shelly pro 3 EM
# --------------------------------------------------------------------------- #

def getShellydata():
    global Shellydata, Shellycfg, debug
    
    if(Shellycfg['enabled']):
        params = dict(id=0)
        url = f"{Shellycfg['url']}{Shellycfg['r_data_uri']}?id=0"
        if (debug): printDebug('Shelly data url', url)

        #Shellydata = requests.get(url, headers={'Content-Type': 'application/json'})
        Shellydata = dict(requests.get(url, headers={'Content-Type': 'application/json'}).json())
        if (debug): printDebug('Shelly data', Shellydata)
        return
    else:
        # test data
        s = '{"id":0,"a_current":4.029,"a_voltage":236.1,"a_act_power":951.2,"a_aprt_power":951.9,"a_pf":1,"a_freq":50,"b_current":4.027,"b_voltage":236.201,"b_act_power":-951.1,"b_aprt_power":951.8,"b_pf":1,"b_freq":50,"c_current":3.03,"c_voltage":236.402,"c_active_power":715.4,"c_aprt_power":716.2,"c_pf":1,"c_freq":50,"n_current":11.029,"total_current":11.083,"total_act_power":2484.782,"total_aprt_power":2486.7,"user_calibrated_phase":[],"errors":["phase_sequence"]}'
        Shellydata = dict(s)
        return
    
def toggleShellyswitch(command = 'off'):
    global Shellycfg, senddata, debug
    if(Shellycfg['enabled'] and command in ("on", "off", "toggle")):
        url = f"{Shellycfg['url']}relay/{Shellycfg['relay_id']}?turn={command}"
        if (debug): printDebug('Shelly Switch', url)
        if (senddata):
            resp = requests.get(url, headers={'Content-Type': 'application/json'})
            if (debug): printDebugHttp('Shelly Switch', resp)
            return
    else:
        if (debug): 
            printDebug('Shelly enabled', Shellycfg['enabled'])
            printDebug('Shelly Switch command', command)
        return

# --------------------------------------------------------------------------- #
# Functions - energy routing limitation
#
# 2 options to manage the routing energy quantity.
# a- using solcast to get power generation forecast.
# b- using ECS temperature
# c- using routed energy
#
# The ideal is using a combination of the 3 data
# 
# --------------------------------------------------------------------------- #
def getDailyProd():
    #from feed
    #returns value in Wh https://identity-dev.mobifactory.net
    global Emoncfg, debug
    url = Emoncfg['url']+Emoncfg['r_uri_dailyenergy']+str(todayMidnight())+'&apikey='+Emoncfg['apikey']
    if (debug): printDebug('EmonURL energy', url)
    resp = requests.get(url)
    if (debug): printDebugHttp('Daily Energy', resp)
    return float(resp.text) * 1000

def getDailyProd2():
    #from input {'time': 1717015802, 'value': 14.68, 'processList': ''}
    #returns value in Wh
    global Emoncfg, debug
    url = Emoncfg['url']+Emoncfg['r_uri_daily2']+'?apikey='+Emoncfg['apikey']
    if (debug): printDebug('EmonURL energy', url)
    resp = requests.get(url)
    if (debug): printDebugHttp('Daily Energy', resp)
    return float(resp.json()['value']) * 1000
	
def limitFromProduction():
    

# --------------------------------------------------------------------------- #
# Functions - utils funtions
# --------------------------------------------------------------------------- #

def str2bool(v):
    return v.lower() in ("true", "t")
  
def remapKeys(data, remap, allkeys = False):
    if(allkeys): 
        # return all keys from data and remap selected keys
        return dict((remap[key], data[key]) if key in remap else (key, value) for key, value in data.items())
    else:
        # return only selected keys in remapping
        return dict((remap[key], data[key]) for key, value in data.items() if key in remap)

def printDebugHttp (sentto, requestObject):
    print(f'{sentto} data sent: {requestObject}')
    print(f'response: {requestObject.json()}\n')
    return

def printDebug(message, data):
    print(f'{message}: {data}\n')
    return

# --------------------------------------------------------------------------- #
# Functions - send data to outside world
# --------------------------------------------------------------------------- #
 
def sendEmonCMS(data):
    global Emoncfg, debug, senddata

    if(Emoncfg['enabled']):

        if ('user_calibrated_phase' in data): data.pop('user_calibrated_phase') #not managed by EmonCMS
        if ('errors' in data): data.pop('errors') #not managed by EmonCMS
        
        if (debug): printDebug('Emondata', data)

        params = dict(node=Emoncfg['nodename_shelly'], fulljson=json.dumps(data), apikey=Emoncfg['apikey'])
        if (senddata):
            res = requests.get(Emoncfg['url']+Emoncfg['uri_senddata'], params=params)
            if (debug): 
                printDebugHttp('Emon data sent', res)
    else:
        return

    
# --------------------------------------------------------------------------- #
# Functions - rate export to platforms limit management
# --------------------------------------------------------------------------- #

def setNextResetAllowedTime():
    global Config
    #Tomorrow timestamp 00:00
    next = datetime.strptime(str(datetime.today().strftime('%Y-%m-%d')) + ' 00:00:00', '%Y-%m-%d %H:%M:%S').timestamp() + 86400
    #Set tomorrow at the conf hour
    Config['shellypro3em']['next_relay_reset'] = str(next)
    setConfig()

def todayMidnight():
    return int(datetime.strptime(str(datetime.today().strftime('%Y-%m-%d')) + ' 00:00:00', '%Y-%m-%d %H:%M:%S').timestamp())

def todayNow():
    return int(datetime.today().timestamp())
    
# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    if(getConfig(ConfFile)):  
        #getShellydata()
        #toggleShellyswitch('toto')
        #sendEmonCMS(Shellydata) #send data to EmonCMS
       print( getDailyProd())
       print(getDailyProd2())
    else:
        print('Can do nothing, no config found')
