#!/usr/bin/python

# python code to read multiple Pzem-004T v3 connected to a single PI. 

# All credits to original Author Paul (Pb66). I just made some tweaks here and there to fit my requirements.

# Note that i am using a external Usb to serial to connect multiple PZEMs to my PI. tty address on my Pi is /dev/ttyUSB0, might be differnt on your device. Connected usb devices can be found using ls /dev/tty* | grep USB on linux

# set slave addresses futher below depending on how many devices you have connected and what their addresses are.

# Didn't investigate much but i was not able to get the RX/TX GPIO on the PI working so using the usb to serial adapter instead.

# the following code will not print anything to console, it will read each pzem one after the other and publish to output to mqtt broker set further below in json format. if you need to debug uncomment  print(json_msg)

####### USER SETTINGS ######
serialPort = "/dev/ttyUSB0"
# device addresses need to be set first on each pzem separately using setaddress.py
slaveAddresses = [1,2,3,4,5,6]
interval = 5
debug = False
#################################################################

import timestamp
import pzem
#import the paho.mqtt.client before hand using pip install paho-mqtt
import paho.mqtt.client as mqtt 
import json

from time import sleep

def on_connect(client, userdata, flags, rc):

    if rc == 0:

        print("Connected to broker")

        global Connected                #Use global variable
        Connected = True                #Signal connection

    else:

        print("Connection failed")

Connected = False #global variable for the state of the connection

# Your MQTT broker IP, change to your mqtt broker address or dns name.
broker_address="192.168.111.92"

#print("creating new paho mqtt instance")
client = mqtt.Client("P1")


client.on_connect= on_connect
print("connecting to mqtt broker.....")
client.connect(broker_address, keepalive=30) #connect to broker

client.loop_start()

while Connected != True:    #Wait for connection
    sleep(0.1)





try:
    while True:
       ts = timestamp.interval(interval)
       device = {}
       data = {}

       for i in slaveAddresses:
           try:
               device[i] = pzem.pzem(serialPort, i)
               if debug:
                   device[i].debug = True
           except Exception as e:
               print("Device:" + str(i) + ", Setup Error:" + str(e))

       try:
           while True:
               if ts.ready():
                   for i in device:
                       data[i] = False
                       try:
                           data[i] = device[i].getData()
                       except IOError as e:
                           print("Device:" + str(device[i].address) + ", IOError:" + str(e))
                       except ValueError as e:
                           print("Device:" + str(device[i].address) + ", ValueError:" + str(e))
                       except TypeError as e:
                           print("Device:" + str(device[i].address) + ", TypeError:" + str(e))
                       except Exception as e:
                           print("Device:" + str(device[i].address) + ", Error:" + str(e))
                       else:
                           if debug:
                               print("Succesfully read device:" + str(device[i].address) + ", Data:" + str(data[i]))

                       if data[i]:
                           value = { device[i].address : data[i] }
                           json_msg = json.dumps(value, indent = 4)
                           #print(json_msg)
                           client.publish("pi/readpzem",json_msg)
                           sleep (0.5)
                       else:
                           if debug:
                               print("No data found for device:" + str(device[i].address))

#       except KeyboardInterrupt:
#           print("Exiting...")                         # Gracefully exit on "CTRL-C"
       except Exception as e:
           print(e)
except KeyboardInterrupt:
 
    client.disconnect()
    client.loop_stop()