
import numpy as np
import cv2 as cv

## Webcam capture and setting

def nothing(x):
    pass

# To adjust HSV values and find Pixel Metric
cap = cv.VideoCapture(0)
camWidth = cap.get(3)
camHeight = cap.get(4)
cap.set(10,50)
fps = cap.get(cv.CAP_PROP_FPS) 
camWidth = int(camWidth)
camHeight = int(camHeight)
midWidth = camWidth//2
midHeight = camHeight//2
pxMetric = 7.8
cv.namedWindow('Trackbars')
cv.createTrackbar('H_Low', 'Trackbars', 0, 179,nothing)
cv.createTrackbar('H_Upper', 'Trackbars', 0, 179,nothing)
cv.createTrackbar('S_Low', 'Trackbars', 0, 255,nothing)
cv.createTrackbar('S_Upper', 'Trackbars', 0, 255,nothing)
cv.createTrackbar('V_Low', 'Trackbars', 0, 255,nothing)
cv.createTrackbar('V_Upper', 'Trackbars', 0, 255,nothing)
    
while True:
    ret, frame = cap.read()
    HL = cv.getTrackbarPos('H_Low', 'Trackbars')
    SL = cv.getTrackbarPos('S_Low', 'Trackbars')
    VL = cv.getTrackbarPos('V_Low', 'Trackbars')
    HU = cv.getTrackbarPos('H_Upper', 'Trackbars')
    SU = cv.getTrackbarPos('S_Upper', 'Trackbars')
    VU = cv.getTrackbarPos('V_Upper', 'Trackbars')
    lowOrange = np.array([ HL, SL, VL])
    uppOrange = np.array([ HU, SU, VU])
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv, lowOrange, uppOrange)
    #kernel = np.ones((5,5),np.uint8)
    #opening = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    #closing = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)
    circFind, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    for contour in circFind:
        circArea = cv.contourArea(contour)
        #print(circArea)
        if circArea > 1000:
            x, y, w, h = cv.boundingRect(contour)
            ball_x = (w//2 + x)
            ball_y = (h//2 + y)
            BP_x = ball_x - midWidth                              
            BP_y = midHeight - ball_y
            BP_x = (BP_x / pxMetric) / 100
            BP_y = (BP_y / pxMetric) / 100    
            cv.circle(frame, (ball_x, ball_y), 30, (255, 0, 255), 2)
            cv.circle(frame, (ball_x, ball_y), 3, (255, 0, 255), -1)
            print("Ball Position : {} , {} ".format(BP_x, BP_y))
    
    # Print x,y grid and centre
    cv.line(frame, (midWidth,0), (midWidth,camHeight), (0,255,0), 1)  # Green colour
    cv.line(frame, (0,midHeight), (camWidth,midHeight), (0,255,0), 1) # Green colour
    cv.circle(frame, (midWidth,midHeight), 6, (0,0,255), 2)  # Red colour

    
    cv.imshow("Frame", frame)
    cv.imshow("Mask", mask)
    #cv.imshow("Open", opening)
    #cv.imshow("Close", closing)
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
    
#print("Low Orange = ", lowOrange)
#print("Upper Orange = ", uppOrange)
#print("MidWidth = ", midWidth)
#print("MidHeight = ", midHeight)
