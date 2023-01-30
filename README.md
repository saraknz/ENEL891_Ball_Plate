# ENEL891_Ball_Plate
Industrial Final Year Project - Ball Plate Balancing System

This project was undertaken for ENEL891 Industrial Project.
Myself and my colleague worked together to complete this project.

Ball Plate Balancing Project was broken into two main parts:
Hardware and Software.
My colleague completed the work for the Hardware aspects, while I completed the System modelling and Software aspects.

Ball Plate Systems:
The two degree of freedom (DOF) ball-plate model consists of a plate that can be tilted up
and down along two perpendicular directions by two servo motors, one servo on each axis (x,
y). The aim of ball balancing systems is to control the movement of the ball, getting it to a set
point or to follow a path. Control over the ball is achieved only indirectly, by moving the
servo’s, which causes the plate tilt which in turn, rolls the ball.
A sensor reads the position of the ball.  We used a camera as the sensor, a PID controller to get the required angle of the plate.   A Ras[berry Pi was used to run the camera, the main code and to send the outputed angle of the servos to an FPGA, which drove the servos.



System Modelling:
Mathematical model of the system and deriving the transfer functions.

Software:
Use image processing to detect the ball within the frame
Develop and apply a PID controller
Designe and create GUI to be used on the touch screen to offer modes of intereact to the user
Design and write the software

![image](https://user-images.githubusercontent.com/69064718/215402260-7c685c60-9b28-4a00-a38e-b27dd23cdd86.png)

The Control script initiates the Director and runs the graphical user interface. When the
Director object is initiated, it starts the Image Processor, PID controller and SPAS and controls
the flow of information.
The Image Processor class activates the camera and fetches each frame and applies a ball
detection method to find the ball within the frame and determine its position. If a ball was
found, the Director passes the ball’s position to the PID controller.
The PID controller class takes the ball’s position and desired set point to calculate the error
which is used in the calculations of the P, and D components. Each servo is treated as
independent, so the x co-ordinate and y co-ordinate are each sent through different instances
of the PID controller, to give an output value for each servo.
When the output angle is returned, the Director sends it to SPAS. This is the servo plate
augmentation system. It was made to apply limits and checks on the output from the PID,
before it is sent to the servo motors. SPAS then calls the UART class. This class converts the
angle into binary and writes it to the UART TX to send the data to the FPGA
