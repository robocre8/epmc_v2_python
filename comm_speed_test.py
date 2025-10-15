from epmc_v2 import EPMC_V2
import time


motorControl = EPMC_V2('/dev/ttyUSB0')

#wait for the EPMC to fully setup
for i in range(4):
  time.sleep(1.0)
  print(f'configuring controller: {i+1} sec')

motorControl.clearDataBuffer()
motorControl.writeSpeed(0.0, 0.0, 0.0, 0.0)
print('configuration complete')

motorControl.setCmdTimeout(5000)
timeout = motorControl.getCmdTimeout()
print("command timeout in ms: ", timeout)

angPos0 = 0.0
angPos1 = 0.0
angPos2 = 0.0
angPos3 = 0.0

angVel0 = 0.0
angVel1 = 0.0
angVel2 = 0.0
angVel3 = 0.0

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
      motorControl.writeSpeed(highTargetVel, highTargetVel, highTargetVel, highTargetVel) # targetA, targetB
      success, motor_data = motorControl.readMotorData()
      if success:
        angPos0 = round(motor_data[0], 2)
        angPos1 = round(motor_data[1], 2)
        angPos2 = round(motor_data[2], 2)
        angPos3 = round(motor_data[3], 2)

        angVel0 = round(motor_data[4], 4)
        angVel1 = round(motor_data[5], 4)
        angVel2 = round(motor_data[6], 4)
        angVel3 = round(motor_data[7], 4)
      dt = start_time - prevTime
      prevTime = start_time
      print(dt)
    except:
       pass


