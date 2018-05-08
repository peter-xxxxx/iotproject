from __future__ import print_function
from device import Buzzer, myLcd, sock, Display, SendMessage
import time, sys, signal, atexit
from mpu6050_class import sensorObj
from device import switch
import numpy as np
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
import csv

def Evaluate(acc, gyr, template):
    Users = np.concatenate((acc, gyr), axis = 1)
    standard = np.array(template)
    dist, _ = fastdtw(Users, standard, dist = euclidean)
    print(dist)
    if (dist > 1000):
        return False
    else:
        return True

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

    # Read the template
    csvFile = open("template.csv", "r")
    reader = csv.reader(csvFile)
    standard = []
    for row in reader:
        temp = []
        for i in range(6):
            temp.append(float(row[i]))
        standard.append(temp)
    csvFile.close()

    # The initial value for variables
    color = 0
    store_acc = []
    store_gyr = []
    now = False
    pre = False
    Display("Ready")
    myLcd.setColor(0, 0, 255)

    while (1):
        sensor.UpdateData()

        # UDP
        SendMessage(sensor.Euler[0],sensor.Euler[1],sensor.Euler[2],color)

        now = switch.read()
        if ((not pre) & now):
            myLcd.setColor(255, 255, 0) # Yellow
            Display("Start")

        if (now):
            store_acc.append(sensor.Acc)
            store_gyr.append(sensor.Gyr)
            color = 1
        if (pre & (not now)):
            Judge = Evaluate(np.array(store_acc),np.array(store_gyr),standard)
            if Judge:
                myLcd.setColor(0, 255, 0)   # Green
                Display("Correct","Press")
                Buzzer(1, 0, 1)
            else:
                myLcd.setColor(255, 0, 0)   # Red
                Display("Wrong","Press")
                Buzzer(0.5, 0.2, 3)
            while (not switch.read()):
                pass
            time.sleep(1)
            store_acc = []
            store_gyr = []
            Display("Ready")
            myLcd.setColor(0, 0, 255)
            color = 0
        pre = now

if __name__ == '__main__':
    main()
