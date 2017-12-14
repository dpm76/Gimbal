'''
Created on 24 ene. 2017

@author: david
'''
import logging
from time import sleep

from config import Configuration
from servo.driver import Driver
from stabilization.stabilizator import Stabilizator


def main():

    logging.basicConfig(level=logging.INFO)
    
    configManager = Configuration.getInstance()
    configManager.read()
    configManager.save()
    
    config = configManager.getConfig()
            
    stabilizator = Stabilizator(config[Configuration.KEY_IMU_CLASS], Driver(2, config[Configuration.KEY_MOTOR_CLASS]), config[Configuration.PID_PERIOD], 2)
    stabilizator.setPidConstants(config[Configuration.PID_KP], config[Configuration.PID_KI], config[Configuration.PID_KD])
    stabilizator.start()
    print "started!"
    logging.info("Started! Press Ctrl+C to stop.")
    
    try:
        while True:
            sleep(0.2)
    except:
        stabilizator.stop() 

if __name__ == '__main__':
    main()
