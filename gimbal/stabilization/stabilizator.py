# -*- coding: utf-8 -*-
'''
Created on 24 ene. 2017

@author: david
'''
from stabilization.pid import Pid


class Stabilizator(object):
    '''
    Stabilizes a surface according to a IMU-sensor
    '''

    def __init__(self, sensor, driver, pidPeriod, numAxis):
        '''
        Constructor
        '''
        
        self._sensor = sensor
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
            .setIntegralConstants(kp)\
            .setDerivativeConstants(kp)        
        
        
    def start(self):
        """
        Starts stabilizator
        """
        
        self._sensor.start()
        self._driver.start()
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
        
        