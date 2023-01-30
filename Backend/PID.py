import time

class PID:

    # Constants
    TIMESTEP = 1/30         # Equals 1/FPS
    MAX_UI = 9.5            # Integrator anti-windup limiter
    DEADZONE = 0.005        # Acceptable Error around the target position

    def __init__(self,KP,KI,KD,target,enableVerbose):
        self.kp = KP
        self.ki = KI
        self.kd = KD
        self.setTarget(target)
        self.error = 0
        self.last_error = 0
        self.last_time = time.time()
        self.integral_error = 0
        self.derivative_error = 0
        self.output = 0
        self.enableVerbose = 0

    def __calculateError__(self, pos):
        ''' Compute the error between the current and target ball position with Dead Zone considerations. '''

        # Calculate the current error of the ball position
        calculatedError = self.setpoint - pos

        # If ball is considered within the deadzone, set error to zero
        if abs(calculatedError) <= PID.DEADZONE:
            calculatedError = 0

        return calculatedError

    def setTarget(self, target):
        ''' Set the Target Ball position on the given axis in meters. '''
        self.setpoint = target

    def compute(self, currPos, currTime):
        
        ''' 
        Determines the required response angle for the servo plate based on the current ball position. 
        currPos - Current Ball Position
        currTime - Current System Time
        Both pieces of information should correspond to the same frame from a ImageFrame object.
        '''

        # Calculate the current error of the ball position
        # If there is no error, then return 0 error
        self.error = self.__calculateError__(currPos)
        if self.enableVerbose:
            print("Position Displ. : {}".format(self.error))
        if self.error == 0:
            newOutput = 0

        # Otherwise, use the controller to calculate the PID and set the angle.

        # Determine elapsed time
        # TODO Deal with first frame
        elapsedTime = currTime - self.last_time
        self.last_time = currTime

        # Calculate the P, I, D Components
        self.integral_error += self.error * elapsedTime
        self.derivative_error = (self.error - self.last_error) / elapsedTime
        self.last_error = self.error
        
        # Anti-Windup for the Integrator
        if self.integral_error > PID.MAX_UI:
            self.integral_error = PID.MAX_UI
        
        # Determines the appropriate output angle based on the current error
        #newOutput = (self.kp*self.error)
        #newOutput = (self.kd*self.derivative_error)
        newOutput = (self.kp*self.error) + (self.kd*self.derivative_error)
        # newOutput = (self.kp*self.error) + (self.ki*self.integral_error) + (self.kd*self.derivative_error)

        # Verbose
        if self.enableVerbose:
            print("P, I, D : {}, {}, {}".format(self.kp*self.error, self.integral_error*self.ki, self.derivative_error*self.kd))

        # Return the angle
        self.output = newOutput
        return self.output