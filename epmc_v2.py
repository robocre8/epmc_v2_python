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

        try:
            payload = self.ser.read(4)
            if len(payload) != 4:
                print("[EPMC SERIAL COMM]: Timeout while reading 4 bytes")
                return False, [0.0]

            # Unpack 4 bytes as little-endian float
            (val,) = struct.unpack('<f', payload)
            return True, [val]

        except serial.SerialException as e:
            print(f"[EPMC SERIAL COMM]: Serial error — {e}")
            return False, [0.0]
        
    def read_packet2(self):
        """
        Reads 8 bytes from the serial port and converts to a float (little-endian).
        Returns (success, value-array)
        """
        try:
            payload = self.ser.read(8)
            if len(payload) != 8:
                print("[EPMC SERIAL COMM]: Timeout while reading 8 bytes")
                return False, [0.0, 0.0]

            # Unpack 4 bytes as little-endian float
            a, b = struct.unpack('<ff', payload)
            return True, [a, b]

        except serial.SerialException as e:
            print(f"[EPMC SERIAL COMM]: Serial error — {e}")
            return False, [0.0, 0.0]
        
    def read_packet3(self):
        """
        Reads 12 bytes from the serial port and converts to a float (little-endian).
        Returns (success, value-array)
        """
        try:
            payload = self.ser.read(12)
            if len(payload) != 12:
                print("[EPMC SERIAL COMM]: Timeout while reading 12 bytes")
                return False, [0.0, 0.0, 0.0]

            # Unpack 4 bytes as little-endian float
            a, b, c = struct.unpack('<fff', payload)
            return True, [a, b, c]

        except serial.SerialException as e:
            print(f"[EPMC SERIAL COMM]: Serial error — {e}")
            return False, [0.0, 0.0, 0.0]
    
    def read_packet4(self):
        """
        Reads 16 bytes from the serial port and converts to a float (little-endian).
        Returns (success, value-array)
        """
        try:
            payload = self.ser.read(16)
            if len(payload) != 16:
                print("[EPMC SERIAL COMM]: Timeout while reading 16 bytes")
                return False, [0.0, 0.0, 0.0, 0.0]

            # Unpack 4 bytes as little-endian float
            a, b, c, d = struct.unpack('<ffff', payload)
            return True, [a, b, c, d]

        except serial.SerialException as e:
            print(f"[EPMC SERIAL COMM]: Serial error — {e}")
            return False, [0.0, 0.0, 0.0, 0.0]
    
    def read_packet6(self):
        """
        Reads 24 bytes from the serial port and converts to a float (little-endian).
        Returns (success, value-array)
        """
        try:
            payload = self.ser.read(24)
            if len(payload) != 24:
                print("[EPMC SERIAL COMM]: Timeout while reading 24 bytes")
                return False, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

            # Unpack 4 bytes as little-endian float
            a, b, c, d, e, f = struct.unpack('<ffffff', payload)
            return True, [a, b, c, d, e, f]

        except serial.SerialException as e:
            print(f"[EPMC SERIAL COMM]: Serial error — {e}")
            return False, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    
    def read_packet8(self):
        """
        Reads 32 bytes from the serial port and converts to a float (little-endian).
        Returns (success, value-array)
        """
        try:
            payload = self.ser.read(32)
            if len(payload) != 32:
                print("[EPMC SERIAL COMM]: Timeout while reading 32 bytes")
                return False, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

            # Unpack 4 bytes as little-endian float
            a, b, c, d, e, f, g, h = struct.unpack('<ffffffff', payload)
            return True, [a, b, c, d, e, f, g, h]

        except serial.SerialException as e:
            print(f"[EPMC SERIAL COMM]: Serial error — {e}")
            return False, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    
    #---------------------------------------------------------------------

    def write_data1(self, cmd, pos, val):
        payload = struct.pack('<Bf', pos, val)
        self.send_packet_with_payload(cmd, payload)
        success, val_arr = self.read_packet1()
        return success, val_arr[0]

    def read_data1(self, cmd, pos):
        payload = struct.pack('<Bf', pos, 0.0)  # big-endian
        self.send_packet_with_payload(cmd, payload)
        success, val_arr = self.read_packet1()
        return success, val_arr[0]
    
    def write_data2(self, cmd, a, b):
        payload = struct.pack('<ff', a,b) 
        self.send_packet_with_payload(cmd, payload)

    def read_data2(self, cmd):
        self.send_packet_without_payload(cmd)
        success, val_arr = self.read_packet2()
        return success, val_arr
    
    def write_data3(self, cmd, a, b, c):
        payload = struct.pack('<fff', a,b,c) 
        self.send_packet_with_payload(cmd, payload)

    def read_data3(self, cmd):
        self.send_packet_without_payload(cmd)
        success, val_arr = self.read_packet3()
        return success, val_arr

    def write_data4(self, cmd, a, b, c, d):
        payload = struct.pack('<ffff', a,b,c,d) 
        self.send_packet_with_payload(cmd, payload)

    def read_data4(self, cmd):
        self.send_packet_without_payload(cmd)
        success, val_arr = self.read_packet4()
        return success, val_arr
    
    def write_data6(self, cmd, a, b, c, d, e, f):
        payload = struct.pack('<ffffff', a,b,c,d,e,f) 
        self.send_packet_with_payload(cmd, payload)

    def read_data6(self, cmd):
        self.send_packet_without_payload(cmd)
        success, val_arr = self.read_packet6()
        return success, val_arr
        
    def write_data8(self, cmd, a, b, c, d, e, f, g, h):
        payload = struct.pack('<ffffffff', a,b,c,d,e,f,g,h) 
        self.send_packet_with_payload(cmd, payload)

    def read_data8(self, cmd):
        self.send_packet_without_payload(cmd)
        success, val_arr = self.read_packet8()
        return success, val_arr
    
    #---------------------------------------------------------------------

    def writeSpeed(self, v0, v1, v2, v3):
        self.write_data4(WRITE_VEL, v0, v1, v2, v3)
    
    def writePWM(self, v0, v1, v2, v3):
        self.write_data4(WRITE_PWM, v0, v1, v2, v3)
    
    def readPos(self):
        success, pos_arr = self.read_data4(READ_POS)
        return success, pos_arr
    
    def readVel(self):
        success, vel_arr = self.read_data4(READ_VEL)
        return success, vel_arr
    
    def readUVel(self):
        success, vel_arr = self.read_data4(READ_UVEL)
        return success, vel_arr
    
    def setCmdTimeout(self, timeout):
        success, res = self.write_data1(SET_CMD_TIMEOUT, 100, timeout)
        return success
        
    def getCmdTimeout(self):
        success, res = self.read_data1(GET_CMD_TIMEOUT, 100)
        if success:
            return success, int(res)
        else:
            return success, 0
    
    def setPidMode(self, motor_no, mode):
        success, res = self.write_data1(SET_PID_MODE, motor_no, mode)
        return success
    
    def getPidMode(self, motor_no):
        success, mode = self.read_data1(GET_CMD_TIMEOUT, motor_no)
        if success:
            return success, int(mode)
        else:
            return success, 0
    
    def clearDataBuffer(self):
        success, res = self.write_data1(CLEAR_DATA_BUFFER, 100, 0.0)
        return success
    
    #---------------------------------------------------------------------

    def readMotorData(self):
        success, data_arr = self.read_data8(READ_MOTOR_DATA)
        return success, data_arr
    
    #---------------------------------------------------------------------