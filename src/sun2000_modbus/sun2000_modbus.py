

# This send data Huawei Sun2000 to emonCMS and/or PVOutput.org
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

from pymodbus import pymodbus_apply_logging_config
from pymodbus.client import (
    ModbusSerialClient,
    ModbusTcpClient,
    ModbusTlsClient,
    ModbusUdpClient,
)
from pymodbus.exceptions import ModbusException
from pymodbus.pdu import ExceptionResponse
from pymodbus.transaction import (
    #    ModbusAsciiFramer,
    #    ModbusBinaryFramer,
    ModbusRtuFramer,
    ModbusSocketFramer,
    ModbusTlsFramer,
)

# --------------------------------------------------------------------------- #
# Globals
# --------------------------------------------------------------------------- #

version = "v1.1.3"

LogFileModbus        = str(Path(__file__).parent.absolute() / 'sun2000.log')
ConfFile             = str(Path(__file__).parent.absolute() / 'sun2000.conf')
modbusStabDelay      = 0.25
Config               = None
Sun2000cfg           = None
Emoncfg              = None
Pvoutputcfg          = None
ModbusDebug          = False
debug                = False
debugdata            = False


# --------------------------------------------------------------------------- #
# Functions - configuration
# --------------------------------------------------------------------------- #

def getConfig(file):
    global Sun2000cfg, Emoncfg, Pvoutputcfg, ModbusDebug, debug, Config, debugdata
    
    if os.path.isfile(file):
        Config = ConfigParser()
        Config.read(file)
        if (debug): print(Config.sections())
        Emoncfg = dict(Config['emoncms'])
        Emoncfg['enabled'] = str2bool(Emoncfg['enabled'])
        Sun2000cfg = dict(Config['sun2000'])
        Sun2000cfg['enabled'] = str2bool(Sun2000cfg['enabled'])
        Pvoutputcfg = dict(Config['pvoutput'])
        Pvoutputcfg['enabled'] = str2bool(Pvoutputcfg['enabled'])
        ModbusDebug = Config['general'].getboolean('modbusdebug')
        debug = Config['general'].getboolean('debug') 
        debugdata = Config['general'].getboolean('debugdata')
        
        if (debug):
            print(f'Emoncfg: {Emoncfg}')
            print(f'Sun2000cfg: {Sun2000cfg}')
            print(f'Pvoutputcfg: {Pvoutputcfg}')
            print(f'ModbusDebug: {ModbusDebug}')
     
        return True
    else:
        print(f'No config file found {file}')
        return False

def setConfig():
    global Config, ConfFile
    with open(ConfFile, 'w') as configfile:
        Config.write(configfile)
# --------------------------------------------------------------------------- #
# Functions - Sun2000 inverter
# --------------------------------------------------------------------------- #
    
def getSun2000Data():
    global Sun2000cfg, ModbusDebug, modbusStabDelay, LogFileModbus
    if (ModbusDebug):
        pymodbus_apply_logging_config("DEBUG", LogFileModbus)
    
    if(Sun2000cfg['enabled']):
        client = ModbusTcpClient(
                Sun2000cfg['address'],
                port=Sun2000cfg['port'],
                framer=ModbusSocketFramer,
                timeout=4,
                retries=2,
                retry_on_empty=True,
                # close_comm_on_error=False,
                # strict=True,
                # source_address=("192.168.1.1", 0),
            )
        client.connect()
        sleep(modbusStabDelay*4) # Connexion stabilization
        
        data = client.read_holding_registers(int(Sun2000cfg['registers_start']), int(Sun2000cfg['registers_len']), int(Sun2000cfg['unit']))
        client.close()
        
        # {'InstantPower': 0.0, 'InternalTemp': 0.0, 'AllTimeEnergy': 4218.73, 'DailyEnergy': 20.47, 'Voltage': 0.0, 'ActivePower': 0.0, 'GridFrequency': 0.0, 'Efficiency': 0.0, 'DeviceStatusCode': '0xa000'}
        return {
            "InstantPower": getRealPower(data),
            "InternalTemp": getTemperature(data),
            "AllTimeEnergy": getLifetimeEnergy(data),
            "DailyEnergy": getDailyEnergy(data),
            "VoltageL1": getVoltage(data, 1),
            "VoltageL2": getVoltage(data, 2),
            "VoltageL3": getVoltage(data, 3),
            "CurrentL1": getCurrent(data, 1),
            "CurrentL2": getCurrent(data, 2),
            "CurrentL3": getCurrent(data, 3),
            "ActivePower": getActivePower(data),
            "GridFrequency": getGridFrequency(data),
            "Efficiency": getGridFrequency(data),
            "DeviceStatusCode": getDeviceStatusCode(data)
              }

    else:
        return dict(InstantPower=0, InternalTemp=0, AllTimeEnergy=0, DailyEnergy=0)
        
