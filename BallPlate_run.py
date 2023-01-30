

import sys
import numpy as np
import cv2 as cv
from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from Director import Director
from BallPlateGUI import Ui_MainWindow
from FrameCollector import FrameCollector

class ballgui(qtw.QMainWindow):
    xpos_counter = 0
    ypos_counter = 0

    def __init__(self, director, frameCollector, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.stackedWidget.setCurrentWidget(self.ui.main_pg)
        self.director = director
        self.frameCollector = frameCollector
        self.pos_setpoint = False
        self.drawRect = False
        self.drawCirc = False

        # Link director to GUI
        self.frameCollector.imageUpdate.connect(self.ImageUpdateSlot)
        
        # Main Menu btns to navigate to another page
        self.ui.btn_main_position.clicked.connect(self.showPosition_pg)
        self.ui.btn_main_pattern.clicked.connect(self.showPattern_pg)
        self.ui.btn_main_joystick.clicked.connect(self.showJoystick_pg)

        # Menu buttons on each page, to return to Main Menu
        self.ui.btn_pos_menu.clicked.connect(self.showMain_pg)
        self.ui.btn_patt_menu.clicked.connect(self.showMain_pg)
        self.ui.btn_joystick_menu.clicked.connect(self.showMain_pg)

        # Position page btn event set up
        self.ui.btn_pos_center.clicked.connect(self.setup_posCenter)
        self.ui.btn_pos_position.clicked.connect(self.setup_posPoint)
        self.ui.btn_pos_reset.clicked.connect(self.setup_posReset)
        self.ui.btn_pos_xplus.clicked.connect(self.Xplus)
        self.ui.btn_pos_xminus.clicked.connect(self.Xminus)
        self.ui.btn_pos_yplus.clicked.connect(self.Yplus)
        self.ui.btn_pos_yminus.clicked.connect(self.Yminus)

        # Patterns page btn event set up
        self.ui.btn_patt_rectangle.clicked.connect(self.setup_pattRectangle)
        self.ui.btn_patt_circle.clicked.connect(self.setup_pattCircle)
        self.ui.btn_patt_infinity.clicked.connect(self.setup_pattInfinity)
        self.ui.btn_patt_center.clicked.connect(self.setup_pattCenter)
        self.ui.btn_patt_reset.clicked.connect(self.setup_pattReset)

        # Joystick page btn event set up

    # CloseEvent known by gui, will perform instructions prior to closing
    def closeEvent(self, event):
        print('Close event fired')
        self.director.kill()
        event.accept()
    
    def showMain_pg(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.main_pg)  
        
    def showPosition_pg(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.position_pg)
        self.ui.btn_pos_center.setStyleSheet(neutralbtn)
        self.ui.btn_pos_position.setStyleSheet(neutralbtn)
        self.ui.lbl_pos_showxpos.setText(str(self.xpos_counter))
        self.ui.lbl_pos_showypos.setText(str(self.ypos_counter))
        
        
    def showPattern_pg(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.pattern_pg)
        self.ui.btn_patt_rectangle.setStyleSheet(neutralbtn)
        self.ui.btn_patt_circle.setStyleSheet(neutralbtn)
        self.ui.btn_patt_infinity.setStyleSheet(neutralbtn)
        self.ui.btn_patt_center.setStyleSheet(neutralbtn)

    def showJoystick_pg(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.joystick_pg)
        self.ui.btn_stick_position.setStyleSheet(neutralbtn)
        self.ui.btn_stick_angle.setStyleSheet(neutralbtn)

    def setup_posCenter(self):
        self.ui.btn_pos_center.setStyleSheet(clickedbtn)
        self.ui.btn_pos_position.setStyleSheet(neutralbtn)
        self.ui.btn_pos_menu.setEnabled(False)
        self.ui.btn_pos_menu.setStyleSheet(disablebtn)
        self.pos_setpoint = False

    def setup_posPoint(self):
        self.ui.btn_pos_position.setStyleSheet(clickedbtn)
        self.ui.btn_pos_center.setStyleSheet(neutralbtn)
        self.ui.btn_pos_menu.setEnabled(False)
        self.ui.btn_pos_menu.setStyleSheet(disablebtn)
        self.pos_setpoint = True
        self.xpos_counter = 0
        self.ypos_counter = 0

    def setup_posReset(self):
        self.ui.btn_pos_menu.setEnabled(True)
        self.ui.btn_pos_menu.setStyleSheet(whitebtn)
        self.ui.btn_pos_center.setStyleSheet(neutralbtn)
        self.ui.btn_pos_position.setStyleSheet(neutralbtn)
        self.xpos_counter = 0
        self.ypos_counter = 0
        self.ui.lbl_pos_showxpos.setText(str(self.xpos_counter))
        self.ui.lbl_pos_showypos.setText(str(self.ypos_counter))
        self.director.setSetposition(0,0)
        self.pos_setpoint = False


    def Xplus(self):
        self.xpos_counter += 2  # 2cm steps
        if self.xpos_counter >= 25:
            self.xpos_counter = 24
        self.ui.lbl_pos_showxpos.setText(str(self.xpos_counter))
        self.showX_SP = (self.xpos_counter / 100)
        self.showY_SP = (self.ypos_counter / 100)
        self.director.setSetposition(self.showX_SP, self.showY_SP)
        
    def Xminus(self):
        self.xpos_counter -= 2  # 2cm steps
        if self.xpos_counter <= -25:
            self.xpos_counter = -24
        self.ui.lbl_pos_showxpos.setText(str(self.xpos_counter))
        self.showX_SP = (self.xpos_counter / 100)
        self.showY_SP = (self.ypos_counter / 100)
        self.director.setSetposition(self.showX_SP, self.showY_SP)
        
    def Yplus(self):
        self.ypos_counter += 2  # 2cm steps
        if self.ypos_counter >= 15:
            self.ypos_counter = 14
        self.ui.lbl_pos_showypos.setText(str(self.ypos_counter))
        self.showX_SP = (self.xpos_counter / 100)
        self.showY_SP = (self.ypos_counter / 100)
        self.director.setSetposition(self.showX_SP, self.showY_SP)
        
    def Yminus(self):
        self.ypos_counter -= 2  # 2cm steps
        if self.ypos_counter <= -15:
            self.ypos_counter = -14
        self.ui.lbl_pos_showypos.setText(str(self.ypos_counter))
        self.showX_SP = (self.xpos_counter / 100)
        self.showY_SP = (self.ypos_counter / 100)
        self.director.setSetposition(self.showX_SP, self.showY_SP)
        
    def setup_pattRectangle(self):
        self.ui.btn_patt_rectangle.setStyleSheet(clickedbtn)
        self.ui.btn_patt_circle.setStyleSheet(neutralbtn)
        self.ui.btn_patt_infinity.setStyleSheet(neutralbtn)
        self.ui.btn_patt_center.setStyleSheet(neutralbtn)
        self.ui.btn_patt_menu.setEnabled(False)
        self.ui.btn_patt_menu.setStyleSheet(disablebtn)
        self.drawRect = True
        self.drawCirc = False

    def setup_pattCircle(self):
        self.ui.btn_patt_circle.setStyleSheet(clickedbtn)
        self.ui.btn_patt_rectangle.setStyleSheet(neutralbtn)
        self.ui.btn_patt_infinity.setStyleSheet(neutralbtn)
        self.ui.btn_patt_center.setStyleSheet(neutralbtn)
        self.ui.btn_patt_menu.setEnabled(False)
        self.ui.btn_patt_menu.setStyleSheet(disablebtn)
        self.drawCirc = True
        self.drawRect = False

    def setup_pattInfinity(self):
        self.ui.btn_patt_infinity.setStyleSheet(clickedbtn)
        self.ui.btn_patt_rectangle.setStyleSheet(neutralbtn)
        self.ui.btn_patt_circle.setStyleSheet(neutralbtn)
        self.ui.btn_patt_center.setStyleSheet(neutralbtn)
        self.ui.btn_patt_menu.setEnabled(False)
        self.ui.btn_patt_menu.setStyleSheet(disablebtn)

    def setup_pattCenter(self):
        self.ui.btn_patt_center.setStyleSheet(clickedbtn)
        self.ui.btn_patt_rectangle.setStyleSheet(neutralbtn)
        self.ui.btn_patt_circle.setStyleSheet(neutralbtn)
        self.ui.btn_patt_infinity.setStyleSheet(neutralbtn)
        self.ui.btn_patt_menu.setEnabled(False)
        self.ui.btn_patt_menu.setStyleSheet(disablebtn)
    
    def setup_pattReset(self):
        self.ui.btn_patt_menu.setEnabled(True)
        self.ui.btn_patt_menu.setStyleSheet(whitebtn)
        self.ui.btn_patt_rectangle.setStyleSheet(neutralbtn)
        self.ui.btn_patt_circle.setStyleSheet(neutralbtn)
        self.ui.btn_patt_infinity.setStyleSheet(neutralbtn)
        self.ui.btn_patt_center.setStyleSheet(neutralbtn)
        self.drawCirc = False
        self.drawRect = False

    def ImageUpdateSlot(self):
        # cant access at same time as director img queque 
        # director will make a separate queque and pass on img object to it, 
        # after director queque is done with it.
        print("Yay Signal here")
        imageFrame = self.frameCollector.getFrame()

        # Ignore if none
        if imageFrame is None:
            return

        # Get the image
        image = imageFrame.getCameraFrame()
        self.displayFrame(image, imageFrame)
        
    # Frame is type of ImageFrame
    def displayFrame(self, img, imageFrame):
        ## Need to draw some stuff on the frame before display
        ballFound = imageFrame.isBallFound()
        
        # The following will always been drawn on frame
        cv.line(img, (320,0), (320,480), (0,255,0), 1)  # Green colour
        cv.line(img, (0,240), (640,240), (0,255,0), 1) # Green colour
        cv.circle(img, (320,240), 6, (0,0,255), 2)  # Red colour

        if self.pos_setpoint == True:
            self.showX = int((self.xpos_counter * 7.6) + 320)
            self.showY = int(240 - (self.ypos_counter * 7.6))
            cv.circle(img, (self.showX, self.showY), 7, (0,255,255), -1)  # Red colour

        if self.drawCirc == True:
            cv.circle(img, (320, 240), 100, (0,255,255), 2)
        
        if self.drawRect == True:
            cv.rectangle(img, (320-100, 240-85), (320+100,240+85), (0,255,255), 2)

        if ballFound:
            pixelX, pixelY = imageFrame.getPixelPosition()
            ballX, ballY = imageFrame.getBallPosition()
            cv.circle(img, (int(pixelX), int(pixelY)), 30, (230, 38, 0), 2)
            cv.circle(img, (int(pixelX), int(pixelY)), 3, (230, 38, 0), -1)
            ballX = round((ballX * 100),2) # Ball X from meters into cm
            ballY = round((ballY * 100),2) # Ball Y from meters into cm
            PAX, PAY = self.director.getPIDAngles()
            xError, yError = self.director.getCurrentError()
            xError = round((xError * 100), 2)
            yError = round((yError * 100), 2)
            PAX = round(PAX, 2)
            PAY = round(PAY, 2)
            self.ui.lbl_ballStats.setText("Ball X: {} cm.  X Error: {}.  PID output X: {}.  \nBall Y: {} cm.   Y Error: {}.  PID output Y: {} ".format(ballX, xError, PAX, ballY, yError, PAY))
            
        # To resize the image to fit into label area
        # This must be the last alteration to the image
        # All things drawn on image must be doen prior
        (h, w, c) = img.shape
        scale = 1.3
        width = int(w / scale)
        height = int(h / scale)
        dim = (width, height)
        image = cv.resize(img, dim, interpolation=cv.INTER_AREA)
        # Convert image (np.ndarray) into format for PyQt5 for display
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        image = qtg.QImage(image, image.shape[1], image.shape[0], qtg.QImage.Format_RGB888) # format as QImage
        image = qtg.QPixmap.fromImage(image) # convert to QPixmap
        self.ui.lbl_frames.setPixmap(image)   
        


neutralbtn = """ 
QPushButton {
border-width: 2px;
border-style: outset;
border-radius: 7;
padding: 3px;
border-color: #0c1b33;
background-color: rgb(189, 213, 234);
color: #0c1b33;
}
"""
clickedbtn = """
QPushButton {
border-width: 2px;
border-style: outset;
border-radius: 7;
padding: 3px;
border-color: #0c1b33;
background-color: rgb(79, 178, 134);
color: #0c1b33;
}
"""
disablebtn = """
QPushButton {
border-width: 2px;
border-color: rgb(179, 179, 179);
border-style: solid;
border-radius: 7;
padding: 3px;
background-color: #fbfbff;
}
"""
whitebtn = """
QPushButton {
border-width: 2px;
border-style: solid;
border-radius: 7;
padding: 3px;
color: rgb(12, 27, 51);
border-color: rgb(12, 27, 51);
background-color: rgb(251, 251, 255);
}
"""

if __name__ == '__main__':
    frameCollectorObj = FrameCollector()
    directorObj = Director(0, 'COM2', frameCollectorObj, False)
    directorObj.start()
    app = qtw.QApplication(sys.argv)
    main_win = ballgui(directorObj, frameCollectorObj)
    main_win.show()
    sys.exit(app.exec_())