'''
Created on 24 ene. 2017

@author: david
'''
from time import sleep

from config import Configuration
from sensor.imu6050dmp import Imu6050Dmp
from servo.driver import Driver
from stabilization.stabilizator import Stabilizator


def main():
    
    configManager = Configuration.getInstance()
    configManager.read()
    configManager.save()
    
    config = configManager.getConfig()
        
    stabilizator = Stabilizator(Imu6050Dmp(), Driver(2, config[Configuration.KEY_MOTOR_CLASS]), config[Configuration.PID_PERIOD], 2)
    stabilizator.setPidConstants(config[Configuration.PID_KP], config[Configuration.PID_KI], config[Configuration.PID_KD])
    stabilizator.start()
    
    try:
        while True:
            sleep(0.2)
    except:
        stabilizator.stop() 

if __name__ == '__main__':
    main()