# --------------------------------------------------------------------------- #
# Functions - registers manipulation
# --------------------------------------------------------------------------- #

def getRealPower(data) :
    global Sun2000cfg
    p = getRegisterValue(data, 1, Sun2000cfg['voltagel1_index'], Sun2000cfg['voltage_ratio']) * getRegisterValue(data, 2, Sun2000cfg['currentl1_index'], Sun2000cfg['current_ratio'])
    p += getRegisterValue(data, 1, Sun2000cfg['voltagel2_index'], Sun2000cfg['voltage_ratio']) * getRegisterValue(data, 2, Sun2000cfg['currentl2_index'], Sun2000cfg['current_ratio'])
    p += getRegisterValue(data, 1, Sun2000cfg['voltagel3_index'], Sun2000cfg['voltage_ratio']) * getRegisterValue(data, 2, Sun2000cfg['currentl3_index'], Sun2000cfg['current_ratio'])
    return p

def getTemperature(data):
    global Sun2000cfg
    return getRegisterValue(data, 1, Sun2000cfg['internaltemp_index'], Sun2000cfg['internaltemp_ratio'])

def getDailyEnergy(data):
    global Sun2000cfg
    return getRegisterValue(data, 2, Sun2000cfg['dailyenergy_index'], Sun2000cfg['dailyenergy_ratio'])
    
def getLifetimeEnergy(data):
    global Sun2000cfg
    return getRegisterValue(data, 2, Sun2000cfg['lifeenergy_index'], Sun2000cfg['lifeenergy_ratio'])
    
def getVoltage(data, L=1):
    #Only L1 voltage to handle single phase inverters
    global Sun2000cfg
    if (L==1):
        return getRegisterValue(data, 1, Sun2000cfg['voltagel1_index'], Sun2000cfg['voltage_ratio'])    
    elif (L==2):
        return getRegisterValue(data, 1, Sun2000cfg['voltagel2_index'], Sun2000cfg['voltage_ratio'])    
    elif (L==3):
        return getRegisterValue(data, 1, Sun2000cfg['voltagel3_index'], Sun2000cfg['voltage_ratio'])
    else:
        #assumes L1
        return getRegisterValue(data, 1, Sun2000cfg['voltagel1_index'], Sun2000cfg['voltage_ratio']) 
        
def getCurrent(data, L=1):
    #Only L1 voltage to handle single phase inverters
    global Sun2000cfg
    if (L==1):
        return getRegisterValue(data, 2, Sun2000cfg['currentl1_index'], Sun2000cfg['current_ratio'])    
    elif (L==2):
        return getRegisterValue(data, 1, Sun2000cfg['currentl2_index'], Sun2000cfg['current_ratio'])    
    elif (L==3):
        return getRegisterValue(data, 1, Sun2000cfg['currentl3_index'], Sun2000cfg['current_ratio'])
    else:
        #assumes L1
        return getRegisterValue(data, 1, Sun2000cfg['currentl1_index'], Sun2000cfg['current_ratio']) 
    
def getActivePower(data):
    global Sun2000cfg
    return getRegisterValue(data, 2, Sun2000cfg['activepower_index'], Sun2000cfg['activepower_ratio'])
    
