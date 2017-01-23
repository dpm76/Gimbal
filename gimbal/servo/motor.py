# -*- coding: utf-8 -*-

"""
Created on 06/04/2015

@author: david
"""
import logging
from os import system
from os.path import exists

from servo.sysfs_writer import SysfsWriter


class Motor(object):
    """
    Controls a single motor
    """
    
    KEY_PWM_ID = "pwmId"
    KEY_PIN_ID = "pinId" 
    
    #BeagleBone's config.
    #TODO 20150408 DPM - Include this configuration in such a settings file
    _pins = [{KEY_PWM_ID: 6, KEY_PIN_ID: "P8.13"},
             {KEY_PWM_ID: 5, KEY_PIN_ID: "P8.19"},
             {KEY_PWM_ID: 4, KEY_PIN_ID: "P9.16"},
             {KEY_PWM_ID: 3, KEY_PIN_ID: "P9.14"}]
    
    PERIOD = 20000000 #nanoseconds = 50Hz
    
    MIN_DUTY = 1000000 #nanoseconds    
    MAX_DUTY = 2000000 #nanoseconds
    
    RANGE_DUTY = (MAX_DUTY - MIN_DUTY) / 100.0

    MAX_THROTTLE = 100.0 #percentage
    MIN_THROTTLE = 0.0 #percentage


    def __init__(self, motorId, neutralThrottle=0.0):
        """
        Constructor
        
        @param motorId: Identificator of the motor.
            A number between 0 to 3, in case of quadcopter.
            A number between 0 to 1, in case of 2-axis gimbal.
        @param neutralThrottle: throttle when the motor is at rest.
        """
        
        pinIndex = motorId
        self._pwmId = Motor._pins[pinIndex][Motor.KEY_PWM_ID]
        self._pinId = Motor._pins[pinIndex][Motor.KEY_PIN_ID]
        
        self._motorId = motorId
        
        self._neutralThrottle = neutralThrottle
        self._throttle = neutralThrottle
        self._duty = self._calculateDuty(self._throttle)

        self._sysfsWriter = None
        
        
    def setSysfsWriter(self, sysfsWriter):
        """
        Sets the filesystem writer. 
        It overrides the standard writer in order to use a dummy writer for testing.
        @param sysfsWriter: Filesystem writer
        """
        
        self._sysfsWriter = sysfsWriter
        
        return self
        
    
    def start(self):
        """
        Starts the motor up
        """
        
        if not self._sysfsWriter:
            self._sysfsWriter = SysfsWriter()
        
        
        if not exists("/sys/class/pwm/pwm{0}".format(self._pwmId)):
            system("config-pin {0} pwm".format(self._pinId))
            self._sysfsWriter.setPath("/sys/class/pwm/export")\
                .write(str(self._pwmId))\
                .close()            
        
        #Stop motor, in order to reset it
        self._sysfsWriter.setPath("/sys/class/pwm/pwm{0}/run".format(self._pwmId))\
            .write("0")\
            .close()
        
        #Set motor
        self._sysfsWriter.setPath("/sys/class/pwm/pwm{0}/period_ns".format(self._pwmId))\
            .write(str(Motor.PERIOD))\
            .close()        
        
        self._throttle = self._neutralThrottle
        self._duty = self._calculateDuty(self._throttle)
        self._sysfsWriter.setPath("/sys/class/pwm/pwm{0}/duty_ns".format(self._pwmId))\
            .write("{0}".format(self._duty))\
            .close()
        self._sysfsWriter.setPath("/sys/class/pwm/pwm{0}/run".format(self._pwmId))\
            .write("1")\
            .close()
        
        self._sysfsWriter.setPath("/sys/class/pwm/pwm{0}/duty_ns".format(self._pwmId))
        
        logging.info("motor {0}: started".format(self._motorId))
        
        
    def setThrottle(self, throttle):
        """
        Sets the motor's throttle
        
        @param throttle: Motor power as percentage 
        """
        
        self._throttle = float(throttle)

        if self._throttle >= Motor.MIN_THROTTLE and self._throttle <= Motor.MAX_THROTTLE:            
        
            self._duty = self._calculateDuty(self._throttle)
            #logging.debug("motor {0}: duty={1}; throttle={2}".format(self._motorId, self._duty, self._throttle))
        
            self._sysfsWriter.write(str(self._duty))

        #else:
        #    logging.debug("motor {0}: duty={1}; throttle={2} (virtual)".format(self._motorId, self._duty, self._throttle))
        
    
    def getThrottle(self):
        """
        Returns the current motor throttle
        """
        
        return self._throttle
    
    
    def getDuty(self):
        """
        Returns the current motor duty
        """
        
        return self._duty    
    
    
    def addThrottle(self, increment):
        """
        Increases or decreases the motor's throttle
        
        @param increment: Value added to the current throttle percentage. This can be negative to decrease.
        """
        
        self.setThrottle(self._throttle + increment)
        
    
    def setMaxThrottle(self):
        """
        Sends the max throttle signal (useful for calibrating process)
        """
        
        #logging.debug("motor {0}: max-throttle".format(self._motorId))
        
        self._throttle = 100.0
        self._duty = Motor.MAX_DUTY

        self._sysfsWriter.write(str(Motor.MAX_DUTY))
        
        
    def setMinThrottle(self):
        """
        Sends the min throttle signal (useful for calibrating process)
        """
        
        #logging.debug("motor {0}: min-throttle".format(self._motorId))
        
        self._throttle = 0.0
        self._duty = Motor.MIN_DUTY
        
        self._sysfsWriter.write(str(Motor.MIN_DUTY))
        

    def setNeutralThrottle(self):
        """
        Set motor being at rest
        """
        
        self._throttle = self._neutralThrottle
        self._duty = self._calculateDuty(self._throttle)        
        self._sysfsWriter.write(str(self._duty))
        
        
    def standBy(self):
        """
        Set the motor in stand-by state
        """
        
        logging.info("motor {0}: stand-by".format(self._motorId))
        self.setNeutralThrottle()        
        
        
    def idle(self):
        """
        Set the motor in idle state
        """
        
        logging.info("motor {0}: idle".format(self._motorId))        
        self.standBy()
        
        
    def stop(self):
        """
        Stops the motor
        """
        
        logging.info("motor {0}: stopping".format(self._motorId))
        
        self.setNeutralThrottle()
        
        self._sysfsWriter.close()        
        self._sysfsWriter.setPath("/sys/class/pwm/pwm{0}/run".format(self._pwmId))\
            .write("0")\
            .close()
        
        logging.info("motor {0}: stopped".format(self._motorId))
        
    
    def _calculateDuty(self, throttle):
        
        return int((Motor.RANGE_DUTY * throttle) + Motor.MIN_DUTY)    
