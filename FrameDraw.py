import cv2 as cv



class FrameDraw:
    midWidth = 320
    midHeight = 240
    viewWidth = 640
    viewHeight = 480
    # Get frame from ...

    def baseGrid(self, frame):
    # Whether Ball or not, will draw the below.
    # Print x,y grid (green) and centre point (red)
        cv.line(frame, (FrameDraw.midWidth,0), (FrameDraw.midWidth, FrameDraw.viewHeight), (0,255,0), 1)  # Green colour
        cv.line(frame, (0, FrameDraw.midHeight), (FrameDraw.viewWidth, FrameDraw.midHeight), (0,255,0), 1) # Green colour
        cv.circle(frame, (FrameDraw.midWidth, FrameDraw.midHeight), 6, (0,0,255), 2)  # Red colour   

        return frame

    def drawBall(self):
        
    # Draw circle and center of detected ball
        cv.circle(frame, (ball_x, ball_y), 30, (255, 0, 255), 2)
        cv.circle(frame, (ball_x, ball_y), 3, (255, 0, 255), -1)   # Color currently magneta
    ## Note : ball_x and ball_y are pixel values 

    # Could also print target setpoint of ball
    # Need to know the fed "Set Point"
    cv.circle(frame, (target_x, target_y), 6, (0,0,255), 2) 

    def frame4Display(self):
        # if no ball,
        # Frame = baseGrid

        # if ball detected,
        # frame = baseGrid
        # frame = drawBall

        # Could also just switch between the two on a True or False value, and
        # have the BaseGrid options under drawBall aswell.

         if ballFound:
            frame = self.drawBall(frame)
            return FrameDraw