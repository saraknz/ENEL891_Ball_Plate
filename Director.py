##
# To print the values found during the calculation process
# For testing purposes on Laptop, set for that situation
##

from typing import ValuesView
# Binary colour detection
#from Backend.ImgProcess import ImgProcess
# Orange colour detection
from Backend.ImageProcessor import ImageProcessor as ImgProcess
import threading
from queue import Queue
import numpy as np
from Backend import *
from PyQt5 import QtCore as qtc

# CONFIG

# Serial Port
BAUD_RATE = 9600
NUM_OF_BITS = 8

# PID Specifications
KP = 20 #2.768
KI = 1.08
KD = 15

MAX_X = 25
MAX_Y = 15

class Director(threading.Thread):

    # Initialise components for the Director
    def __init__(self, cameraID, serialAddress, frameCollector, verbose):
        
        # Run super class
        threading.Thread.__init__(self)

        # Aim for the setpoint in the Center of the Plate
        self.setpoint = [0,0]

        # PID Controllers for the Servos
        self.P_aX = 0
        self.P_aY = 0
        self.BP_x = 0
        self.BP_y = 0
        self.xAxis = PID.PID(KP, KI, KD, self.setpoint[0], False)
        self.yAxis = PID.PID(KP, KI, KD, self.setpoint[1], False)

        # Initialise the Image Processor Thread
        self.imgQueue = Queue()
        # self.imgProc = ImageProcessor.ImageProcessor(cameraID, self.imgQueue, False)
        self.imgProc = ImgProcess(cameraID, self.imgQueue, verbose)
        self.imgProc.start()

        # Initialise the Augmentation System and start Thread
        self.augmentation = ServoPlateAugmentationSystem.ServoPlateAugmentationSystem(serialAddress, BAUD_RATE, NUM_OF_BITS, 0)
        self.augmentation.start()

        # Flags for this Class
        self.enableVerbose = verbose
        self.returnPlateToFlat = False
        self.keepRunning = True

        # Link Frame Collector
        self.frameCollector = frameCollector
        # Mode
        # self.patternMode = PatternTypes.CENTER
    
    # The main loop for this thread
    def run(self):

        # Keep running this loop of code until the the "terminate" method is called
        while(self.keepRunning):
            self.__performLoopIteration__()
        
        # Safely destroy the image processor
        self.imgProc.destroyProcessor()

    # Method checks the queue and gets the latest frame
    def __getNextQueueImage__(self):

        # Review the current number of items in the queue
        queueSize = self.imgQueue.qsize()

        # If no items exist, reuturn null
        if (queueSize == 0):
            return None

        elif (queueSize == 1):
            return self.imgQueue.get_nowait()
            
        else:
            while(self.imgQueue.qsize() > 1):
                self.imgQueue.get_nowait()
                if self.enableVerbose:
                    print("Frame was flushed from Queue")
            return self.imgQueue.get_nowait()

    # Performs the logic needed for the Director to sequence the classes
    def __performLoopIteration__(self):

        # Grab the next Image from the Queue
        nextImg = self.__getNextQueueImage__()

        # If no image is queued, return.
        if nextImg == None:
            if self.enableVerbose:
                print("No Frame in Queue to Process")
            return

        # Transmit the frame of the ball to the GUI
        self.frameCollector.addFrame(nextImg)
        
        # If plate is being overriden to flat, then set servo position
        if self.returnPlateToFlat == True:
            if self.enableVerbose:
                print("Plate set to flatten")
            return

        # Otherwise, if image is returned...
        # If ball is found
        if (nextImg.isBallFound()):

            if self.enableVerbose:
                print("Ball Found in Frame")

            # Get Information
            self.BP_x, self.BP_y = nextImg.getBallPosition()
            timestamp = nextImg.getTimeStamp()

            # Send position data to the PID Controllers and determine the desired Plate Angles
            self.P_aX = self.xAxis.compute(self.BP_x, timestamp)
            self.P_aY = self.yAxis.compute(self.BP_y, timestamp)

            # Send the desired angle to SPAS for Augmentation and Tx
            self.augmentation.setNextAngle(self.P_aX, self.P_aY)

            # Print Verbose if Desired
            if (self.enableVerbose):
                print("Ball Pos X, Y: {}, {}".format(self.BP_x, self.BP_y))
                print("Plate Angle X, Y: {}, {}".format(self.P_aX, self.P_aY))

        else:
            if self.enableVerbose:
                print("Ball not found in frame")

    # Switch the mode of the Director to a Pattern or Otherwise
    # Must pass a PatternTypes Enum
    def setMode(self, patternMode):

        # If this is a type of Enumeration, then select the correct Pattern Object
        if isinstance(patternMode, PatternTypes):
            pass

        # Return back to ZERO POSITION

        # Then Change Mode

        # Otherwise, throw an exception
        else:
            Exception("The mode provide is not a form of pattern.")

        # Return if execution complete
        return True

    def getCurrentError(self):
        ''' Calculate and return the current error of the ball position'''
        xError = abs(self.BP_x - self.setpoint[0])
        yError = abs(self.BP_y - self.setpoint[1])
        return [xError, yError]

    def getPIDAngles(self):
        ''' Return the servo angles from the PID controller'''
        return [self.P_aX, self.P_aY]

    def setSetposition(self, posX, posY):
        ''' Go to a set position in cms from the center. '''
        """
        # Check X
        if abs(posX) > Director.MAX_X:
            Exception("X Position exceeds maximum.")
            return

        # Check Y
        if abs(posY) > Director.MAX_Y:
            Exception("Y Position exceeds maximum.")
            return
        """
        # Otherwise, update the setpoint
        self.setpoint = [posX, posY]
        self.xAxis.setTarget(posX)
        self.yAxis.setTarget(posY)

    def getSetposition(self):
        ''' Get the current setpoint for the ball. '''
        return self.setpoint

    def holdPlate(self):
        ''' Hold the plate in the current position. '''
        self.augmentation.hold()

    def releasePlate(self):
        ''' Release any active hold acting on the plate and resume control. '''
        self.augmentation.resume()
        self.returnPlateToFlat = False

    def flattenPlate(self):
        ''' Returns the plate to the flat position. '''
        self.augmentation.setNextAngle(0,0)
        self.returnPlateToFlat = True

    def kill(self):
        ''' Destroys the director thread and all child objects. '''
        self.keepRunning = False