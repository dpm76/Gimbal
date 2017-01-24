# -*- coding: utf-8 -*-
'''
Created on 11/04/2015

@author: david
'''

import logging
from threading import Thread
import time


class Pid(object):
    '''
    Proportional Integrative Derivative stabilizer
    '''
    
    #Period range to be considered as correct loop rate
    PERIOD_RANGE_MARGIN = 0.1

    def __init__(self, period, length, readInputDelegate, setOutputDelegate, pidName = ""):
        '''
        Constructor
        @param period: Timerate to perform each calculation
        @param length: Number of items to stabilize
        @param readInputDelegate: Method to gather current values.
         Must return an array with the same number of items to stabilize
        @param setOutputDelegate: Returns an array with the values to react,
         one for each item to stabilize. 
        @param pidName: (optional) Name to identify the PID-thread among other ones.
        '''
        
        self._pidName = pidName
        
        self._targets = [0.0] * length        
        
        self._integrals = [0.0] * length
        self._lastErrors = [0.0] * length
        
        self._period = period        
        self._minPeriod = period * (1.0 - Pid.PERIOD_RANGE_MARGIN)
        self._maxPeriod = period * (1.0 + Pid.PERIOD_RANGE_MARGIN)
        self._periodTarget = (self._minPeriod + self._period) / 2.0 
        
        self._previousTime = time.time()
        self._currentPeriod = period
        
        self._kp = [0.0] * length
        self._ki = [0.0] * length
        self._kd = [0.0] * length
        
        self._readInput = readInputDelegate
        self._setOutput = setOutputDelegate
    
        self._isRunning = False
        self._thread = None
        
        self._length = length
        
        self._integralLocked = [False] * length
        
        self._deltaTimeSum = 0.0
        self._iterationCount = 0
        
    
    def setProportionalConstants(self, kpMatrix):
        """
        @param kpMatrix: Proportional constant array. One for each item to stabilize
        """
        
        if self._length == len(kpMatrix):
            self._kp = kpMatrix            
        else:
            raise Exception("Wrong matrix length")
        
        return self
    
    
    def setIntegralConstants(self, kiMatrix):
        """
        @param kiMatrix: Integral constant array. One for each item to stabilize
        """
        
        if self._length == len(kiMatrix):
            self._ki = kiMatrix
        else:
            raise Exception("Wrong matrix length")
        
        return self
        
    
    def setDerivativeConstants(self, kdMatrix):
        """
        @param kdMatrix: Derivative constant array. One for each item to stabilize
        """
        
        if self._length == len(kdMatrix):
            self._kd = kdMatrix
        else:
            raise Exception("Wrong matrix length")
        
        return self
    
    
    def getProportionalConstants(self):
        """
        @return: Proportional constants array
        """
        
        return self._kp
    
    
    def getIntegralConstants(self):
        """
        @return: Integral constants array
        """

        return self._ki
    
    
    def getDerivativeConstants(self):
        """
        @return: Derivative constants array
        """

        return self._kd
    
        
    def _calculate(self):
        """
        Performs the stabilization
        """
        
        outputArray = [0.0]*self._length
        
        currentValues  = self._readInput()        
        currentTime = time.time()
        dt = currentTime - self._previousTime
                
        for i in range(self._length):
            
            error = self._targets[i] - currentValues[i]            
                        
            #Proportional stabilization
            pPart = self._kp[i] * error
            
            #Integral stabilization
            if not self._integralLocked[i]:
                self._integrals[i] += error * dt
            iPart = self._ki[i] * self._integrals[i]
            
            #Derivative stabilization
            dPart = self._kd[i] * (error - self._lastErrors[i]) / dt            
            self._lastErrors[i] = error
            
            #Join partial results
            result = pPart + iPart + dPart
            outputArray[i] = result            

        self._previousTime = currentTime
        self._setOutput(outputArray)
        
        self._currentPeriod = dt
        self._deltaTimeSum += dt
        self._iterationCount += 1
    
    
    def setTarget(self, target, index):
        """
        Sets target for any item
        @param target: Value to reach
        @param index: Item to change
        """
        
        self._targets[index] = target
        
    
    def setTargets(self, targets):
        """
        Sets targets
        @param targets: Array with the targets to reach. One for each item to stabilize.
        """
        
        self._targets = targets
        
        
    def getTarget(self, index):
        """
        Gets the current target for an item
        @param index: Item index
        @return: Current target
        """
        
        return self._targets[index]
    
    
    def getTargets(self):
        """
        Gets all current targets
        @return: Array of current targets
        """
        
        return self._targets
        
        
    def getCurrentPeriod(self):
        """
        Gets the current target period
        @return: Current target period
        """
        
        return self._currentPeriod
    
    
    def _do(self): 
        """
        Performs the stabilization
        """
        
        dtSum = 0.0
        iterCount = 0        
        underFreq = 0
        overFreq = 0
        rightFreq = 0
        acceptableFreq = 0
        
        diff = 0.0
        
        self._previousTime = time.time()
        time.sleep(self._period)
        while self._isRunning:
        
            t0 = time.time()
        
            self._calculate()
            
            calculationTime = time.time() - t0
            dtSum += calculationTime
            iterCount += 1
                 
            if self._currentPeriod < self._minPeriod:
                overFreq += 1
            elif self._currentPeriod >= self._minPeriod and self._currentPeriod <= self._period:
                rightFreq += 1
            elif self._currentPeriod > self._period and self._currentPeriod <= self._maxPeriod:
                acceptableFreq += 1
            else:
                underFreq += 1
                freq = 1.0/self._maxPeriod
                currentFreq = 1.0/self._currentPeriod
                message="I cannot operate at min. {0:.3f}Hz. Current rate is {1:.3f}Hz".format(freq, currentFreq)
                #print message
                logging.warn(message)

            diff += self._periodTarget - self._currentPeriod
            sleepTime = self._period - calculationTime + 0.1 * diff
            if sleepTime > 0.0:            
                time.sleep(sleepTime)
            else:
                time.sleep(0.001)

                
        if dtSum != 0.0 and iterCount != 0:
            tAvg = dtSum * 1000.0 / iterCount
            fAvg = float(iterCount) / dtSum
        else:
            tAvg = 0.0
            fAvg = float("inf")
            
        message = "PID-\"{0}\" (net values) t: {1:.3f}ms; f: {2:.3f}Hz".format(self._pidName, tAvg, fAvg)
        logging.info(message)
        #print message
        
        underFreqPerc = underFreq * 100.0 / iterCount
        overFreqPerc = overFreq * 100.0 / iterCount
        rightFreqPerc = rightFreq * 100.0 / iterCount
        acceptableFreqPerc = acceptableFreq * 100.0 / iterCount       
        message = "In freq: {0:.3f}%; Acceptable: {1:.3f}%; Under f.: {2:.3f}%; Over f.: {3:.3f}%"\
            .format(rightFreqPerc, acceptableFreqPerc, underFreqPerc, overFreqPerc)
        logging.info(message)
        #print message
        
    
    def start(self):
        """
        Starts stabilization.
        Inits a thread to perform calculations in background
        """
        
        if self._thread == None or not self._thread.isAlive():
            
            logging.info("Starting PID-\"{0}\"".format(self._pidName))

            self._deltaTimeSum = 0.0
            self._iterationCount = 0
            
            #Reset PID variables
            length = len(self._kp)
            self._integrals = [0.0] * length
            self._lastErrors = [0.0] * length
            
            self._isRunning = True
            self._thread = Thread(target=self._do)
            self._thread.start()
            
        
    def stop(self):
        """
        Stops the stabilization.
        """
        
        self._isRunning = False        
        if self._thread != None and self._thread.isAlive():
            
            self._thread.join()
            
            if self._iterationCount != 0 and self._deltaTimeSum:
                
                averageDeltaTime = self._deltaTimeSum * 1000.0/ self._iterationCount
                averageFrequency = self._iterationCount / self._deltaTimeSum
                
            else:
                
                averageDeltaTime = 0.0
                averageFrequency = float("inf")
                
            message = "PID-\"{0}\" - Avg. time: {1:.3f}ms - Avg. freq: {2:.3f}Hz".format(self._pidName, averageDeltaTime, averageFrequency)
            #print message
            logging.info(message)
                
    
    def isRunning(self):
        """
        @return: Reports whether the PID stabilization is currently running
        """
        
        return self._isRunning
    
    
    def lockIntegral(self, index):
        """
        Locks the result's integral part of any item
        @param index: Item index 
        """
        
        self._integralLocked[index] = True
        
    
    def unlockIntegral(self, index):
        """
        Unlocks the result's integral part of any item
        @param index: Item index
        """
        
        self._integralLocked[index] = False
        
    
    def resetIntegral(self, index):
        """
        Sets to zero the integral of any item
        @param index: Item index
        """
        
        self._integrals[index] = 0.0
    
    
    def resetTime(self):
        """
        Resets the time
        """
        
        self._previousTime = time.time()
