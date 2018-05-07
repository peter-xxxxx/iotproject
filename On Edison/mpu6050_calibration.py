from __future__ import print_function
import time, sys, signal, atexit
import pyupm_mpu9150
import socket, math
import numpy as np


class sensorObj(pyupm_mpu9150):

    """
    Constant class
    """
    class const(object):
        class ConstError(TypeError): pass
        class ConstCaseError(ConstError): pass

        def __setattr__(self, name, value):
            if name in self.__dict__:
                raise self.ConstError("can't change const %s" % name)
            if not name.isupper():
                raise self.ConstCaseError('const name "%s" is not all uppercase' % name)
            self.__dict__[name] = value

    def __init__(self, frequency = 200, # Hz
                 avgtime = 3,           # number of sampling times over which we take average
                 caltimes = 200,        # number of sampling times for calibration
                 g = 9.802,             # Gravity acceleration value in New York City
                 accscale = 3,
                 gyrscale = 3):
        # Set up necessary constants
        self.GyrBias = np.array([0, 0, 0, 0])
        self.const.FREQUENCY  = frequency
        self.const.AVGTIME    = avgtime
        self.const.CALTIMES   = caltimes
        self.const.G          = g
        self.const.SAMPLETIME = 1.0 / (const.FREQUENCY * const.AVGTIME)

        #Initialize the sensor
        sensor.init()
        sensor.enableTemperatureSensor(False)
        sensor.setAccelerometerScale(accscale)
        sensor.setGyroscopeScale(gyrscale)

    """
    ================================================================================
    RecieveData
    ================================================================================
    Input:
        sensor: a object of the IMU sensor
    Output:
        Acc: Acceleration data, a vector with 3 elements of float, representing x y and z
             axis, respectively.
        Gyr: Angular speed data, a vector with 3 elemenets of float, representing x
             y and z axis, respectively
    ================================================================================
    Get the IMU data from sensor. Withdraw the raw data for AVGTIME times, then
    take an average on them. The sampleing time is stored in the constant SAMPLETIME.
    ================================================================================
    """
    def RecieveData():

        sensor = self.sensor

        # Initialize the accumulative variables
        x = pyupm_mpu9150.new_floatp()
        y = pyupm_mpu9150.new_floatp()
        z = pyupm_mpu9150.new_floatp()
        ax = 0
        ay = 0
        az = 0
        gx = 0
        gy = 0
        gz = 0

        # Get the raw data
        for i in range(self.const.AVGTIME):
            sensor.update()

            # Acceleration Data
            sensor.getAccelerometer(x, y, z)
            ax += pyupm_mpu9150.floatp_value(x)
            ay += pyupm_mpu9150.floatp_value(y)
            az += pyupm_mpu9150.floatp_value(z)

            # Angular Speed Data
            sensor.getGyroscope(x, y, z)
            gx += pyupm_mpu9150.floatp_value(x)
            gy += pyupm_mpu9150.floatp_value(y)
            gz += pyupm_mpu9150.floatp_value(z)

            # Pause time for next sampling
            time.sleep(self.const.SAMPLETIME)

        Acc = np.array([ax, ay, az])
        Gyr = np.array([gx, gy, gz]) - GyrBias
        Acc = Acc * const.G / const.AVGTIME
        Gyr = Gyr * math.pi / (const.AVGTIME * 180)

        return Acc, Gyr

    """
    ================================================================================
    Calibration
    ================================================================================
    Input:
        sensor: a object of the IMU sensor
    Output:
        GyrBias*: the bias of Gyroscope, a vector of 3 elemenets of float,
                  representing x y and z axis, respectively. This parameter should
                  be set as a constant
        Quat:     Quanternion, a vector of 4 elements of floats, representing a b
                  c and d, respectively. (a + bi + cj + dk)
    ================================================================================
    Calibrate the sensor at stable situation, giving out the bias and the initial
    Quaternion
    ================================================================================
    """
    def Calibration(sensor):

        # Calibrate the Gyroscope
        gx = 0
        gy = 0
        gz = 0
        for i in range(const.CALTIMES):
            _, Gyr = RecieveData(sensor)
            gx += Gyr[0] * 180 / math.pi
            gy += Gyr[1] * 180 / math.pi
            gz += Gyr[2] * 180 / math.pi
        gx = gx / const.CALTIMES
        gy = gy / const.CALTIMES
        gz = gz / const.CALTIMES
        GyrBias = np.array([gx, gy, gz])
        #Calculate the Quaternion
        Quat = np.array([0, 0, 0, 0])
        acc, _ = RecieveData(sensor)

        pitch = math.asin(acc[1] / acc[2])
        roll  = math.asin(acc[0] / acc[2])
        yaw   = 0

        Quat[0] = (math.cos(yaw / 2) * math.cos(pitch / 2) * math.cos(roll / 2) +
                   math.sin(yaw / 2) * math.sin(pitch / 2) * math.sin(roll / 2))
        Quat[1] = (math.cos(yaw / 2) * math.sin(pitch / 2) * math.cos(roll / 2) +
                   math.sin(yaw / 2) * math.cos(pitch / 2) * math.sin(roll / 2))
        Quat[2] = (math.cos(yaw / 2) * math.cos(pitch / 2) * math.sin(roll / 2) -
                   math.sin(yaw / 2) * math.sin(pitch / 2) * math.cos(roll / 2))
        Quat[3] = (math.cos(yaw / 2) * math.sin(pitch / 2) * math.sin(roll / 2) -
                   math.sin(yaw / 2) * math.cos(pitch / 2) * math.cos(roll / 2))
        return Quat

def main():

    """
    Initialization
    """
    # Instantiate an MPU60X0 on I2C bus 0
    sensor = pyupm_mpu9150.MPU60X0()

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

    sensor.init()
    sensor.enableTemperatureSensor(False)
    #sensor_2.init()

    sensor.setAccelerometerScale(3)
    sensor.setGyroscopeScale(3)

    q = Calibration(sensor)
    print(q)
    while (1):
        acc, gyr = RecieveData(sensor)
        print(acc)
        print(gyr)
        print("="*50)
        time.sleep(0.5)

if __name__ == '__main__':
    main()
