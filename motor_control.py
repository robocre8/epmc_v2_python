import time
from epmc_v2 import EPMC_V2

port = '/dev/ttyUSB0'
epmcV2 = EPMC_V2(port)

if __name__ == '__main__':
  
  time.sleep(2.0)

  # left wheels (motor 0 and motor 2)
  # right wheels (motor 1 and motor 3)
  epmcV2.writeSpeed(0.0, 0.0, 0.0, 0.0)
  epmcV2.clearDataBuffer()

  epmcV2.setCmdTimeout(6000)
  timeout = epmcV2.getCmdTimeout()
  print("command timeout in ms: ", timeout)

  lowTargetVel = 0.00 # in rad/sec
  highTargetVel = 3.142 # in rad/sec

  prevTime = None
  sampleTime = 0.02

  ctrlPrevTime = None
  ctrlSampleTime = 4.0
  sendHigh = True


  # left wheels (motor 0 and motor 2)
  # right wheels (motor 1 and motor 3)
  epmcV2.writeSpeed(lowTargetVel, lowTargetVel, lowTargetVel, lowTargetVel)

  sendHigh = True

  prevTime = time.time()
  ctrlPrevTime = time.time()
  
  while True:
    if time.time() - ctrlPrevTime > ctrlSampleTime:
      if sendHigh:
        # left wheels (motor 0 and motor 2)
        # right wheels (motor 1 and motor 3)
        epmcV2.writeSpeed(highTargetVel, highTargetVel, highTargetVel, highTargetVel)

        sendHigh = False
      else:
        # left wheels (motor 0 and motor 2)
        # right wheels (motor 1 and motor 3)
        epmcV2.writeSpeed(lowTargetVel, lowTargetVel, lowTargetVel, lowTargetVel)

        sendHigh = True
      
      ctrlPrevTime = time.time()



    if time.time() - prevTime > sampleTime:
      try:
        # left wheels (motor 0 and motor 2)
        # right wheels (motor 1 and motor 3)
        # pos0, pos1, pos2, pos3 = epmcV2.readPos()
        # v0, v1, v2, v3 = epmcV2.readVel()

        pos0, pos1, pos2, pos3, v0, v1, v2, v3 = epmcV2.readMotorData()
        
        print("-----------------------------------------")
        print("left wheels - motor 0 and motor 2")
        print(f"motor0_readings: [{pos0}, {v0}]")
        print(f"motor2_readings: [{pos2}, {v2}]\n")

        print("right wheels - motor 1 and motor 3")
        print(f"motor1_readings: [{pos1}, {v1}]")
        print(f"motor3_readings: [{pos3}, {v3}]")
        print("-----------------------------------------\n")

      except:
        pass
      
      prevTime = time.time()