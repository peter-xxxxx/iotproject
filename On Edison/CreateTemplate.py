from __future__ import print_function
from device import Buzzer, myLcd, sock
import time, sys, signal, atexit
from mpu6050_class import sensorObj
from device import switch, Display, myLcd
import numpy as np
import csv

def main():

    """
    Initialization
    """
    # Initialize the sensor
    sensor = sensorObj()

    ## Exit handlers ##
    # This function stops python from printing a stacktrace when you hit control-C
    def SIGINTHandler(signum, frame):
        raise SystemExit

    # This function lets you run code on exit
    def exitHandler():
        print("Exiting")
        sys.exit(0)

    # Register exit handlers
    atexit.register(exitHandler)
    signal.signal(signal.SIGINT, SIGINTHandler)

    Display("Ready")
    while(not switch.read()):
        pass
    time.sleep(2)

    store_acc = []
    store_gyr = []
    now = False
    pre = False
    while (1):
        sensor.UpdateData()
        now = switch.read()
        if ((not pre) & now):
            myLcd.setColor(255, 0, 0)
            Display("Start")

        if (now):
            store_acc.append(sensor.Acc)
            store_gyr.append(sensor.Gyr)
        if (pre & (not now)):
            myLcd.setColor(255, 255, 255)
            Display("Done")
            break
        pre = now

    csvFile = open("template.csv", "w")
    writer= csv.writer(csvFile)

    for i in range(len(store_acc)):
        d = ["{:.4f}".format(store_acc[i][0]),
             "{:.4f}".format(store_acc[i][1]),
             "{:.4f}".format(store_acc[i][2]),
             "{:.4f}".format(store_gyr[i][0]),
             "{:.4f}".format(store_gyr[i][1]),
             "{:.4f}".format(store_gyr[i][2])]
        writer.writerow(d)
    csvFile.close()

    while (not switch.read()):
        pass

if __name__ == '__main__':
    main()
