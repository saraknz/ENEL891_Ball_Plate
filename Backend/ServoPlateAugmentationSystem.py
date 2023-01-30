import threading
import time
import numpy
from Backend import UART

class ServoPlateAugmentationSystem(threading.Thread):

    # Constants
    MAX_ANGLE = 15          # Maximum Delfection Angle
    MAX_DELTA_ANGLE = 5     # Maximum Rate of change of Deflection Angle / sec
    INSTRUCTIONS_PER_SECOND = 5

    def __init__(self, devicePath, baud, bits, enableVerbose):
        threading.Thread.__init__(self)
        self.baudDelay = ServoPlateAugmentationSystem.__calculateDelay__(baud, bits)
        self.framePerSec = baud / bits
        self.dTheta = ServoPlateAugmentationSystem.MAX_DELTA_ANGLE/self.framePerSec
        self.frameHoldMax = (self.framePerSec / ServoPlateAugmentationSystem.INSTRUCTIONS_PER_SECOND) - 1
        
        # Initalise variables
        self.setXAngle = 0
        self.setYAngle = 0
        self.currXAngle = 0
        self.currYAngle = 0
        self.frameHoldCounter = 0

        # Create UART Controller
        self.uart = UART.UART(devicePath)

        # Operating Flags
        self.enableVerbose = enableVerbose
        self.keepRunning = True
        self.pause = False

    @staticmethod
    def __calculateDelay__(baud, bits):
        '''
        Calculate the delay used based on the Baud Rate and number of Bits per packet. 
        Method is able to be modified further to add/remove delays to compesnate for python execution.
        '''
        period = 1 / (baud / bits)
        return period

    @staticmethod
    def __convAngleToServo__(servoXAngle, servoYAngle):
        ''' Convert from plate axis system to servo axis system. '''
        servoXAngle = 90 - servoXAngle
        servoYAngle = 90 + servoYAngle
        return servoXAngle, servoYAngle

    @staticmethod
    def __setMaxAngle__(angle):
        ''' Limits the Maximum Angle '''
        if abs(angle) > ServoPlateAugmentationSystem.MAX_ANGLE:
            return numpy.sign(angle) * ServoPlateAugmentationSystem.MAX_ANGLE
        else:
            return angle

    @staticmethod
    def __setStepAngle__(desiredAngle, currentAngle):
        
        # Get delta
        delta = abs(desiredAngle) - abs(currentAngle)

        # If delta is too great, then set the next angle
        if abs(delta) > ServoPlateAugmentationSystem.MAX_DELTA_ANGLE:
            return numpy.sign(delta) * ServoPlateAugmentationSystem.MAX_DELTA_ANGLE
        else:
            return desiredAngle

    def __plateAugmentation__(self):
        
        # If holdCounter is still active, then do not calculate and maintain
        self.frameHoldCounter += 1
        if self.frameHoldCounter < self.frameHoldMax:
            return self.currXAngle, self.currYAngle

        # Otherwise, determine new position
        # If angle is greater than desired freedom, limit
        servoX = ServoPlateAugmentationSystem.__setStepAngle__(self.setXAngle, self.currXAngle)
        servoY = ServoPlateAugmentationSystem.__setStepAngle__(self.setYAngle, self.currYAngle)

        # Set the new values for the current angles
        self.currXAngle = servoX
        self.currYAngle = servoY

        return self.currXAngle, self.currYAngle

    def setNextAngle(self, setXAngle, setYAngle):
        ''' Set a new desired angle for the servos in degrees. Maximum Angle enforced. '''
        self.setXAngle = ServoPlateAugmentationSystem.__setMaxAngle__(setXAngle)
        self.setYAngle = ServoPlateAugmentationSystem.__setMaxAngle__(setYAngle)

    def terminate(self):
        ''' Terminate the '''
        self.keepRunning = False

    def hold(self):
        ''' Hold the movement of the plate without terminating the thread. '''
        self.pause = True

    def resume(self):
        ''' Resume the movement of the plate without terminating the thread. '''
        self.pause = False

    def pauseResume(self):
        ''' Pause/Resume the movement of the plate without terminating the thread. '''
        self.pause = not self.pause

    def run(self):
        
        # Keep Thread alive unless the keepRunning flag is unset
        while self.keepRunning:

            # If not paused, continue to generate positions
            if not self.pause:
                
                # Get the next UART Instruction
                servoX, servoY = self.__plateAugmentation__()

                # Convert to Servo Angle system
                servoX, servoY = ServoPlateAugmentationSystem.__convAngleToServo__(servoX, servoY)
                
                # Send the Instruction
                self.uart.sendXServo(servoX)
                self.uart.sendYServo(servoY)

                # Show Debug
                if self.enableVerbose:
                    print("UART Tx sX: {}".format(servoX))
                    print("UART Tx sY: {}".format(servoY))
            
            # Put the thread to sleep for the baud delay
            time.sleep(self.baudDelay)