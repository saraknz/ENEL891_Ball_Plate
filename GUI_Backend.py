from GUIs.BallDetection import BallDetection
import sys
import numpy as np
import cv2 as cv
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from mockup import Ui_MainWindow


class MyGUI(QtWidgets.QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.stackedWidget.setCurrentWidget(self.ui.MainMenu_pg)

        # Main Menu Buttons to navigate to another page
        self.ui.MM_Position_btn.clicked.connect(self.showPositionPage)
        self.ui.MM_Pattern_btn.clicked.connect(self.showPatternPage)
        self.ui.MM_Joystick_btn.clicked.connect(self.showJoystickPage)

        # Menu buttons to return to Main Menu Page
        self.ui.menu_Pos_btn.clicked.connect(self.showMainMenu)
        self.ui.menu_Pattern_btn.clicked.connect(self.showMainMenu)
        self.ui.menu_Joystick_btn.clicked.connect(self.showMainMenu)

        # Position Page Button events setup
        self.ui.Pos_center_btn.clicked.connect(self.PositionCentersetup)
        self.ui.Pos_position_btn.clicked.connect(self.PositionPointsetup)

        # Follow Pattern Page Button events setup
        self.ui.Pattern_Rectangle_btn.clicked.connect(self.PatternRectangleSetup)
        self.ui.Pattern_Circle_btn.clicked.connect(self.PatternCircleSetup)
        self.ui.Pattern_Infinity_btn.clicked.connect(self.PatternInfinitySetup)
        self.ui.Pattern_center_btn.clicked.connect(self.PatternCenterSetup)

        # Joystick Page Button events setup
        self.ui.Joystick_BallCont_btn.clicked.connect(self.JoystickBallSetup)
        self.ui.Joystick_PlateCont_btn.clicked.connect(self.JoystickPlateSetup)

        self.Worker1 = Worker1()
        self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)
        self.Worker1.start()

    def ImageUpdateSlot(self,img):
        piximg = QtGui.QPixmap.fromImage(img)
        self.ui.frames_lbl.setPixmap(piximg)
        # self.ui.frames)lbl.setPixmap(QPixmap.fromImage(img))
        


    def closeEvent(self, event):
        print('Close event fired')
        self.Worker1.Capture.release()  # not checked this
        self.Worker1.stop()
        cv.destroyAllWindows()
        event.accept()


    def showMainMenu(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.MainMenu_pg)  
        self.ui.Pos_center_btn.setStyleSheet(unclickedbtn_stylesheet)  
        self.ui.Pos_position_btn.setStyleSheet(unclickedbtn_stylesheet)
        self.ui.Pattern_Rectangle_btn.setStyleSheet(unclickedbtn_stylesheet)
        self.ui.Pattern_Circle_btn.setStyleSheet(unclickedbtn_stylesheet)
        self.ui.Pattern_Infinity_btn.setStyleSheet(unclickedbtn_stylesheet)
        self.ui.Pattern_center_btn.setStyleSheet(unclickedbtn_stylesheet)
        self.ui.Joystick_BallCont_btn.setStyleSheet(unclickedbtn_stylesheet)
        self.ui.Joystick_PlateCont_btn.setStyleSheet(unclickedbtn_stylesheet)

    def showPositionPage(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.BalancePosition_pg)

    def showPatternPage(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.Pattern_pg)

    def showJoystickPage(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.Joystick_pg)

    def PositionCentersetup(self):
        self.ui.Pos_center_btn.setStyleSheet(clickedbtn_stylesheet)
        self.ui.Pos_position_btn.setStyleSheet(unclickedbtn_stylesheet)
    
    def PositionPointsetup(self):
        self.ui.Pos_center_btn.setStyleSheet(unclickedbtn_stylesheet)
        self.ui.Pos_position_btn.setStyleSheet(clickedbtn_stylesheet)

    def PatternRectangleSetup(self):
        self.ui.Pattern_Rectangle_btn.setStyleSheet(clickedbtn_stylesheet)
        self.ui.Pattern_Circle_btn.setStyleSheet(unclickedbtn_stylesheet)
        self.ui.Pattern_Infinity_btn.setStyleSheet(unclickedbtn_stylesheet)
        self.ui.Pattern_center_btn.setStyleSheet(unclickedbtn_stylesheet)

    def PatternCircleSetup(self):
        self.ui.Pattern_Rectangle_btn.setStyleSheet(unclickedbtn_stylesheet)
        self.ui.Pattern_Circle_btn.setStyleSheet(clickedbtn_stylesheet)
        self.ui.Pattern_Infinity_btn.setStyleSheet(unclickedbtn_stylesheet)
        self.ui.Pattern_center_btn.setStyleSheet(unclickedbtn_stylesheet)

    def PatternInfinitySetup(self):
        self.ui.Pattern_Rectangle_btn.setStyleSheet(unclickedbtn_stylesheet)
        self.ui.Pattern_Circle_btn.setStyleSheet(unclickedbtn_stylesheet)
        self.ui.Pattern_Infinity_btn.setStyleSheet(clickedbtn_stylesheet)
        self.ui.Pattern_center_btn.setStyleSheet(unclickedbtn_stylesheet)

    def PatternCenterSetup(self):
        self.ui.Pattern_Rectangle_btn.setStyleSheet(unclickedbtn_stylesheet)
        self.ui.Pattern_Circle_btn.setStyleSheet(unclickedbtn_stylesheet)
        self.ui.Pattern_Infinity_btn.setStyleSheet(unclickedbtn_stylesheet)
        self.ui.Pattern_center_btn.setStyleSheet(clickedbtn_stylesheet)

    def JoystickBallSetup(self):
        self.ui.Joystick_BallCont_btn.setStyleSheet(clickedbtn_stylesheet)
        self.ui.Joystick_PlateCont_btn.setStyleSheet(unclickedbtn_stylesheet)

    def JoystickPlateSetup(self):
        self.ui.Joystick_BallCont_btn.setStyleSheet(unclickedbtn_stylesheet)
        self.ui.Joystick_PlateCont_btn.setStyleSheet(clickedbtn_stylesheet)




unclickedbtn_stylesheet = """
QPushButton {
border-width: 2px;
border-color: rgb(103, 103, 103);
border-style: outset;
border-radius: 7;
padding: 3px;
background-color: rgb(250, 250, 250);
}

"""     
        
clickedbtn_stylesheet = """
QPushButton{
border-width: 2px;
border-color: rgb(103, 103, 103);
border-style: inset;
border-radius: 7;
padding: 3px;
background-color: rgb(165, 244, 121);
}
"""

class Worker1(QtCore.QThread):
    ImageUpdate = QtCore.pyqtSignal(QtGui.QImage)
    def run(self):
        self.ThreadActive = True
        self.Capture = cv.VideoCapture(0)
        while self.ThreadActive:
            ret, frame = self.Capture.read()
            if ret:
                img = cv.cvtColor(frame, cv.COLOR_BGR2RGB)  
                img = QtGui.QImage(img, img.shape[1], img.shape[0], QtGui.QImage.Format_RGB888)
                self.ImageUpdate.emit(img)

    def stop(self):
        self.ThreadActive = False
        self.quit()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_win = MyGUI()
    main_win.show()
    sys.exit(app.exec_())