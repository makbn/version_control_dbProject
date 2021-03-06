import os
import sys

from PySide.QtWebKit import QWebView, QWebPage

import MyWidgets
import Utils
from ui import MainWidget
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtDeclarative import *
from PySide import *
from Database import DatabaseMiddleWare

PARTITION = 50
image_size = 64
BACK_WIDGET = None
class CrtRepositoryPage(QtGui.QWidget):
    WINDOW_WIDTH= 800
    WINDOW_HEIGHT=600
    WINDOW_TITLE="Login"
    WINDOW_FOOTER_MESSAGE="Some Text here for DataBase Project 2016"
    WINDOW_PASSWORD_TITLE="Password :"
    WINDOW_USERNAM_TITLE="Username :"
    WINDOW_PARENT=None

    def __init__(self,parent=None):
        super(CrtRepositoryPage, self).__init__(parent)
        self.WINDOW_PARENT=parent
        self.layout = QtGui.QHBoxLayout()
        self.addWidgets()

    def loadSplash(self):
        self.view = QWebView(self)
        #self.view.webkit.page().userAgentForUrl = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:37.0) Gecko/20100101 Firefox/37.0"
        self.view.linkClicked.connect(self.handleLinkClicked)
        self.page =self.view.page()
        self.view.setMinimumSize(self.WINDOW_WIDTH,PARTITION*11 + 10)
        self.view.setMaximumSize(self.WINDOW_WIDTH,PARTITION*10 + 10)
        self.view.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        cwd = os.getcwd()
        self.view.load(QUrl.fromLocalFile(os.path.join(cwd,"resource","AddRepoPage.html")))
        self.WINDOW_PARENT.QApplicationRef.processEvents()
        print(self.view.page().mainFrame().toHtml())

        frame = self.view.page().mainFrame()
        document = frame.documentElement()
        self.view.show()

    def addWidgets(self):
        self.background=MyWidgets.createBackground(self)
        self.loadSplash()
        dvider = MyWidgets.createLableColered(self,0,PARTITION*11 +10,self.WINDOW_WIDTH,100,"rgba(29,185,84,255)")
        footer = MyWidgets.createTextLable(self.WINDOW_FOOTER_MESSAGE, self,PARTITION*1, PARTITION*11 +15, "white", "5")
        close=MyWidgets.createBorderLessButton("EXIT",self,710,0,self.WINDOW_PARENT.quit)
        close=MyWidgets.createBorderLessButton("BACK",self,630,0,self.back)

    def handleLinkClicked(self, url):
        action=url.toString()
        if(action.__contains__("doRegister")):
            self.signup()
        elif(action.__contains__("doLogin")):
            self.login()
        else:
            self.recoverPassword()

    def signup(self):
        #DatabaseMiddleWare.initialize()
        frame = self.view.page().mainFrame()
        document = frame.documentElement()
        email = document.findAll("#getEmail").at(0).toPlainText()
        password = document.findAll("#getPassword").at(0).toPlainText()
        username = document.findAll("#getUsername").at(0).toPlainText()
        firstname = document.findAll("#getFirstname").at(0).toPlainText()
        lastname = document.findAll("#getLastname").at(0).toPlainText()
        date = document.findAll("#getDate").at(0).toPlainText()
        Gender = document.findAll("#getGender").at(0).toPlainText()

        user = {
            "email": email,
            "password": password,
            "username": username,
            "firstname": firstname,
            "lastname": lastname,
            "birthdate": date,
            "gender": 1 if Gender == "Male" else 0
        }
        found = DatabaseMiddleWare.fetchUser(username)
        if(found != None) :
            print("username Already exists")
        else:
            DatabaseMiddleWare.register(user)
            print("register")

    def back(self):
        back=Utils.UIHelper.backPressHandler(BACK_WIDGET,self.WINDOW_PARENT)
        self.WINDOW_PARENT.setCentralWidget(back)