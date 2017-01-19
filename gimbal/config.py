'''
Created on 20 de ene. de 2016

@author: david
'''
import json
from os import path


class Configuration(object):
    
    FILE_PATH = "./gimbal.config.json"
    
    KEY_MOTOR_CLASS = "motor-class"
    VALUE_MOTOR_CLASS_LOCAL = "local"
    VALUE_MOTOR_CLASS_DUMMY = "dummy"
    
    KEY_IMU_CLASS = "imu-class"
    VALUE_IMU_CLASS_6050 = "imu6050"
    VALUE_IMU_CLASS_DUMMY = "dummy"
    
    PID_KP = "PID_KP"
    PID_KI = "PID_KI"
    PID_KD = "PID_KD"
    
    DEFAULT_CONFIG = {
                      KEY_MOTOR_CLASS: VALUE_MOTOR_CLASS_DUMMY,
                      KEY_IMU_CLASS: VALUE_IMU_CLASS_DUMMY,
                      
                      PID_KP: [0.0, 0.0, 0.0],  
                      PID_KI: [0.0, 0.0, 0.0],  
                      PID_KD: [0.0, 0.0, 0.0]
                      }
    
    _instance = None
    
    @staticmethod
    def getInstance():
        
        if Configuration._instance == None:
            Configuration._instance = Configuration()
            
        return Configuration._instance
    

    def __init__(self):
        
        #Read stored config from file
        self._config = Configuration.DEFAULT_CONFIG.copy()
        
        if path.exists(Configuration.FILE_PATH):
    
            with open(Configuration.FILE_PATH, "r") as configFile:
                serializedConfig = " ".join(configFile.readlines())
                configFile.close()
                
            storedConfig = json.loads(serializedConfig)
            
            #Replace default config by stored config
            for key in self._config.keys():
                
                if key in storedConfig:
                    
                    self._config[key] = storedConfig[key]
                    
        #Write current config into file
        serializedConfig = json.dumps(self._config)        
        with open(Configuration.FILE_PATH, "w+") as configFile:
            configFile.write(serializedConfig + "\n")
            configFile.close()
            
            
    def getConfig(self):
        
        return self._config
