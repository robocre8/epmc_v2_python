import time
from epmc_v2 import EPMC_V2

port = '/dev/ttyUSB0'
epmcV2 = EPMC_V2(port)

def main():
  for i in range(3):
    time.sleep(1.0)
    print(i+1, " sec")

  res = epmcV2.setUseIMU(1)
  print(res)

if __name__ == "__main__":
  main()