def getGridFrequency(data):
    global Sun2000cfg
    return getRegisterValue(data, 1, Sun2000cfg['gridfrequency_index'], Sun2000cfg['gridfrequency_ratio'])
    
def getEfficiency(data):
    global Sun2000cfg
    return getRegisterValue(data, 1, Sun2000cfg['efficiency_index'], Sun2000cfg['efficiency_ratio'])
    
def getDeviceStatusCode(data):
    global Sun2000cfg
    return getRegisterValue(data, 1, Sun2000cfg['devicestatus_index'], Sun2000cfg['devicestatus_ratio'], True)
    
def getRegisterValue(data, length = 1, startindex = 0, ratio = 1, ashex = False):
    if length == 1 and not ashex:
        return data.registers[int(startindex)]/int(ratio)
    elif length == 1 and ashex:
        return hex(data.registers[int(startindex)])
    elif length == 2:
        return (data.registers[int(startindex)]*65535+data.registers[int(startindex)+1])/int(ratio)
    else:
        #default length = 1
        return data.registers[int(startindex)]/int(ratio)

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
    
    
    
# --------------------------------------------------------------------------- #
# Functions - send data to outside world
# --------------------------------------------------------------------------- #
 
def sendEmonCMS(data):
    global Emoncfg, debug, debugdata
    
    #for my specific use case - to be commented
    emonlabels = {'InstantPower': 'PUI_PROD', 'InternalTemp': 'TEMP_INT'}
    data = remapKeys(data, emonlabels, True)
    data.pop('DeviceStatusCode')
    
    if (debug or debugdata): print(f'Emondata: {data}')

    if(Emoncfg['enabled']):
        params = dict(node=Emoncfg['nodename'], fulljson=json.dumps(data), apikey=Emoncfg['apikey'])
        res = requests.get(Emoncfg['url'], params=params)
        if (debug or debugdata): print(f'Emon data sent {res}')
    else:
        return

def sendPVOutput(data):
    global Pvoutputcfg, debug, debugdata
    
    pvoutputlabels = {'InstantPower': 'v2', 'AllTimeEnergy': 'v1', 'VoltageL1': 'v6'}
    pvoutputdata = remapKeys(data, pvoutputlabels, False)
    
    pvoutputdata['d'] = datetime.today().strftime('%Y%m%d')
    pvoutputdata['t'] = datetime.today().strftime('%H:%M')
    pvoutputdata['v1'] = int(pvoutputdata['v1']*1000) #From kWh to Wh
    pvoutputdata['v2'] = int(pvoutputdata['v2'])
    pvoutputdata['c1'] = 2
    if (debug or debugdata): print(pvoutputdata)
    
    
    
    if(Pvoutputcfg['enabled'] and float(Pvoutputcfg['nextapicall_timestamp']) < time.time()):
        headers = {
            "X-Pvoutput-Apikey": Pvoutputcfg['apikey'],
            "X-Pvoutput-SystemId": Pvoutputcfg['siteid'],
            }
        
        res = requests.post(Pvoutputcfg['url'], headers=headers, data=pvoutputdata)
        setNextPVOAllowedTime()
        if (debug or debugdata): print(f'PVO data sent {res}')
        return
    else:
        return
# --------------------------------------------------------------------------- #
# Functions - rate limit management
# --------------------------------------------------------------------------- #

def setNextPVOAllowedTime():
    global Config, Pvoutputcfg
    #used for rate limit management to send data to PVO
    interval = 3600 / int(Pvoutputcfg['hitsperhour'])
    Config['pvoutput']['nextapicall_timestamp'] = str(time.time() + interval)
    setConfig()
    
# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    if(getConfig(ConfFile)):  
        data = getSun2000Data()
        if (debug or debugdata): print(data)
        sendEmonCMS(data) #send data to EmonCMS
        sendPVOutput(data) #send to PVOutput
    else:
        print('Can do nothing, no config found')