import time

class ImageFrame(object):

    def __init__(self, ballFound, cameraFrame, BP_x, BP_y, pixelX, pixelY, elapsedTime, velocity):
        self.ballFound = ballFound
        self.cameraFrame = cameraFrame
        self.ballX = BP_x
        self.ballY = BP_y
        self.pixelX = pixelX
        self.pixelY = pixelY
        self.elapsedTime = elapsedTime
        self.velocity = velocity
        self.timeStamp = time.time()

    def getCameraFrame(self):
        return self.cameraFrame

    def isBallFound(self):
        return self.isBallFound
    
    def getPixelPosition(self):
        if (self.isBallFound()):
            return self.pixelX, self.pixelY
        else:
            return 0, 0

    def getBallPosition(self):
        if (self.isBallFound()):
            return self.ballX, self.ballY
        else:
            return 0, 0
    
    def getVelocity(self):
        if (self.isBallFound()):
            return self.velocity
        else:
            return 0, 0

    def getTimeStamp(self):
        return self.timeStamp