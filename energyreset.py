# Python code to reset Energy on Pzem-004T v3. Worked initially but have been getting an error later i think, didnt tshoot.

# need to connect one pzem at a time to the PI Serial and reset the PZEM's internal KWH counter to 0.

# All credits to original Author Paul (Pb66). I just made some tweaks here and there to fit my requirements.


import minimalmodbus

pz = minimalmodbus.Instrument('/dev/ttyUSB0', 6)
pz.serial.baudrate = 9600

pz._performCommand(66,'')