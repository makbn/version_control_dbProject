import sys
import MyWidgets
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtDeclarative import *
from PySide import *



class MainWidget(QtGui.QWidget):
    WINDOW_WIDTH= 800
    WINDOW_HEIGHT=600
    WINDOW_TITLE="Main"
    WINDOW_PARENT=None
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.WINDOW_PARENT=parent
        layout = QtGui.QHBoxLayout()
        self.label = QtGui.QLabel('logged in!')
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.addWidgets()

    def addWidgets(self):

        background=MyWidgets.createBackground(self)
        dvider = MyWidgets.createLableColered(self,0,540,self.WINDOW_WIDTH,61,"rgba(104,33,122,255)")

        close=MyWidgets.createBorderLessButton("close",self,710,16,self.WINDOW_PARENT.quit)




