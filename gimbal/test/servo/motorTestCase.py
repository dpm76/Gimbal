'''
Created on 18 ene. 2017

@author: david
'''
import unittest

from servo.motor import Motor
from test.servo.sysfs_writer_dummy import SysfsWriterDummy


class MotorTest(unittest.TestCase):

    def testStart(self):
        
        filesystem = SysfsWriterDummy()
        motor = Motor(0, 50.0).setSysfsWriter(filesystem)
        motor.start()
        
        throttle = motor.getThrottle()
        duty = motor.getDuty()
        
        self.assertEquals(throttle, 50.0, "Incorrect throttle")
        self.assertEquals(duty, 1500000, "Incorrect duty")
        
        #pwm6 corresponds to the motor number 0
        self.assertEquals(int(filesystem.read("/sys/class/pwm/pwm6/run")), 1, "Motor not running")
        self.assertEquals(int(filesystem.read("/sys/class/pwm/pwm6/period_ns")), 20000000, "Incorrect period")
        self.assertEquals(int(filesystem.read("/sys/class/pwm/pwm6/duty_ns")), 1500000, "Motor not running")
        
    
    def testSetThrottle(self):
        
        filesystem = SysfsWriterDummy()
        motor = Motor(0, 50.0).setSysfsWriter(filesystem)
        motor.start()
        
        motor.setThrottle(10.0)
        
        throttle = motor.getThrottle()
        duty = motor.getDuty()
        
        self.assertEquals(throttle, 10.0, "Throttle wasn't properly set")
        self.assertEquals(duty, 1100000, "Duty wasn't properly set")
        #pwm6 corresponds to the motor number 0
        self.assertEquals(int(filesystem.read("/sys/class/pwm/pwm6/duty_ns")), 1100000, "Duty wasn't properly written")
        
    
    def testGetThrottle(self):
        
        filesystem = SysfsWriterDummy()
        motor = Motor(0, 50.0).setSysfsWriter(filesystem)
        motor.start()        
        motor.setThrottle(10.0)
        
        throttle = motor.getThrottle()
        self.assertEquals(throttle, 10.0, "Throttle wasn't properly returned")
        
    
    def testGetDuty(self):
        
        filesystem = SysfsWriterDummy()
        motor = Motor(0, 50.0).setSysfsWriter(filesystem)
        motor.start()        
        motor.setThrottle(10.0)
        
        duty = motor.getDuty()
        
        self.assertEquals(duty, 1100000, "Duty wasn't properly returned")
        
    
    def testAddThrottle(self):
        
        filesystem = SysfsWriterDummy()
        motor = Motor(0, 50.0).setSysfsWriter(filesystem)
        motor.start()        
        motor.setThrottle(10.0)
        
        motor.addThrottle(15.0)        
        throttle = motor.getThrottle()        
        
        self.assertEquals(throttle, 25.0, "Throttle wasn't properly added")
        
    
    def testSetMaxThrottle(self):
        
        filesystem = SysfsWriterDummy()
        motor = Motor(0, 50.0).setSysfsWriter(filesystem)
        motor.start()
        
        motor.setMaxThrottle()        
        throttle = motor.getThrottle()        
        
        self.assertEquals(throttle, 100.0, "Throttle wasn't properly set")
            
    
    def testSetMinThrottle(self):
        
        filesystem = SysfsWriterDummy()
        motor = Motor(0, 50.0).setSysfsWriter(filesystem)
        motor.start()
        
        motor.setMinThrottle()        
        throttle = motor.getThrottle()        
        
        self.assertEquals(throttle, 0.0, "Throttle wasn't properly set")
        
    
    def testSetNeutralThrottle(self):
        
        filesystem = SysfsWriterDummy()
        motor = Motor(0, 50.0).setSysfsWriter(filesystem)
        motor.start()
        
        motor.setThrottle(10.0)
        throttle = motor.getThrottle()
        self.assertEquals(throttle, 10.0, "Throttle wasn't properly set")
        
        motor.setNeutralThrottle()        
        throttle = motor.getThrottle()        
        
        self.assertEquals(throttle, 50.0, "Throttle wasn't properly set")
        
    
    def testStandBy(self):
        
        filesystem = SysfsWriterDummy()
        motor = Motor(0, 50.0).setSysfsWriter(filesystem)
        motor.start()
        
        motor.setThrottle(10.0)
        throttle = motor.getThrottle()
        self.assertEquals(throttle, 10.0, "Throttle wasn't properly set")
        
        motor.standBy()        
        throttle = motor.getThrottle()        
        
        self.assertEquals(throttle, 50.0, "Throttle wasn't properly set")
        
    
    def testIdle(self):
        
        filesystem = SysfsWriterDummy()
        motor = Motor(0, 50.0).setSysfsWriter(filesystem)
        motor.start()
        
        motor.setThrottle(10.0)
        throttle = motor.getThrottle()
        self.assertEquals(throttle, 10.0, "Throttle wasn't properly set")
        
        motor.idle()        
        throttle = motor.getThrottle()        
        
        self.assertEquals(throttle, 50.0, "Throttle wasn't properly set")
        
    
    def testStop(self):
        
        filesystem = SysfsWriterDummy()
        motor = Motor(0, 50.0).setSysfsWriter(filesystem)
        motor.start()
        
        motor.setThrottle(10.0)
        throttle = motor.getThrottle()
        self.assertEquals(throttle, 10.0, "Throttle wasn't properly set")
        
        motor.stop()
        
        throttle = motor.getThrottle()
        self.assertEquals(throttle, 50.0, "Throttle wasn't properly set at neutral value")
        
        #pwm6 corresponds to the motor number 0
        self.assertEquals(int(filesystem.read("/sys/class/pwm/pwm6/run")), 0, "Motor wasn't properly stopped")
        
    
    def test_calculateDuty(self):
        
        filesystem = SysfsWriterDummy()
        motor = Motor(0, 50.0).setSysfsWriter(filesystem)
        
        duty = motor._calculateDuty(0.0)
        self.assertEquals(duty, 1000000, "Wrong duty")
        
        duty = motor._calculateDuty(50.0)
        self.assertEquals(duty, 1500000, "Wrong duty")
        
        duty = motor._calculateDuty(100.0)
        self.assertEquals(duty, 2000000, "Wrong duty")
    
    


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()