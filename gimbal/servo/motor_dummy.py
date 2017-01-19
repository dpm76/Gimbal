'''
Created on 19 de ene. de 2016

@author: david
'''
import time


class MotorDummy(object):
    
    MAX_THROTTLE = 80.0 #percentage
    
    def __init__(self, motorId, neutralThrottle=0.0):
        """
        Constructor
        
        @param motorId: Identificator of the motor. A number between 0 to 3 (in case of quadcopter)  
        """
                
        self._motorId = motorId        
        self._throttle = 0.0
        self._neutralThrottle = neutralThrottle 
        
        
    def start(self):
        
        self._throttle = 0.0
        
    
    def setThrottle(self, throttle):
        
        self._throttle = float(throttle)
        time.sleep(0.001)

        
    def getThrottle(self):
        
        return self._throttle
    
    
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

        self._throttle = 100.0
        
        
    def setMinThrottle(self):
        """
        Sends the min throttle signal (useful for calibrating process, or setting the motor in stand-by state)
        """
        
        self._throttle = 0.0
        
        
    def standBy(self):
        """
        Set the motor in stand-by state
        """
        
        self.setMinThrottle()        
        
        
    def idle(self):
        """
        Set the motor in idle state
        """
        
        self._throttle = 0.0
        
        
    def stop(self):
        """
        Stops the motor
        """
        
        self._throttle = 0.0
