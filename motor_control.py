import time
from epmc_v2 import EPMC_V2

port = '/dev/ttyACM0'
epmcV2 = EPMC_V2(port)

if __name__ == '__main__':
  
  time.sleep(2.0)

  # left wheels (motor 0 and motor 2)
  # right wheels (motor 1 and motor 3)
  # epmcV2.writeSpeed(0.0, 0.0, 0.0, 0.0)

  epmcV2.setCmdTimeout(6000)
  timeout = epmcV2.getCmdTimeout()
  print("command timeout in ms: ", timeout)

  lowTargetVel = -3.142 # in rad/sec
  highTargetVel = 6.284 # in rad/sec

  prevTime = None
  sampleTime = 0.02

  ctrlPrevTime = None
  ctrlSampleTime = 4.0
  sendHigh = True


  # left wheels (motor 0 and motor 2)
  # right wheels (motor 1 and motor 3)
  # epmcV2.writeSpeed(lowTargetVel, lowTargetVel)
  epmcV2.writePWM(0, 0)

  sendHigh = True

  prevTime = time.time()
  ctrlPrevTime = time.time()
  
  while True:
    if time.time() - ctrlPrevTime > ctrlSampleTime:
      if sendHigh:
        # left wheels (motor 0 and motor 2)
        # right wheels (motor 1 and motor 3)
        # epmcV2.writeSpeed(highTargetVel, highTargetVel)
        epmcV2.writePWM(80, 80)

        sendHigh = False
      else:
        # left wheels (motor 0 and motor 2)
        # right wheels (motor 1 and motor 3)
        # epmcV2.writeSpeed(lowTargetVel, lowTargetVel)
        epmcV2.writePWM(150, 150)

        sendHigh = True
      
      ctrlPrevTime = time.time()



    if time.time() - prevTime > sampleTime:
      try:
        # left wheels (motor 0 and motor 2)
        # right wheels (motor 1 and motor 3)
        # pos0, pos1, pos2, pos3 = epmcV2.readPos()
        # v0, v1, v2, v3 = epmcV2.readVel()

        pos0, pos1, v0, v1 = epmcV2.readMotorData()
        
        print("-----------------------------------------")
        print(f"motor0_readings: [{pos0}, {v0}]")
        print(f"motor1_readings: [{pos1}, {v1}]")
        print("-----------------------------------------\n")

      except:
        pass
      
      prevTime = time.time()