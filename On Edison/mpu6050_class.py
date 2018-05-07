from __future__ import print_function
import time, sys, signal, atexit
import pyupm_mpu9150
import math
import numpy as np
from device import Display, switch

"""
================================================================================
Class sensorObj
================================================================================
Heritaged from pyupm_mpu9150, realized self-edited functions
================================================================================
"""
class sensorObj(pyupm_mpu9150.MPU60X0):

    """
    ================================================================================
    Constant class
    ================================================================================
    Use a dictionary to store the neccessary constants in calculation, once the
    constant was set, it can not be changed or re-assigned
    ================================================================================
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

    """
    ================================================================================
    Initialization Function
    ================================================================================
    Initialize the sensor use the init function heritaged from MPU60X0 class, then
    prepare the neccessary parameters for the sensorObj class
    ================================================================================
    """
    def __init__(self, frequency = 200, # Hz
                 avgtime = 3,           # number of sampling times over which we take average
                 caltimes = 200,        # number of sampling times for calibration
                 g = 9.802,             # Gravity acceleration value in New York City
                 accscale = 3,
                 gyrscale = 3):

        super(sensorObj, self).__init__()

        # Set up constants
        self.const.FREQUENCY  = frequency
        self.const.AVGTIME    = avgtime
        self.const.CALTIMES   = caltimes
        self.const.G          = g
        self.const.SAMPLETIME = 1.0 / (self.const.FREQUENCY * self.const.AVGTIME)

        # Parameters
        self.GyrBias = np.array([0, 0, 0])
        self.Quat    = np.array([0, 0, 0, 0])

        #Initialize the sensor
        self.init()
        self.enableTemperatureSensor(False)
        self.setAccelerometerScale(accscale)
        self.setGyroscopeScale(gyrscale)
        self.Calibration()

    """
    ================================================================================
    setGyroscopeScale
    ===============================================================================
    Rewrite the function setGyroscopeScale(gyrscale) from class MPU60X0,
    to make sure the parameter on the sensor is identical to the on in the program
    ===============================================================================
    """
    def setGyroscopeScale(self, gyrscale):
        if (gyrscale == 0):
            self.SCALEFACT = 32767.0 / 250.0
        elif (gyrscale == 1):
            self.SCALEFACT = 32767.0 / 500.0
        elif (gyrscale == 2):
            self.SCALEFACT = 32767.0 / 1000.0
        elif (gyrscale == 3):
            self.SCALEFACT = 32767.0 / 2000.0
        else:
            raise StandardError, "The scale of gyroscope Out of Range"
        super(sensorObj, self).setGyroscopeScale(gyrscale)

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
    def RecieveData(self):

        GyrBias = self.GyrBias

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
            self.update()

            # Acceleration Data
            self.getAccelerometer(x, y, z)
            ax += pyupm_mpu9150.floatp_value(x)
            ay += pyupm_mpu9150.floatp_value(y)
            az += pyupm_mpu9150.floatp_value(z)

            # Angular Speed Data
            self.getGyroscope(x, y, z)
            gx += pyupm_mpu9150.floatp_value(x)
            gy += pyupm_mpu9150.floatp_value(y)
            gz += pyupm_mpu9150.floatp_value(z)

            # Pause time for next sampling
            time.sleep(self.const.SAMPLETIME)

        Acc = np.array([ax, ay, az])
        Gyr = np.array([gx, gy, gz]) - GyrBias
        Acc = Acc * self.const.G / self.const.AVGTIME
        Gyr = Gyr * math.pi / (self.const.AVGTIME * 180 * self.SCALEFACT)

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
    def Calibration(self):

        # Calibrate the Gyroscope
        gx = 0
        gy = 0
        gz = 0

        Display("Calibration", "Press Button")
        while (not switch.read()):
            pass
        Display("Calibrating")

        for i in range(self.const.CALTIMES):
            _, Gyr = self.RecieveData()
            gx += Gyr[0] * 180 * self.SCALEFACT / math.pi
            gy += Gyr[1] * 180 * self.SCALEFACT / math.pi
            gz += Gyr[2] * 180 * self.SCALEFACT / math.pi
        gx = gx / self.const.CALTIMES
        gy = gy / self.const.CALTIMES
        gz = gz / self.const.CALTIMES
        self.GyrBias = np.array([gx, gy, gz])
        #Calculate the Quaternion
        Quat = np.array([0, 0, 0, 0])
        acc, _ = self.RecieveData()

        pitch = math.asin(acc[1] / acc[2])
        roll  = math.asin(acc[0] / acc[2])
        yaw   = 0

        self.Quat[0] = (math.cos(yaw / 2) * math.cos(pitch / 2) * math.cos(roll / 2) +
                        math.sin(yaw / 2) * math.sin(pitch / 2) * math.sin(roll / 2))
        self.Quat[1] = (math.cos(yaw / 2) * math.sin(pitch / 2) * math.cos(roll / 2) +
                        math.sin(yaw / 2) * math.cos(pitch / 2) * math.sin(roll / 2))
        self.Quat[2] = (math.cos(yaw / 2) * math.cos(pitch / 2) * math.sin(roll / 2) -
                        math.sin(yaw / 2) * math.sin(pitch / 2) * math.cos(roll / 2))
        self.Quat[3] = (math.cos(yaw / 2) * math.sin(pitch / 2) * math.sin(roll / 2) -
                        math.sin(yaw / 2) * math.cos(pitch / 2) * math.cos(roll / 2))

        Display("Let's FENCE!")
