# Reading PZEM-004t power sensor (new version v3.0) through Modbus-RTU protocol over TTL UART
# Run as:
# python pzemv3.py

# To install dependencies: 
# pip install modbus-tk
# pip install pyserial

import serial
import time
import json
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu

# Connect to the sensor
sensor = serial.Serial(
                       port='/dev/ttyUSB0',
                       baudrate=9600,
                       bytesize=8,
                       parity='N',
                       stopbits=1,
                       xonxoff=0
                      )

master = modbus_rtu.RtuMaster(sensor)
master.set_timeout(2.0)
master.set_verbose(True)


        # Changing power alarm value to 100 W 
        # master.execute(1, cst.WRITE_SINGLE_REGISTER, 1, output_value=100)

dict_payload = dict()

while True:

        data = master.execute(1, cst.READ_INPUT_REGISTERS, 0, 10)

        dict_payload["voltage"] = data[0] / 10.0 # [V]
        dict_payload["current"] = (data[1] + (data[2] << 16)) / 1000.0 # [A]
        dict_payload["power"] = (data[3] + (data[4] << 16)) / 10.0 # [W]
        dict_payload["energy"] = (data[5] + (data[6] << 16))/1000 # [kWh]
        dict_payload["frequency"] = data[7] / 10.0 # [Hz]
        dict_payload["powerFactor"] = data[8] / 100.0
        dict_payload["alarm"] = data[9] # 0 = no alarm
        str_payload = json.dumps(dict_payload, indent=2)        
        print(str_payload)

        time.sleep(2)
		
		
try:
    master.close()
    if sensor.is_open:
        sensor.close()
except:
    pass
