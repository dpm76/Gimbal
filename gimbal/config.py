'''
Created on 20 de ene. de 2016

@author: david
'''
import json
from os import path
import logging


DEFAULT_FILE_PATH = "./config.json"

class Configuration(object):
    
    
    
    KEY_MOTOR_CLASS = "motor-class"
    VALUE_MOTOR_CLASS_LOCAL = "local"
    VALUE_MOTOR_CLASS_DUMMY = "dummy"
    
    KEY_IMU_CLASS = "imu-class"
    VALUE_IMU_CLASS_6050 = "imu6050"
    VALUE_IMU_CLASS_DUMMY = "dummy"
    
    PID_PERIOD = "pid-period"
    
    PID_KP = "PID_KP"
    PID_KI = "PID_KI"
    PID_KD = "PID_KD"
    
    DEFAULT_CONFIG = {
                      KEY_MOTOR_CLASS: VALUE_MOTOR_CLASS_DUMMY,
                      KEY_IMU_CLASS: VALUE_IMU_CLASS_DUMMY,
                      
                      PID_PERIOD: 0.1,
                      PID_KP: [0.0, 0.0],  
                      PID_KI: [0.0, 0.0],  
                      PID_KD: [0.0, 0.0]
                      }
    
    _instance = None
    
    @staticmethod
    def getInstance():
        """
        @return: Unique object instance
        """
        
        if Configuration._instance == None:
            Configuration._instance = Configuration()
            
        return Configuration._instance
    

    def __init__(self):
        """
        Constructor
        """        
        
        self._config = Configuration.DEFAULT_CONFIG.copy()
            
    
    def read(self, filepath=DEFAULT_FILE_PATH):
        """
        Reads stored configuration from file
        @param filepath: Configuration filepath
        """
        
        if path.exists(filepath):
    
            with open(filepath, "r") as configFile:
                serializedConfig = " ".join(configFile.readlines())
                configFile.close()
                
            storedConfig = json.loads(serializedConfig)
            
            #Replace default config by stored config
            for key in self._config.keys():
                
                if key in storedConfig:
                    
                    self._config[key] = storedConfig[key]
        else:
            logging.info("Configuration file {0} not found. Using default config.".format(filepath))            
                    
                    
    def save(self, filepath=DEFAULT_FILE_PATH):
        """
        Writes current configuration into file
        @param filepath: Configuration filepath
        """
        
        serializedConfig = json.dumps(self._config)        
        with open(filepath, "w+") as configFile:
            configFile.write(serializedConfig + "\n")
            configFile.close()
            
        
            
    def getConfig(self):
        
        return self._config
