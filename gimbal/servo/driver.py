# -*- coding: utf-8 -*-

'''
Created on 06/04/2015

@author: david
'''

from glob import glob
from os import system
from os.path import exists

from config import Configuration
from servo.motor import Motor
from servo.motor_dummy import MotorDummy


class Driver(object):
    '''
    Controls a motor set
    '''
    
    NEUTRAL_THROTTLE = Motor.MAX_THROTTLE / 2.0
    X_AXIS_MOTOR = 0
    Y_AXIS_MOTOR = 1
    
    def __init__(self, numMotors=2, motorType="", sysfsWriterFactory=None):
        '''
        Constructor

        @param numMotors: Motors amount that the driver will manage         
        @param motorType: String with the type of the motor to implement. See Configuration.VALUE_MOTOR_CLASS_*
        If motorType value is not provided, the configuration will be used.
        @param sysfsWriterFactory: System filesystem writer factory. Usually is null but for testing purposes
        '''
        
        self._numMotors = numMotors
        self._config = Configuration.getInstance().getConfig()        
        self._motors = []
        
        self._motorType = motorType
        if self._motorType == "":
            self._motorType = self._config[Configuration.KEY_MOTOR_CLASS]

        for motorId in range(self._numMotors):
            motor = self._createMotor(motorId, sysfsWriterFactory)
            self._motors.append(motor)            
            
    
    def _createMotor(self, motorId, sysfsWriterFactory):
        '''
        Creates a new motor instance
        '''
        
        if self._motorType == Configuration.VALUE_MOTOR_CLASS_LOCAL:            
            motor = Motor(motorId, Driver.NEUTRAL_THROTTLE)
            if sysfsWriterFactory:
                motor.setSysfsWriter(sysfsWriterFactory.create())
            
        else: #default VALUE_MOTOR_CLASS_DUMMY
            motor = MotorDummy(motorId, Driver.NEUTRAL_THROTTLE)        
            
        return motor
            
        
    def start(self):
        '''
        Inits the motor set
        '''
        
        if self._motorType == Configuration.VALUE_MOTOR_CLASS_LOCAL \
            and not exists("/sys/class/pwm/pwm3") \
            and len(glob("sys/devices/bone_capemgr.*")) > 0:
            
            system("echo cape-universaln > /sys/devices/bone_capemgr.*/slots")
            
        #Init motors
        for motor in self._motors:
            motor.start()
            motor.standBy()
            
            
    def stop(self):
        """
        Stops the motors
        """        

        for motor in self._motors:
            motor.stop()
                        
    
    def rotateX(self, throttle): 
        """
        Set X-axis motor throttle
        @param throttle: motor's throttle as range from -100 to +100 
        """
        
        self._rotate(Driver.X_AXIS_MOTOR, throttle)        

    
    def rotateY(self, throttle):
        """
        Set Y-axis motor throttle
        @param throttle: motor's throttle as range from -100 to +100 
        """
    
        self._rotate(Driver.Y_AXIS_MOTOR, throttle)


    def _rotate(self, index, throttle):
        """
        Set motor throttle
        @param throttle: motor's throttle as range from -100 to +100
        @param index: motor's index 
        """
    
        self._motors[index].setThrottle(Driver.NEUTRAL_THROTTLE + (throttle / 2.0))
        
                
    def getThrottles(self):
        
        return [motor.getThrottle() for motor in self._motors]
