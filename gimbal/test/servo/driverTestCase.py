'''
Created on 19 ene. 2017

@author: david
'''
import unittest

from config import Configuration
from servo.driver import Driver
from test.servo.sysfs_writer_dummy import SysfsWriterDummyFactory


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testStart(self):
        
        driver = Driver(2, Configuration.VALUE_MOTOR_CLASS_LOCAL, SysfsWriterDummyFactory())
        driver.start()
        
        throttles = driver.getThrottles()
        
        self.assertSequenceEqual(throttles, [50.0, 50.0], "Not started properly")
        

    def testStop(self):
        driver = Driver(2, Configuration.VALUE_MOTOR_CLASS_LOCAL, SysfsWriterDummyFactory())
        driver.start()
        driver.rotateX(100.0)
        driver.rotateY(-100.0)
        
        driver.stop()
        throttles = driver.getThrottles()
        
        self.assertSequenceEqual(throttles, [50.0, 50.0], "Not stoped properly")
        

    def testRotateX(self):
        
        driver = Driver(2, Configuration.VALUE_MOTOR_CLASS_LOCAL, SysfsWriterDummyFactory())
        driver.start()
        driver.rotateX(100.0)
        
        throttles = driver.getThrottles()
        
        self.assertEquals(throttles[Driver.X_AXIS_MOTOR], 100.0, "Not set properly")
        
    
    def testRotateXMinimal(self):
        
        driver = Driver(2, Configuration.VALUE_MOTOR_CLASS_LOCAL, SysfsWriterDummyFactory())
        driver.start()
        driver.rotateX(-100.0)
        
        throttles = driver.getThrottles()
        
        self.assertEquals(throttles[Driver.X_AXIS_MOTOR], 0.0, "Not set properly")
        
        
    def testRotateXMaximal(self):
        
        driver = Driver(2, Configuration.VALUE_MOTOR_CLASS_LOCAL, SysfsWriterDummyFactory())
        driver.start()
        driver.rotateX(100.0)
        
        throttles = driver.getThrottles()
        
        self.assertEquals(throttles[Driver.X_AXIS_MOTOR], 100.0, "Not set properly")


    def testRotateXNeutral(self):
        
        driver = Driver(2, Configuration.VALUE_MOTOR_CLASS_LOCAL, SysfsWriterDummyFactory())
        driver.start()
        driver.rotateX(0.0)
        
        throttles = driver.getThrottles()
        
        self.assertEquals(throttles[Driver.X_AXIS_MOTOR], 50.0, "Not set properly")


    def testRotateY(self):
        
        driver = Driver(2, Configuration.VALUE_MOTOR_CLASS_LOCAL, SysfsWriterDummyFactory())
        driver.start()
        driver.rotateY(100.0)
        
        throttles = driver.getThrottles()
        
        self.assertEquals(throttles[Driver.Y_AXIS_MOTOR], 100.0, "Not set properly")
        

    def testRotateYMinimal(self):
        
        driver = Driver(2, Configuration.VALUE_MOTOR_CLASS_LOCAL, SysfsWriterDummyFactory())
        driver.start()
        driver.rotateY(-100.0)
        
        throttles = driver.getThrottles()
        
        self.assertEquals(throttles[Driver.Y_AXIS_MOTOR], 0.0, "Not set properly")
        
        
    def testRotateYMaximal(self):
        
        driver = Driver(2, Configuration.VALUE_MOTOR_CLASS_LOCAL, SysfsWriterDummyFactory())
        driver.start()
        driver.rotateY(100.0)
        
        throttles = driver.getThrottles()
        
        self.assertEquals(throttles[Driver.Y_AXIS_MOTOR], 100.0, "Not set properly")


    def testRotateYNeutral(self):
        
        driver = Driver(2, Configuration.VALUE_MOTOR_CLASS_LOCAL, SysfsWriterDummyFactory())
        driver.start()
        driver.rotateY(0.0)
        
        throttles = driver.getThrottles()
        
        self.assertEquals(throttles[Driver.Y_AXIS_MOTOR], 50.0, "Not set properly")

        
    def testGetThrottles(self):
        
        driver = Driver(2, Configuration.VALUE_MOTOR_CLASS_LOCAL, SysfsWriterDummyFactory())
        driver.start()
        driver.rotateX(-100.0)
        driver.rotateY(100.0)
        
        throttles = driver.getThrottles()
        
        self.assertSequenceEqual(throttles, [0.0, 100.0], "Wrong values")
        
        
    def testNeutralThrottle(self):
        
        self.assertEquals(Driver.NEUTRAL_THROTTLE, 50.0, "Incorrect neutral throttle")



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testStart']
    unittest.main()