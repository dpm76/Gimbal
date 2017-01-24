'''
Created on 24 ene. 2017

@author: david
'''
import unittest

from stabilization.pid import Pid
from time import sleep


class PidTestCase(unittest.TestCase):


    def _readInput(self):
        
        return self._input
    
    
    def _setOutput(self, output):
        
        self._output = output

    
    def _getRoundedOutput(self):
        
        return [int(x + 0.5) for x in self._output]


    def setUp(self):

        self._input = None
        self._output = None
        
        self._pid = Pid(0.02, 2, self._readInput, self._setOutput, "test-pid")\
            .setProportionalConstants([1,1])\
            .setIntegralConstants([1,1])\
            .setDerivativeConstants([1,1])


    def testCalculate(self):
        
        self._input = [-1.0,2.0]
        self._pid.setTargets([0.0,0.0])
        
        self._pid.resetTime()
        sleep(1.0)
        self._pid._calculate()
        
        output = self._getRoundedOutput()
        self.assertSequenceEqual(output, [3, -5], "Bad calculation: {0}".format(output))
        
        self._input = [3.0, -5.0]
        self._pid.resetTime()
        sleep(1.0)
        self._pid._calculate()
        
        output = self._getRoundedOutput()
        self.assertSequenceEqual(output, [-8, 15], "Bad calculation: {0}".format(output))


    def testSetTarget(self):
        
        self._pid.setTarget(1.0, 1)
        targets = self._pid.getTargets()
        
        self.assertEquals(targets[1], 1.0, "Target wasn't properly set")

    
    def testSetTargets(self):

        self._pid.setTargets([1.0, 2.0])
        targets = self._pid.getTargets()
        
        self.assertSequenceEqual(targets, [1.0, 2.0], "Targets weren't properly set")
        
    
    def testSetConstants(self):
        
        self._pid\
            .setProportionalConstants([2.0,2.0])\
            .setIntegralConstants([3.0,3.0])\
            .setDerivativeConstants([4.0,4.0])
            
        kp = self._pid.getProportionalConstants()
        ki = self._pid.getIntegralConstants()
        kd = self._pid.getDerivativeConstants()
        
        self.assertSequenceEqual(kp, [2.0,2.0], "Constants weren't properly set")
        self.assertSequenceEqual(ki, [3.0,3.0], "Constants weren't properly set")
        self.assertSequenceEqual(kd, [4.0,4.0], "Constants weren't properly set")
        
    
    def testIntegralLock(self):
        
        self._input = [-1.0,2.0]
        self._pid.setTargets([0.0,0.0])
        
        self._pid.resetTime()
        sleep(1.0)
        self._pid._calculate()
       
        self._pid.lockIntegral(0)        
        
        self._input = [3.0, -5.0]
        self._pid.resetTime()
        sleep(1.0)
        self._pid._calculate()
        
        output = self._getRoundedOutput()
        self.assertSequenceEqual(output, [-5, 15], "Bad calculation: {0}".format(output))

    
    def testIntegralReset(self):
        
        self._input = [-1.0,2.0]
        self._pid.setTargets([0.0,0.0])
        
        self._pid.resetTime()
        sleep(1.0)
        self._pid._calculate()
       
        self._pid.resetIntegral(0)        
        
        self._input = [3.0, -5.0]
        self._pid.resetTime()
        sleep(1.0)
        self._pid._calculate()
        
        output = self._getRoundedOutput()
        self.assertSequenceEqual(output, [-9, 15], "Bad calculation: {0}".format(output))
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()