# -*- coding: utf-8 -*-
'''
Created on 23/10/2015

@author: david
'''

import logging
import math
import time

import imu6050_defs as reg
from .I2CSensor import I2CSensor
from .vector import Vector
from copy import deepcopy
from .state import SensorState


try:
    import smbus
    
except ImportError:
    
    class smbus(object):
        @staticmethod
        def SMBus(channel):
            raise Exception("smbus module not found!")


class Imu6050(I2CSensor):
    '''
    Gyro and accelerometer
    '''
    
    ADDRESS = 0x68
    GYRO2DEG = 250.0 / 32767.0 # +/- 250º/s mode
    ACCEL2G = 2.0 / 32767.0 # +/- 2g mode
    GRAVITY = 9.807 #m/s²
    PI2 = math.pi / 2.0
    ACCEL2MS2 = GRAVITY * ACCEL2G

    #CALIBRATION_FILE_PATH = "../calibration.config.json"
    

    def __init__(self):
        '''
        Constructor
        '''
        
        self._setAddress(Imu6050.ADDRESS)
        
        self._bus = smbus.SMBus(1)
        
        self._gyroOffset = [0]*3
        
        self._gyroReadTime = time.time()
        
        self._previousAngles = [0.0]*3
        
        self._accOffset = [0]*3

        self._accAnglesOffset = [0.0]*2
        
        self._lastReadAccRawData = [0]*3
        
        self._angSpeed = [0.0]*2
        self._localGravity = 0.0
        
        self._state = SensorState()
    
    
    def _readRawGyroX(self):
        
        return self._readWordHL(reg.GYRO_XOUT)
    
    
    def _readRawGyroY(self):
        
        return self._readWordHL(reg.GYRO_YOUT)
    
    
    def _readRawGyroZ(self):
        
        return self._readWordHL(reg.GYRO_ZOUT)
    
    
    def _readAngSpeed(self, reg, index):

        data = (self._readWordHL(reg) - self._gyroOffset[index]) * Imu6050.GYRO2DEG
        return data


    def readAngleSpeeds(self):
        
        return self._state.angleSpeeds


    def _readAngleSpeeds(self):

        speedAX = self._readAngSpeedX()
        speedAY = self._readAngSpeedY()        
        speedAZ = self._readAngSpeedZ()

        self._state.angleSpeeds = [speedAX, speedAY, speedAZ]


    def _readAngSpeedX(self):
        
        return self._readAngSpeed(reg.GYRO_XOUT, 0)


    def _readAngSpeedY(self):
        
        return self._readAngSpeed(reg.GYRO_YOUT, 1)


    def _readAngSpeedZ(self):
        
        return self._readAngSpeed(reg.GYRO_ZOUT, 2)
    

    def _readAccAngles(self):

        rawAccX = self._readRawAccelX()
        rawAccY = self._readRawAccelY()
        rawAccZ = self._readRawAccelZ()

        accAngX = math.degrees(math.atan2(rawAccY, rawAccZ))
        accAngY = -math.degrees(math.atan2(rawAccX, rawAccZ))
        
        accAngles = [accAngX, accAngY]
        
        return accAngles


    def readAngles(self):
        
        return self._state.angles


    def _readAngles(self):
        
        accAngles = self._readAccAngles()
        previousAngSpeeds = self._angSpeed 
        self._angSpeed = [self._state.angleSpeeds[0],self._state.angleSpeeds[1]] #[self._readAngSpeedX(), self._readAngSpeedY()]
        currentTime = time.time()
        dt2 = (currentTime - self._gyroReadTime) / 2.0
        
        currentAngles = [0.0]*3
        
        for index in range(2):
            expectedAngle = self._previousAngles[index] + \
                (self._angSpeed[index] + previousAngSpeeds[index]) * dt2            
            currentAngles[index] = 0.2 * accAngles[index] + 0.8 * expectedAngle
        
        self._gyroReadTime = currentTime
        self._previousAngles = currentAngles
        
        self._state.angles = deepcopy(currentAngles)


    def readDeviceAngles(self):

        angles = self.readAngles()

        angles[0] -= self._accAnglesOffset[0]
        angles[1] -= self._accAnglesOffset[1]

        #logging.info(angles)

        return angles

    
    def _readRawAccel(self, reg):

        return self._readWordHL(reg)
    
    
    def _readRawAccelX(self):
        
        return self._readRawAccel(reg.ACC_XOUT)
    
    
    def _readRawAccelY(self):
        
        return self._readRawAccel(reg.ACC_YOUT)
    
    
    def _readRawAccelZ(self):
        
        return self._readRawAccel(reg.ACC_ZOUT)
   
    
    def readAccels(self):
        
        return self._state.accels
   

    def _readAccels(self):

        accelX = self._readRawAccelX() * Imu6050.ACCEL2MS2
        accelY = self._readRawAccelY() * Imu6050.ACCEL2MS2
        accelZ = self._readRawAccelZ() * Imu6050.ACCEL2MS2
        
        angles = [math.radians(angle) for angle in self.readAngles()]

        accels = Vector.rotateVector3D([accelX, accelY, accelZ], angles + [0.0])
        
        #Eliminate gravity acceleration
        accels[2] -= self._localGravity

        self._state.accels = accels
    
    
    def readQuaternions(self):
        #TODO
        pass
    
    
    def resetGyroReadTime(self):
        
        self._gyroReadTime = time.time()
    
    
    def refreshState(self):
        
        self._readAngleSpeeds()
        self._readAngles()
        self._readAccels()
        
    
    def start(self):
        '''        
         Initializes sensor
        '''
        
        startMessage = "Using IMU-6050."
        logging.info(startMessage)

        #Initializes gyro
        self._bus.write_byte_data(self._address, reg.PWR_MGM1, reg.RESET)
        self._bus.write_byte_data(self._address, reg.PWR_MGM1, reg.CLK_SEL_X)
        #1kHz (as DPLF_CG_6) / (SMPLRT_DIV +1) => sample rate @50Hz)
        self._bus.write_byte_data(self._address, reg.SMPRT_DIV, 19)
        #DLPF_CFG_6: Low-pass filter @5Hz; analog sample rate @1kHz
        self._bus.write_byte_data(self._address, reg.CONFIG, reg.DLPF_CFG_6)
        self._bus.write_byte_data(self._address, reg.GYRO_CONFIG, reg.GFS_250)
        self._bus.write_byte_data(self._address, reg.ACCEL_CONFIG, reg.AFS_2)
        self._bus.write_byte_data(self._address, reg.PWR_MGM1, 0)
        #TODO 20160202 DPM - Sample rate at least at 400Hz
        
        #Wait for sensor stabilization
        time.sleep(1)
        
        self.calibrate()
    

    def calibrate(self):
        '''
        Calibrates sensor
        '''
        
        logging.info("Calibrating accelerometer...")
        self._accOffset = [0.0]*3
        
        i = 0
        while i < 100:

            self._accOffset[0] += self._readRawAccelX()
            self._accOffset[1] += self._readRawAccelY()
            self._accOffset[2] += self._readRawAccelZ()
            
            time.sleep(0.02)
            i+=1
        
        for index in range(3): 
            self._accOffset[index] /= float(i)
        
        
        #Calibrate gyro
        logging.info("Calibrating gyro...")
        self._gyroOffset = [0.0]*3
        
        i = 0
        while i < 100:
            
            self._gyroOffset[0] += self._readRawGyroX()
            self._gyroOffset[1] += self._readRawGyroY()
            self._gyroOffset[2] += self._readRawGyroZ()
            
            time.sleep(0.02)
            i += 1
            
        for index in range(3):
            self._gyroOffset[index] /= float(i) 
            
        #Calculate sensor installation angles
        self._accAnglesOffset[0] = self._previousAngles[0] = math.degrees(math.atan2(self._accOffset[1], self._accOffset[2]))
        self._accAnglesOffset[1] = self._previousAngles[1] = -math.degrees(math.atan2(self._accOffset[0], self._accOffset[2]))
        
        #Calculate local gravity
        angles = [math.radians(angle) for angle in self._accAnglesOffset]
        accels = [accel * Imu6050.ACCEL2MS2 for accel in self._accOffset]       
        self._localGravity = Vector.rotateVector3D(accels, angles + [0.0])[2]
    
    
    def getMaxErrorZ(self):
        
        return 0.1
    
    
    def stop(self):
        
        pass
    
