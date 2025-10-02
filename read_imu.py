import time
from epmc_v2 import EPMC_V2

port = '/dev/ttyUSB0'
epmcV2 = EPMC_V2(port)

def main():
  for i in range(2):
    time.sleep(1.0)
    print(i+1, " sec")

  prevTime = time.time()
  sampleTime = 0.01

  epmcV2.clearDataBuffer()

  while True:
    if time.time() - prevTime > sampleTime:
      try:
        use_imu = epmcV2.getUseIMU()
        if(use_imu == 1):
          r, p, y, ax, ay, az, gx, gy, gz = epmcV2.readImuData()

          print(f"r: {r}\tp: {p}\ty: {y}")
          print(f"ax: {ax}\tay: {ay}\taz: {az}")
          print(f"gx: {gx}\tgy: {gy}\tgz: {gz}\n")
        else:
          print("IMU Mode Not Activated")
      except:
        pass
      
      prevTime = time.time()

if __name__ == "__main__":
  main()