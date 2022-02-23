# Python code to set address on Pzem-004T v3 different from the default factory address. Address is being set to "3" in this example. Modify as appropriate.

# All credits to original Author Paul. I just made some tweaks here and there to fit my requirements.

# Used when you are connecting more than 1 Pzem-004T v3 to the usb to serial adapter on the raspberry PI.Each pzem needs to have a unique address that is referenced again in the read_pzem.py to reach each pzem one after the other.

# Note that the external Usb to serial i am using on my PI has tty address /dev/ttyUSB0, might be differnt on your device. 

# Didn't investigate much but i was not able to get the RX/TX GPIO on the PI working instead of the usb to serial.

#!/usr/bin/env python

"""

Driver for the PZEM-014 and PZEM-016 Energy monitors, for communication using the Modbus RTU protocol.

"""

__author__  = "Paul Burnell"
__license__ = "TBC"

try:
    import json
    import minimalmodbus
except ImportError:
    print("Cannot import minimalmodbus, is it installed?\nExiting...")
    quit()

class pzem(minimalmodbus.Instrument):

    def __init__(self, serialPort, slaveAddress=1):
        """
        Create monitor device instance
        """
        minimalmodbus.Instrument.__init__(self, serialPort, slaveAddress)
        self.serial.timeout = 0.1
        self.serial.baudrate = 9600



    def setSlaveAddress(self, address):
        """
        Set a new slave address (1 to 247), initially set to 1 from factory.
        Each device must have a unique address, Max of 31 devices per network.
        """
        return self.write_register(2,address,0,6)

if __name__ == "__main__":

    import time

    serialPort = "/dev/ttyUSB0"

    # # # Using a single devive with factory default address of "1"
    #pz = pzem(serialPort)

    # Using a slave address other than the factory default of "1". Changing address from default of 1 to 3 in this example.
    slaveAddress = 1
    pz = pzem(serialPort, slaveAddress)

    pz.setSlaveAddress(3)
