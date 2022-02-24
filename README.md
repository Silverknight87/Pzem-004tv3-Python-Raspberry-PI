# Pzem-004tv3-Python-Raspberry-PI
**Python code to Read Multiple PZEM 004t connected in parallel to USBtoSerial converter on Raspberry PI (Model 3B) and output JSON objects to MQTT**

Code first posted by Paul(PB66) somewhere on this [thread](https://community.openenergymonitor.org/t/pzem-016-single-phase-modbus-energy-meter/7780). I just made some simple modifications to format output to JSON and sent to MQTT broker for consumption on Nodered or elsewhere. Note: I am not a programmer, all modifications i made are purely based on my half knowledge and Internet search, please excuse if some of the stuff i have done looks lame, what matters is the code is working for me and is giving desired results for over 1 month. Feedback for improvements always welcome.

Steps:

Listing some basic instructions here but more notes/instructuons in each .py file on this repo.

1. Connect PZEM004t v3 to Raspberry Pi as shown in the image below. Each PZEM needs to be assigned a unique address 1-10 separately before connecting them all together in parallel.
2. The PZEMs need AC input for the Power monitoring chip to work. The 5v input to the UART does not power the PZEM.
4. pip install the required dependencies "pip install minimalmodbus"; "pip install paho-mqtt"
5. Set unique address for each Pzem using setaddress.py. Read instructions inside file.
6. The image below shows 3 PZem's connected in Parallel. but my example code in read_pzem.py is configured to read 6 pzem's addressed 1-6. Change this line "slaveAddresses = [1,2,3,4,5,6]" in the read_pzem.py file to the addresses you have set for your pzems.
7. ESP8266 devices needed Schottky diodes on the RX lines to operate correctly as per instructions on the Internet but i have not had any issues connecting the PZEM's directly in parallel to the PI USB to serial
8. See instructions inside "read_pzem.py" before finally running it. The code is currently set to send json objects for each pzem to the configured MQTT broker. Be sure to change the MQTT broker address to your Mqtt broker and mqtt topic to your desired topic.
9. If you just want to see JSON output on console and not send to mqtt, feel free to uncomment and comment lines 102 and 103 in read_pzem.py
10. I have set up read_pzem.py to run at startup and loop for ever. So, whenever my PI boots up, i keep getting data on the mqtt topic as long as the PZEM's have mains power.
11. I am reading a total of 3 phases of Load and 3 phases of solar generation as of now and writing the required data to Influx db via nodered and also doing some computations on the data as per my need.
12. I am also picking up kwh data via mqtt on home assistant and feeding it to the Energy Dashboard. Unfortunately, PZEM 004t v3 does not have the capability to differenciate Energy being Imported and exported so i really do not have the visibility into how much is being exported on Home assistant. I just need to manually see how much was generated and how much is consumed and then do a sum or different to figure out how much excess was exported or imported. This is the only part i hate the PZEM's for, everthign else works perfectly.
 

![alt text](https://github.com/vjversatile/Pzem-004tv3-Python-Raspberry-PI/blob/master/Pi%20Pzem.png?raw=true)


