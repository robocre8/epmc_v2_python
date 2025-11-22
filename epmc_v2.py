import serial
import struct

class EPMCSerialError(Exception):
        """Custom exception for for EPMC Comm failure"""
        pass


# Serial Protocol Command IDs -------------
START_BYTE = 0xAA
WRITE_VEL = 0x01
WRITE_PWM = 0x02
READ_POS = 0x03
READ_VEL = 0x04
READ_UVEL = 0x05
READ_TVEL = 0x06
SET_PPR = 0x07
GET_PPR = 0x08
SET_KP = 0x09
GET_KP = 0x0A
SET_KI = 0x0B
GET_KI = 0x0C
SET_KD = 0x0D
GET_KD = 0x0E
SET_RDIR = 0x0F
GET_RDIR = 0x10
SET_CUT_FREQ = 0x11
GET_CUT_FREQ = 0x12
SET_MAX_VEL = 0x13
GET_MAX_VEL = 0x14
SET_PID_MODE = 0x15
GET_PID_MODE = 0x16
SET_CMD_TIMEOUT = 0x17
GET_CMD_TIMEOUT = 0x18
SET_I2C_ADDR = 0x19
GET_I2C_ADDR = 0x1A
RESET_PARAMS = 0x1B
READ_MOTOR_DATA = 0x2A
CLEAR_DATA_BUFFER = 0x2C
#---------------------------------------------



class EPMC_V2:
    def __init__(self, port, baud=115200, timeOut=0.1):
        self.ser = serial.Serial(port, baud, timeout=timeOut)
        
    #------------------------------------------------------------------------
    def send_packet_without_payload(self, cmd):
        length = 0
        packet = bytearray([START_BYTE, cmd, length])
        checksum = sum(packet) & 0xFF
        packet.append(checksum)
        self.ser.write(packet)

    def send_packet_with_payload(self, cmd, payload_bytes):
        length = len(payload_bytes)
        packet = bytearray([START_BYTE, cmd, length]) + payload_bytes
        checksum = sum(packet) & 0xFF
        packet.append(checksum)
        self.ser.write(packet)

    def read_packet1(self):
        """
        Reads 4 bytes from the serial port and converts to a float (little-endian).
        Returns (success, value-array)
        """
        payload = self.ser.read(4)
        if len(payload) != 4:
            print("[EPMC SERIAL ERROR]: Timeout while reading 1 values")
            raise EPMCSerialError("[EPMC SERIAL ERROR]: Timeout while reading 1 value")

        # Unpack 4 bytes as little-endian float
        (val,) = struct.unpack('<f', payload)
        return val
    
    def read_packet4(self):
        """
        Reads 16 bytes from the serial port and converts to a float (little-endian).
        Returns (success, value-array)
        """
        payload = self.ser.read(16)
        if len(payload) != 16:
            print("[EPMC SERIAL ERROR]: Timeout while reading 4 values")
            raise EPMCSerialError("[EPMC SERIAL ERROR]: Timeout while reading 4 values")

        # Unpack 4 bytes as little-endian float
        a, b, c, d = struct.unpack('<ffff', payload)
        return a, b, c, d
    
    def read_packet8(self):
        """
        Reads 32 bytes from the serial port and converts to a float (little-endian).
        Returns (success, value-array)
        """
        payload = self.ser.read(32)
        if len(payload) != 32:
            print("[EPMC SERIAL ERROR]: Timeout while reading 8 values")
            raise EPMCSerialError("[EPMC SERIAL ERROR]: Timeout while reading 8 values")

        # Unpack 4 bytes as little-endian float
        a, b, c, d, e, f, g, h = struct.unpack('<ffffffff', payload)
        return a, b, c, d, e, f, g, h
    
    #---------------------------------------------------------------------

    def write_data1(self, cmd, pos, val):
        payload = struct.pack('<Bf', pos, val)
        self.send_packet_with_payload(cmd, payload)
        val = self.read_packet1()
        return val

    def read_data1(self, cmd, pos):
        payload = struct.pack('<Bf', pos, 0.0)  # big-endian
        self.send_packet_with_payload(cmd, payload)
        val = self.read_packet1()
        return val

    def write_data4(self, cmd, a, b, c, d):
        payload = struct.pack('<ffff', a,b,c,d) 
        self.send_packet_with_payload(cmd, payload)

    def read_data4(self, cmd):
        self.send_packet_without_payload(cmd)
        a, b, c, d = self.read_packet4()
        return a, b, c, d
    
    def read_data8(self, cmd):
        self.send_packet_without_payload(cmd)
        a, b, c, d, e, f, g, h = self.read_packet8()
        return a, b, c, d, e, f, g, h
    
    #---------------------------------------------------------------------

    def writeSpeed(self, v0, v1, v2=0.0, v3=0.0):
        self.write_data4(WRITE_VEL, v0, v1, v2, v3)
    
    def writePWM(self, pwm0, pwm1, pwm2=0, pwm3=0):
        self.write_data4(WRITE_PWM, pwm0, pwm1, pwm2, pwm3)
    
    def readPos(self):
        pos0, pos1, pos2, pos3 = self.read_data4(READ_POS)
        return round(pos0, 2), round(pos1, 2), round(pos2, 2), round(pos3, 2)
    
    def readVel(self):
        vel0, vel1, vel2, vel3 = self.read_data4(READ_VEL)
        return round(vel0, 4), round(vel1, 4), round(vel2, 4), round(vel3, 4)
    
    def readUVel(self):
        vel0, vel1, vel2, vel3 = self.read_data4(READ_UVEL)
        return round(vel0, 4), round(vel1, 4), round(vel2, 4), round(vel3, 4)
    
    def readTVel(self):
        vel0, vel1, vel2, vel3 = self.read_data4(READ_TVEL)
        return round(vel0, 4), round(vel1, 4), round(vel2, 4), round(vel3, 4)
    
    def setCmdTimeout(self, timeout):
        res = self.write_data1(SET_CMD_TIMEOUT, 100, timeout)
        return int(res)
        
    def getCmdTimeout(self):
        timeout = self.read_data1(GET_CMD_TIMEOUT, 100)
        return int(timeout)
    
    def setPidMode(self, mode):
        res = self.write_data1(SET_PID_MODE, 100, mode)
        res = True if int(res) == 1 else False
        return res
    
    def getPidMode(self):
        mode = self.read_data1(GET_CMD_TIMEOUT, 100)
        return int(mode)
    
    def clearDataBuffer(self):
        res = self.write_data1(CLEAR_DATA_BUFFER, 100, 0.0)
        res = True if int(res) == 1 else False
        return res
    
    #---------------------------------------------------------------------

    def readMotorData(self):
        pos0, pos1, pos2, pos3, vel0, vel1, vel2, vel3 = self.read_data8(READ_MOTOR_DATA)
        return round(pos0, 2), round(pos1, 2), round(pos2, 2), round(pos3, 2), round(vel0, 4), round(vel1, 4), round(vel2, 4), round(vel3, 4)
    
    #---------------------------------------------------------------------