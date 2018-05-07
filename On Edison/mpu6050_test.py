from __future__ import print_function
from device import Buzzer, myLcd, sock
import time, sys, signal, atexit
from mpu6050_class import sensorObj

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

    while (1):
        acc, gyr = sensor.RecieveData()
        print(acc)
        print(gyr)
        print("="*50)

if __name__ == '__main__':
    main()
