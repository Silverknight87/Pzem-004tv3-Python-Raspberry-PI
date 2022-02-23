#!/usr/bin/env python

"""

Driver for the PZEM-014 and PZEM-016 Energy monitors, for communication using the Modbus RTU protocol.

"""

__author__  = "Paul Burnell"
__license__ = "TBC"


import time

class interval():

    def __init__(self, interval, speed=0.01):    
        """  """
        self.interval = interval
        self.looptime = interval * speed
        self.previous = time.time()//interval*interval


    def ready(self):
        """ """
        time.sleep(self.looptime)
        timeNow = time.time()//self.interval*self.interval
        if timeNow >= (self.previous + self.interval):
            self.previous = timeNow
            return True
        else:
            return False

if __name__ == "__main__":

    ts = interval(5)
    stats = [999,0,0,0]       # min, max.avg, count, 
    maxDiff = 0

    while True:

        if ts.ready():
            results = [ts.previous,time.time()]
            results.append(round(((results[1]-results[0])*1000),3))
            if results[2] < stats[0]:
                stats[0] = results[2]
            if results[2] > stats[1]:
                stats[1] = results[2]
            stats[2] = round((((stats[3]*stats[2])+results[2])/(stats[3]+1)),1)
            stats[3] += 1

            print("Timestamped:{}\tActual:{}\tDiff:{}mS\t(min:{},max:{},avg:{})".format(*results+stats))
            #print("Actual time:"+str(time.time())+" Timestamped:"+str(ts.previous))