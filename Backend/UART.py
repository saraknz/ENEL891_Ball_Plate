# Servo Controller
# Sets a UART Controller on specified UART device with baud of 9600

import serial

class UART:

    # Constants for maximum angle deflection from 90 degrees
    MAX_DEFLECTION = 20
    X_ANGLE_TUNER =  0 * 2      # Values for ANGLE_TUNER is [desired angle] * 2
    Y_ANGLE_TUNER = 0 * 2

    def __init__(self, uartDevicePath):
        ''' Constructor which sets the Serial Port and flushes any pending data '''
        global serialPort
        serialPort = serial.Serial(uartDevicePath, 9600, timeout=1)
        serialPort.flush()

    @staticmethod
    def sendXServo(servoXAngle):
        ''' Transmits the Servo Angle for the X Rotation Axis over UART '''
        xAngleBits = UART.__convertAngle__(servoXAngle + UART.X_ANGLE_TUNER)
        xByte = UART.__generateUARTData__(xAngleBits, 1)
        UART.__uartTX__(xByte)

    @staticmethod 
    def sendYServo(servoYAngle):
        ''' Transmits the Servo Angle for the Y Rotation Axis over UART '''
        yAngleBits = UART.__convertAngle__(servoYAngle + UART.Y_ANGLE_TUNER)
        yByte = UART.__generateUARTData__(yAngleBits, 0)
        UART.__uartTX__(yByte)
        
    @staticmethod 
    def __convertAngle__(angle):

        ''' Converts a Given Angle into the 7-bit value required by the FPGA '''

        # Check if angle is a number between 0 to 180 deg, otherwise throw exception
        try:
            angle = int(angle)
        except ValueError:
            raise ValueError("The angle specified is not a valid numerical value.")

        if (angle > 180 or angle < 0):
            raise ValueError("The angle specified is outside the scope of this servo.")

        # If angle is greater than bound, then set to the maximum
        if (abs(angle - 90) < UART.MAX_DEFLECTION):
            angle = angle / abs(angle) * UART.MAX_DEFLECTION

        # If value is okay, then convert into closest binary representation
        binaryPos = ((angle - 70) / 0.5)
        binaryPos = int(binaryPos)
        return binaryPos

    @staticmethod 
    def __generateUARTData__(binaryPosition, isYServo):
        ''' Takes the Binary Position Data and Servo Select and generates the 8-bit value '''
        # Assembles the byte
        if (isYServo == 1):
            byteInt = binaryPosition + 128
        else:
            byteInt = binaryPosition
        
        byte = [byteInt]

        return bytearray(byte)

    @staticmethod
    def __uartTX__(data):
        ''' Performs the UART TX for some given data '''
        global serialPort
        size = serialPort.write(data)