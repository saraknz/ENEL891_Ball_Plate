import math

class Pattern(object):

    # Constants
    DEADZONE_TOLLERANCE = 0.005        # Acceptable Error around the target position

    # Create new Pattern Object, with a list of 2D Coordinates (Positions), and set the current Position to Zero
    def __init__(self, pattern):
        self.positions = pattern
        self.currentPosition = 0
        self.numOfPositions = len(pattern)
        return

    # Takes the current position from the calling method, and determines the next suitable position
    def getNextPosition(self, plateX, plateY):
        
        # Get current positions
        currentX = self.pattern[self.currentPosition][0]
        currentY = self.pattern[self.currentPosition][1]

        # Compare to deadzone tollerance
        displacementX = currentX - plateX
        displacementY = currentY - plateY
        displacement2D = math.sqrt(displacementX ^ 2 + displacementY ^ 2)

        # If in suitable position, move and return next position
        # Otherwise, return current position
        goToNextPos = True
        if (abs(displacementX)) > Pattern.DEADZONE_TOLLERANCE:
            goToNextPos = False
        if (abs(displacementX)) > Pattern.DEADZONE_TOLLERANCE:
            goToNextPos = False

        if (goToNextPos):

            # Add delay of n frames
            # TODO

            # Go to next position
            self.currentPosition += 1
            if (self.numOfPositions < self.currentPosition):
                self.currentPosition = 0

        return self.pattern[self.currentPosition][0], self.pattern[self.currentPosition][1]