
# Python code to reset Energy on Pzem-004T v3


import minimalmodbus

pz = minimalmodbus.Instrument('/dev/ttyUSB0', 1)
pz.serial.baudrate = 9600

pz._performCommand(66, '')
