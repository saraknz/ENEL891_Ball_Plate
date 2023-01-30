from PyQt5 import QtCore as qtc
from queue import Queue


class FrameCollector(qtc.QObject):

    imageUpdate = qtc.pyqtSignal()

    def __init__(self):
        qtc.QObject.__init__(self)
        self.frameQueue = Queue()

    def addFrame(self, frameToAdd):
        self.frameQueue.put(frameToAdd)
        self.imageUpdate.emit()
        print("Frame Collected")

    def getFrame(self):
        # Review the current number of items in the queue
        queueSize = self.frameQueue.qsize()

        # If no items exist, reuturn null
        if (queueSize == 0):
            return None

        elif (queueSize == 1):
            return self.frameQueue.get_nowait()
            
        else:
            while(self.frameQueue.qsize() > 1):
                self.frameQueue.get_nowait()
            return self.frameQueue.get_nowait()

