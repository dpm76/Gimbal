from sensor.imu6050dmp import Imu6050Dmp
from time import time, sleep

sensor = Imu6050Dmp()
sensor.start()
sleep(0)
sensor.resetGyroReadTime()
sleep(0)

n = 0
timeStart = time()

try:
  while True:
    n += 1
    sensor.refreshState()
    #angles = sensor.readDeviceAngles()
    #print(angles)
except KeyboardInterrupt:
  pass
finally:
  timeEnd = time()
  sensor.stop()
  avgTime = (timeEnd - timeStart)/n
  freq = 1.0/avgTime
  print("Avg. Time={0}; Freq={1}".format(avgTime, freq))
