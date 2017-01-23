# -*- coding: utf-8 -*-

'''
Created on 23/01/2017

@author: david
'''
import logging

from random import uniform, seed
from copy import deepcopy


class SensorDummy(object):
    '''
    IMU sensor dummy for testing
    '''
    
    ERROR_ANGLE_SPEED_DISTRIBUTION = [-1.0, 1.0] #[-0.1, 0.15]
    ERROR_ANGLE_DISTRIBUTION = [-0.0, 0.0] #[-0.08, 0.1]
    ERROR_ACCEL_DISTRIBUTION = [-0.1, 0.1] #[-0.1, 0.15]
    
    def __init__(self, addNoise=False):
        
        self._addNoise = addNoise
        if self._addNoise:        
            seed()
        self._currentAngles = [0.0] * 3
    
    
    def _noisify(self, data, distribution):

        inputData = deepcopy(data)
        noisedList = [item + uniform(distribution[0], distribution[1]) for item in inputData]

        return noisedList


    def setCurrentAngles(self, angles):
        
        self._currentAngles = angles

    def readAngles(self):
        '''
        Positive angles are CCW for axis Z
        '''
        
        state = self._drone.getState()        
        angles = \
            self._noisify(state._angles, SensorDummy.ERROR_ANGLE_DISTRIBUTION) \
            if self._addNoise \
            else deepcopy(state._angles) 
        
        return angles

    
    def readDeviceAngles(self):

        return self.readAngles()

    
    def resetGyroReadTime(self):        
        pass

    
    def refreshState(self):
        pass
    
    
    def start(self):
        
        text = "Using dummy IMU." 

        logging.info(text)
        
    
    def calibrate(self):
        pass
    
    def stop(self):
        pass
    
    def getMaxErrorZ(self):
        
        return SensorDummy.ERROR_ACCEL_DISTRIBUTION[1]
    