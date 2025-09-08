import serial
import struct


# Serial Protocol Command IDs -------------
START_BYTE = 0xAA
WRITE_VEL = 0x01
WRITE_PWM = 0x02
READ_POS = 0x03
READ_VEL = 0x04
READ_UVEL = 0x05
SET_PID_MODE = 0x15
GET_PID_MODE = 0x16
SET_CMD_TIMEOUT = 0x17
GET_CMD_TIMEOUT = 0x18
SET_USE_IMU = 0x1C
GET_USE_IMU = 0x1D
READ_ACC = 0x1E
READ_ACC_VAR = 0x21
READ_GYRO = 0x24
READ_GYRO_VAR = 0x27
#---------------------------------------------



class EPMC_V2:
    def __init__(self, port, baud=921600, timeOut=0.1):
        self.ser = serial.Serial(port, baud, timeout=timeOut)
    
    #------------------------------------------------------------------------
    def send_packet(self, cmd):
        length = 0
        packet = bytearray([START_BYTE, cmd, length])
        checksum = sum(packet) & 0xFF
        packet.append(checksum)
        self.ser.write(packet)

    def send_packet_stream(self, cmd, payload_bytes):
        length = len(payload_bytes)
        packet = bytearray([START_BYTE, cmd, length]) + payload_bytes
        checksum = sum(packet) & 0xFF
        packet.append(checksum)
        self.ser.write(packet)

    def read_packet(self):
        payload = self.ser.read(4)
        a = struct.unpack('<f', payload)[0]  # little-endian float
        return a

    def read_packet_stream(self):
        payload = self.ser.read(16)
        a, b, c, d = struct.unpack('<ffff', payload)  # little-endian float
        return a, b, c, d
    
    #---------------------------------------------------------------------

    def write_data(self, cmd, pos, val):
        payload = struct.pack('<Bf', pos, val)
        self.send_packet_stream(cmd, payload)
        val = self.read_packet()
        return val

    def read_data(self, cmd, pos):
        payload = struct.pack('<Bf', pos, 0.0)  # big-endian
        self.send_packet_stream(cmd, payload)
        val = self.read_packet()
        return val

    def write_data_stream(self, cmd, a, b, c, d):
        payload = struct.pack('<ffff', a,b,c,d) 
        self.send_packet_stream(cmd, payload)
        val = self.read_packet()
        return val

    def read_data_stream(self, cmd):
        self.send_packet(cmd)
        a, b, c, d = self.read_packet_stream()
        return a, b, c, d
        
    #---------------------------------------------------------------------

    def writeSpeed(self, v0, v1, v2, v3):
        res = self.write_data_stream(WRITE_VEL, v0, v1, v2, v3)
        return int(res)
    
    def writePWM(self, v0, v1, v2, v3):
        res = self.write_data_stream(WRITE_PWM, v0, v1, v2, v3)
        return int(res)
    
    def readPos(self):
        pos0, pos1, pos2, pos3 = self.read_data_stream(READ_POS)
        return round(pos0,4), round(pos1,4), round(pos2,4), round(pos3,4)
    
    def readVel(self):
        v0, v1, v2, v3 = self.read_data_stream(READ_VEL)
        return round(v0,6), round(v1,6), round(v2,6), round(v3,6)
    
    def readUVel(self):
        v0, v1, v2, v3 = self.read_data_stream(READ_UVEL)
        return round(v0,6), round(v1,6), round(v2,6), round(v3,6)
    
    def setCmdTimeout(self, timeout):
        res = self.write_data(SET_CMD_TIMEOUT, 0, timeout)
        return int(res)
    
    def getCmdTimeout(self):
        timeout = self.read_data(GET_CMD_TIMEOUT, 0)
        return int(timeout)
    
    def setPidMode(self, motor_no, mode):
        res = self.write_data(SET_PID_MODE, motor_no, mode)
        return int(res)
    
    def getPidMode(self, motor_no):
        mode = self.read_data(GET_CMD_TIMEOUT, motor_no)
        return int(mode)
    
    #---------------------------------------------------------------------

    def setUseIMU(self, val):
        res = self.write_data(SET_USE_IMU, 0, val)
        return int(res)
    
    def getUseIMU(self):
        val = self.read_data(GET_USE_IMU, 0)
        return val
    
    def readAcc(self):
        ax, ay, az, _ = self.read_data_stream(READ_ACC)
        return ax, ay, az
    
    def readAccVariance(self):
        ax, ay, az, _ = self.read_data_stream(READ_ACC_VAR)
        return ax, ay, az
    
    def readGyro(self):
        gx, gy, gz, _ = self.read_data_stream(READ_GYRO)
        return gx, gy, gz
    
    def readGyroVariance(self):
        gx, gy, gz, _ = self.read_data_stream(READ_GYRO_VAR)
        return gx, gy, gz
    
    #####################################################