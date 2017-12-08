# -*- coding: utf-8 -*-

'''
Created on 23/01/2017

@author: david
'''
from copy import deepcopy
from time import time
import logging
from random import uniform, seed


class SensorDummy(object):
    '''
    IMU sensor dummy for testing
    '''
    
    ERROR_ANGLE_SPEED_DISTRIBUTION = [-1.0, 1.0] #[-0.1, 0.15]
    ERROR_ANGLE_DISTRIBUTION = [-0.08, 0.1]
    ERROR_ACCEL_DISTRIBUTION = [-0.1, 0.1] #[-0.1, 0.15]
    
    def __init__(self, addNoise=False):
        
        self._addNoise = addNoise
        if self._addNoise:        
            seed()
        self._currentAngles = [0.0] * 3
        self._timestamp = time() 
    
    
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
        
        angleSpeed = self._noisify([0.0]*3, SensorDummy.ERROR_ANGLE_SPEED_DISTRIBUTION)
        timeStampNow = time()
        timeDelta = timeStampNow - self._timestamp
        self._timestamp = timeStampNow
        angleDelta = [timeDelta * angle for angle in angleSpeed]
        self._currentAngles = [x+y for x,y in zip(angleDelta, self._currentAngles)]
        angles = \
            self._noisify(self._currentAngles, SensorDummy.ERROR_ANGLE_DISTRIBUTION) \
            if self._addNoise \
            else deepcopy(self._currentAngles) 
        
        return angles

    
    def readDeviceAngles(self):

        return self.readAngles()

    
    def resetGyroReadTime(self):        
        self._timestamp = time()

    
    def refreshState(self):
        pass
    
    
    def start(self):
        
        text = "Using dummy IMU." 
        
        print(text)
        logging.info(text)
        
    
    def calibrate(self):
        pass
    
    def stop(self):
        pass
    
    def getMaxErrorZ(self):
        
        return SensorDummy.ERROR_ACCEL_DISTRIBUTION[1]
    