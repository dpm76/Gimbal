from servo.motor import Motor
from time import time
from random import uniform

NEUTRAL_THROTTLE = Motor.MIN_THROTTLE + (Motor.MAX_THROTTLE - Motor.MIN_THROTTLE) / 2.0

motor0 = Motor(0, NEUTRAL_THROTTLE)
motor1 = Motor(1, NEUTRAL_THROTTLE)
n=0
motor0.start()
motor1.start()
startTime = time()
try:
  while True:
    throttle0 = uniform(0.0, 100.0)
    throttle1 = uniform(0.0, 100.0)
    motor0.setThrottle(throttle0)
    motor1.setThrottle(throttle1)
    n+=1
except KeyboardInterrupt:
  pass
finally:
  endTime = time()
  motor0.stop()
  motor1.stop()
  dTime = endTime - startTime
  avgTime = dTime/n
  freq = 1.0/avgTime
  print("Avg. time={0}; f={1}".format(avgTime, freq))



