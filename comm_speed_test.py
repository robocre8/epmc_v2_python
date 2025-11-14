from epmc_v2 import EPMC_V2
import time


motorControl = EPMC_V2('/dev/ttyUSB0')

#wait for the EPMC to fully setup
for i in range(3):
  time.sleep(1.0)
  print(f'configuring controller: {i+1} sec')

motorControl.clearDataBuffer()
motorControl.writeSpeed(0.0, 0.0, 0.0, 0.0)
print('configuration complete')

motorControl.setCmdTimeout(5000)
timeout = motorControl.getCmdTimeout()
print("command timeout in ms: ", timeout)

lowTargetVel = -3.142 # in rad/sec
highTargetVel = 3.142 # in rad/sec

prevTime = None
sampleTime = 0.015

ctrlPrevTime = None
ctrlSampleTime = 5.0
sendHigh = True

sendHigh = True

prevTime = time.time()
ctrlPrevTime = time.time()
while True:
    try:
      start_time = time.time()
      motorControl.writeSpeed(highTargetVel, highTargetVel, highTargetVel, highTargetVel)
      pos0, pos1, pos2, pos3, v0, v1, v2, v3 = motorControl.readMotorData()
      dt = start_time - prevTime
      prevTime = start_time
      print(dt)
    except:
       pass


