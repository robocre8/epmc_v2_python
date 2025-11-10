from epmc_v2 import EPMC_V2
import time

lowTargetVel = 0.00 # in rad/sec
highTargetVel = 5.00 # in rad/sec

prevTime = None
sampleTime = 0.015

ctrlPrevTime = None
ctrlSampleTime = 5.0
sendHigh = True

motorControl = EPMC_V2('/dev/ttyACM0')

#wait for the EPMC to fully setup
for i in range(3):
  time.sleep(1.0)
  print(f'configuring controller: {i+1} sec')

motorControl.clearDataBuffer()
motorControl.writeSpeed(0.0, 0.0)
print('configuration complete')

motorControl.setCmdTimeout(10000)
timeout = motorControl.getCmdTimeout()
print("command timeout in ms: ", timeout)


motorControl.writeSpeed(lowTargetVel, lowTargetVel) # targetA, targetB
sendHigh = True

prevTime = time.time()
ctrlPrevTime = time.time()
while True:
  if time.time() - ctrlPrevTime > ctrlSampleTime:
    if sendHigh:
      print("command high")
      motorControl.writeSpeed(highTargetVel, highTargetVel) # targetA, targetB
      highTargetVel = highTargetVel*-1
      sendHigh = False
    else:
      print("command low")
      motorControl.writeSpeed(lowTargetVel, lowTargetVel) # targetA, targetB
      sendHigh = True
    
    
    ctrlPrevTime = time.time()



  if time.time() - prevTime > sampleTime:
    try:
      pos0, pos1, v0, v1 = motorControl.readMotorData()

      print(f"motor0_readings: [{pos0}, {v0}]")
      print(f"motor1_readings: [{pos1}, {v1}]")
      print("")
    except:
      pass
    
    prevTime = time.time()
