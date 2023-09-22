
"""
Connect Huawei SUN2000 inverter to get production power and push result to EmonCMS
Uses pyModbus & Request
Personnalise send_emonCMS() to fit your settings

Registers list from https://github.com/olivergregorius/sun2000_modbus

"""

# --------------------------------------------------------------------------- #
# import the various client implementations
# --------------------------------------------------------------------------- #
from time import sleep
import requests
import json
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

def get_sun2000_modbus(debug = False):
    unit = 1
    host = "192.168.1.180"
    port = "502"
    
    if (debug):
        pymodbus_apply_logging_config("DEBUG")
     
    client = ModbusTcpClient(
            host,
            port=port,
            framer=ModbusSocketFramer,
            timeout=4,
            retries=3,
            retry_on_empty=True,
            # close_comm_on_error=False,
            # strict=True,
            #source_address=("192.168.0.57", 0),
        )
    client.connect()
    sleep(1) # Connexion stabilization
    # power = client.read_holding_registers(32080, 2, unit) # active power, length 2, factor 1
    power = client.read_holding_registers(32069, 9, unit) # voltage and current on all 3 phases
    sleep(0.5) # Connexion stabilization
    temp = client.read_holding_registers(32087, 1, unit) #internal temperature, length 1, factor 10
    # sleep(0.5)
    # dailyEnergy = client.read_holding_registers(32114, 2, unit)  # Energie du jour facteur 100
    client.close()

    # power calculation
    v1 = power.registers[0] /10
    v2 = power.registers[1] /10
    v3 = power.registers[2] /10
    i1 = (power.registers[3]*65535+power.registers[4])/1000
    i2 = (power.registers[5]*65535+power.registers[6])/1000
    i3 = (power.registers[7]*65535+power.registers[8])/1000
    
    p = v1*i1+v2*i2+v3*i3
    
    #p = power.registers[0]*65535+power.registers[1]
    t = temp.registers[0]/10
    
    return dict(PUI_PROD=p, TEMP_INT=t)

    
def send_emonCMS():
    # Récupère les données avant de les envoyer
    data = get_sun2000_modbus()
    params = dict(node='ONDULEUR', fulljson=json.dumps(data), apikey='YOUR EMONCMS API KEY')
    # print(data)
    # print(params)
    url = 'http://192.168.1.1/input/post'
    res = requests.get(url, params=params)

    

if __name__ == "__main__":
    send_emonCMS() #send data to EmonCMS
