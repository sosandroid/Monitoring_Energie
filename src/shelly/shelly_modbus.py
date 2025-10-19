#####################################################
## Lecture des registres Modbus TCP du Shelly Pro 3EM
## Auteur : Sosandroid
## Date 2025-10-19
## Version : 1.0
## Description : Ce script lit les registres Modbus TCP du Shelly Pro 3EM pour les mettre à disposition d'une autre application. Permet de fournir des float ou int en fonction de l'usage. par exemple un PLC ne gère que des int.
#####################################################

from pymodbus.client import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder

# Configuration Modbus TCP
ip_address = "192.168.1.188" # Adresse IP du Shelly Pro 3EM
port = 502                   # Port Modbus TCP par défaut
unit_id = 1                  # ID de l'esclave Modbus

# Adresse du premier registre (exemple : 1000 pour un Input Register)
start_address = 1000
regsiters_length = 75  # Nombre de registres à lire

def read_inputRegisters_shelly(ip, port, unit, address, length):
    # Connexion au client Modbus TCP; récupération de la réponse brute et transmission
    # 
    client = ModbusTcpClient(ip, port)
    client.connect()
    try:
        response = client.read_input_registers(address, length, slave=unit)
        if not response.isError():
            return response.registers
        else:
            print(f"Erreur de lecture : {response}")
            return None
    finally:
        client.close()
        
def decode_float32_from_registers(registers):
    # Décodage des deux registres en un float 32 bits
    # Attention : l'ordre des registres dépend de l'endianness (Big Endian ou Little Endian)
    # Ici, on suppose que le Shelly Pro 3EM utilise le format Big Endian (le plus courant en Modbus)
    decoder = BinaryPayloadDecoder.fromRegisters(
        registers,
        byteorder=Endian.BIG,
        wordorder=Endian.LITTLE
    )
    return decoder.decode_32bit_float()
   
def decode_uint32_from_registers(registers): 
    # Décodage des deux registres en un uint 32 bits
    decoder = BinaryPayloadDecoder.fromRegisters(
        registers,
        byteorder=Endian.BIG,
        wordorder=Endian.LITTLE
    )
    return decoder.decode_32bit_uint()

def decode_bool_from_registers(registers, bit_index=0, return_bit=True):
    # Décodage d'un bit spécifique dans les registres
    decoder = BinaryPayloadDecoder.fromRegisters(
        registers,
        byteorder=Endian.BIG,
        wordorder=Endian.LITTLE
    )
    # Lire tous les bits des registres
    bits = decoder.decode_bits()
    if return_bit:
        return bits[bit_index]
    else:
        return bool(bits[bit_index])

def float_to_int(float_value, scaling_factor=100):
    # Convertir un float en int (tronquer la partie décimale)
    return round(float_value * scaling_factor)

def decode_shelly_data(ip, port, unit, address, length, to_int=False, scaling_factor=100):
    registers = read_inputRegisters_shelly(ip, port, unit, address, length)
    if registers is None:
        return None

    data = {}
    data['timestamp'] = decode_uint32_from_registers(registers[0:2]) # registers 0 1
    data['phaseA_error'] = decode_bool_from_registers(registers[2:3], bit_index=0) # registers 2
    data['phaseB_error'] = decode_bool_from_registers(registers[3:4], bit_index=0) # registers 3
    data['phaseC_error'] = decode_bool_from_registers(registers[4:5], bit_index=0) # registers 4
    data['neutral_error'] = decode_bool_from_registers(registers[5:6], bit_index=0) # registers 5
    data['phase_sequence_error'] = decode_bool_from_registers(registers[6:7], bit_index=0) # registers 6
    data['neutral_current'] = decode_float32_from_registers(registers[7:9]) # registers 7 8
    data['neutral_current_mismatch'] = decode_bool_from_registers(registers[9:10], bit_index=0) # registers 9
    data['neutral_overcurrent_error'] = decode_bool_from_registers(registers[10:11], bit_index=0) # registers 10
    data['total_current'] = decode_float32_from_registers(registers[11:13]) # registers 11 12
    data['total_active_power'] = decode_float32_from_registers(registers[13:15]) # registers 13 14
    data['total_apparent_power'] = decode_float32_from_registers(registers[15:17]) # registers 15 16
    data['phaseA_voltage'] = decode_float32_from_registers(registers[20:22]) # registers 20 21
    data['phaseA_current'] = decode_float32_from_registers(registers[22:24]) # registers 23 24
    data['phaseA_active_power'] = decode_float32_from_registers(registers[24:26]) # registers 24 25
    data['phaseA_apparent_power'] = decode_float32_from_registers(registers[26:28]) # registers 26 27
    data['phaseA_power_factor'] = decode_float32_from_registers(registers[28:30]) # registers 28 29
    data['phaseA_overpower_error'] = decode_bool_from_registers(registers[30:31], bit_index=0) # registers 30
    data['phaseA_overvoltage_error'] = decode_bool_from_registers(registers[31:32], bit_index=1) # registers 31
    data['phaseA_overcurrent_error'] = decode_bool_from_registers(registers[32:33], bit_index=0) # registers 32
    data['phaseA_frequency'] = decode_float32_from_registers(registers[33:35])  # registers 33 34
    data['phaseB_voltage'] = decode_float32_from_registers(registers[40:42]) # registers 40 41
    data['phaseB_current'] = decode_float32_from_registers(registers[42:44]) # registers 43 44
    data['phaseB_active_power'] = decode_float32_from_registers(registers[44:46]) # registers 45 46
    data['phaseB_apparent_power'] = decode_float32_from_registers(registers[46:48]) # registers 47 48
    data['phaseB_power_factor'] = decode_float32_from_registers(registers[48:50]) # registers 48 49
    data['phaseB_overpower_error'] = decode_bool_from_registers(registers[50:51], bit_index=0) # registers 50
    data['phaseB_overvoltage_error'] = decode_bool_from_registers(registers[51:52], bit_index=1) # registers 51
    data['phaseB_overcurrent_error'] = decode_bool_from_registers(registers[52:53], bit_index=0) # registers 52
    data['phaseB_frequency'] = decode_float32_from_registers(registers[53:55])  # registers 53 54
    data['phaseC_voltage'] = decode_float32_from_registers(registers[60:62]) # registers 60 61
    data['phaseC_current'] = decode_float32_from_registers(registers[62:64]) # registers 63 64
    data['phaseC_active_power'] = decode_float32_from_registers(registers[64:66]) # registers 65 66
    data['phaseC_apparent_power'] = decode_float32_from_registers(registers[66:68]) # registers 67 68
    data['phaseC_power_factor'] = decode_float32_from_registers(registers[68:70]) # registers 68 69
    data['phaseC_overpower_error'] = decode_bool_from_registers(registers[70:71], bit_index=0) # registers 70
    data['phaseC_overvoltage_error'] = decode_bool_from_registers(registers[71:72], bit_index=1) # registers 71
    data['phaseC_overcurrent_error'] = decode_bool_from_registers(registers[72:73], bit_index=0) # registers 72
    data['phaseC_frequency'] = decode_float32_from_registers(registers[73:75])  # registers 73 74

    if to_int:
        for key in data:
            if isinstance(data[key], float):
                data[key] = float_to_int(data[key], scaling_factor)

    return data

# Exemple d'utilisation
if __name__ == "__main__":
    shelly_data = decode_shelly_data(
        ip_address,
        port,
        unit_id,
        start_address,
        regsiters_length,
        to_int=True,
        scaling_factor=100
    )
    if shelly_data is not None:
        for key, value in shelly_data.items():
            print(f"{key}: {value}")