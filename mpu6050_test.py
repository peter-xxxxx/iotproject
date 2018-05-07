from __future__ import print_function
import time, sys, signal, atexit
import pyupm_mpu9150 as sensorObj
import socket, math

def main():

    """
    Initialization
    """
    # Instantiate an MPU60X0 on I2C bus 0
    sensor_1 = sensorObj.MPU60X0()

    ## Exit handlers ##
    # This function stops python from printing a stacktrace when you hit control-C
    def SIGINTHandler(signum, frame):
        raise SystemExit

    # This function lets you run code on exit
    def exitHandler():
        print("Exiting")
        sys.exit(0)

    # UDP Initialization
    UDP_IP = "192.168.0.105"
    UDP_PORT = 6001
    MESSAGE = ""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Register exit handlers
    atexit.register(exitHandler)
    signal.signal(signal.SIGINT, SIGINTHandler)

    sensor_1.init()
    sensor_1.enableTemperatureSensor(False)
    if (not sensor_1.setDigitalLowPassFilter(20)):
        print("Failed to set up filter")
    #sensor_2.init()

    sensor_1.setAccelerometerScale(3)
    sensor_1.setGyroscopeScale(2)
    x = sensorObj.new_floatp()
    y = sensorObj.new_floatp()
    z = sensorObj.new_floatp()

    # Sample frequency
    sampleFreq = 5
    sampleTime = 1.0 / sampleFreq

    while (1):
        # Update the data in MPU
        sensor_1.update()

        """
        Get raw data from Accelerometer and Gyroscope
        """
        sensor_1.getAccelerometer(x, y, z)
        ax = sensorObj.floatp_value(x)
        ay = sensorObj.floatp_value(y)
        az = sensorObj.floatp_value(z)

        sensor_1.getGyroscope(x, y, z)
        gx = sensorObj.floatp_value(x)
        gy = sensorObj.floatp_value(y)
        gz = sensorObj.floatp_value(z)

        """
        Send out message to server
        """

        if (math.fabs(az) >= 0.02):
            Pitch = math.atan(ax / az) * (180 / math.pi)
            Roll = math.atan(ay / az) * (180 / math.pi)
        else:
            Pitch = 90
            Roll = 0
        MESSAGE = "{:.0f} {:.0f} 0 0".format(Pitch, Roll)
        sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

if __name__ == '__main__':
    main()
