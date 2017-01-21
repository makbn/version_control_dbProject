import os
import sys
from PySide.QtUiTools import QUiLoader
from PySide.QtWebKit import QWebView
import MyWidgets
from Database import DatabaseMiddleWare
from ui import MainWidget, NewLogin
from ui import LoginWidget
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtDeclarative import *
from PySide import *

from ui import RegisterPage

PARTITION = 50
image_size = 64

class SplashWidget(QtGui.QWidget):
    WINDOW_WIDTH= 800
    WINDOW_HEIGHT=600

    WINDOW_TITLE="Login"
    WINDOW_FOOTER_MESSAGE="Some Text here for DataBase Project 2016"
    WINDOW_PASSWORD_TITLE="Password :"
    WINDOW_USERNAM_TITLE="Username :"
    WINDOW_PARENT=None
    view=None

    def __init__(self, parent=None):
        super(SplashWidget, self).__init__(parent)
        self.WINDOW_PARENT=parent
        self.layout = QtGui.QHBoxLayout()
        self.addWidgets()

    def complete_name(self):
        frame = self.view.page().mainFrame()
        print (frame.evaluateJavaScript('completeAndReturnName();'))

        # Connect 'complete_name' to the button's 'clicked' signal
        #button.clicked.connect(complete_name)


    def addWidgets(self):

        self.background=MyWidgets.createBackground(self)
        self.loadSplash()
        signup=MyWidgets.createPushButton("SignUp",self,(self.WINDOW_WIDTH/2)-100,self.WINDOW_HEIGHT/2 -30,self.doSignup)
        login=MyWidgets.createPushButton("Sign In",self,(self.WINDOW_WIDTH/2)+10,self.WINDOW_HEIGHT/2 -30,self.doLogin)
        dvider = MyWidgets.createLableColered(self,0,PARTITION*11 +10,self.WINDOW_WIDTH,100,"rgba(29,185,84,255)")
        footer = MyWidgets.createTextLable(self.WINDOW_FOOTER_MESSAGE, self,PARTITION*1, PARTITION*11 +15, "white", "5")
        close=MyWidgets.createBorderLessButton("EXIT",self,710,0,self.WINDOW_PARENT.quit)

    def loadSplash(self):
        self.view = QWebView(self)
        self.view.setMinimumSize(self.WINDOW_WIDTH,PARTITION*11 + 10)
        self.view.setMaximumSize(self.WINDOW_WIDTH,PARTITION*10 + 10)
        cwd = os.getcwd()
        self.view.load(QUrl.fromLocalFile(os.path.join(cwd,"resource","Splash.html")))
        self.WINDOW_PARENT.QApplicationRef.processEvents()

        frame = self.view.page().mainFrame()
        document = frame.documentElement()
        document.findAll(".carousel-caption").at(1).firstChild().setPlainText(self.getUserNumber()+" Registered User!")
        document.findAll(".carousel-caption").at(2).firstChild().setPlainText(self.getRepoNumbers()+" Repositories!")
        self.view.show()

    def getUserNumber(self):
        try:
            return str(DatabaseMiddleWare.getUsersNumber()[0]['count'])
        except:
            return "db Exception"

    def getRepoNumbers(self):
        try:
            return str(DatabaseMiddleWare.getRepoNumber()[0]['count'])
        except:
            return "db Exception"


    def doLogin(self):
        logWidget = NewLogin.NewLoginWidget(self.WINDOW_PARENT)
        NewLogin.BACK_WIDGET="SplashWidget"
        self.WINDOW_PARENT.setCentralWidget(logWidget)

    def doSignup(self):
        signup=RegisterPage.RegisterPage(self.WINDOW_PARENT)
        print(RegisterPage.BACK_WIDGET)
        RegisterPage.BACK_WIDGET="SplashWidget"
        print(RegisterPage.BACK_WIDGET)
        self.WINDOW_PARENT.setCentralWidget(signup)