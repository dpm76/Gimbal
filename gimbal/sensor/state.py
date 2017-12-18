# -*- coding: utf-8 -*-
'''
Created on 23 de feb. de 2016

@author: david
'''

class SensorState(object):
    '''
    Sensor's state
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        self.accels = [0.0]*3
        self.angleSpeeds = [0.0]*3
        self.angles = [0.0]*3
