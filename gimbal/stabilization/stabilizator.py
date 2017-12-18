# -*- coding: utf-8 -*-
'''
Created on 24 ene. 2017

@author: david
'''
from time import sleep

from config import Configuration
from sensor.imu6050dmp import Imu6050Dmp
from sensor.imu6050 import Imu6050
from sensor.sensor_dummy import SensorDummy
from stabilization.pid import Pid


class Stabilizator(object):
    '''
    Stabilizes a surface according to a IMU-sensor
    '''

    def __init__(self, sensorType, driver, pidPeriod, numAxis):
        '''
        Constructor
        '''
        
        if sensorType == Configuration.VALUE_IMU_CLASS_6050:
            self._sensor = Imu6050()
        elif sensorType == Configuration.VALUE_IMU_CLASS_6050_DMP:
            self._sensor = Imu6050Dmp()
        else:
            self._sensor = SensorDummy()
            
        self._driver = driver
        self._pid = Pid(pidPeriod, numAxis, self.readAngles, self.setOutput, "stabilizator")
        
        
    def setPidConstants(self, kp, ki, kd):
        """
        Sets the pid constants
        @param kp: Array of propotional constants
        @param ki: Array of integral constants
        @param kd: Array of derivative constants
        """
        
        self._pid\
            .setProportionalConstants(kp)\
            .setIntegralConstants(ki)\
            .setDerivativeConstants(kd)        
        
        
    def start(self):
        """
        Starts stabilizator
        """
        
        self._driver.start()
        sleep(1)
        self._sensor.start()        
        self._pid.start()
    
    
    def stop(self):
        """
        Stops stabilizator
        """
        
        self._pid.stop()
        self._driver.stop()
        self._sensor.stop()
    
    
    def readAngles(self):
        """
        Reads angles from IMU
        """
        
        self._sensor.refreshState()
        angles = self._sensor.readDeviceAngles()
        
        return angles[:2]
    
    
    def setOutput(self, output):
        """
        Sets output into driver
        """
        
        #TODO Lock pid integral when output is out of motor range
        self._driver.rotateX(-output[0])
        self._driver.rotateY(output[1])
        
        
