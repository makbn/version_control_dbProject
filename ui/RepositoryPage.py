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
class RepositoryPage(QtGui.QWidget):
    WINDOW_WIDTH= 800
    WINDOW_HEIGHT=600
    WINDOW_TITLE="Login"
    WINDOW_FOOTER_MESSAGE="Some Text here for DataBase Project 2016"
    WINDOW_PASSWORD_TITLE="Password :"
    WINDOW_USERNAM_TITLE="Username :"
    WINDOW_PARENT=None
    repositoryName = ""
    repositoryId = ""

    def __init__(self,parent=None , repositoryId=None , repositoryName=None):
        super(RepositoryPage, self).__init__(parent)
        self.WINDOW_PARENT=parent
        self.layout = QtGui.QHBoxLayout()
        self.repositoryId = repositoryId
        self.repositoryName = repositoryName
        print(self.repositoryName)
        self.addWidgets()


    def loadSplash(self):
        self.view = QWebView(self)
        self.view.linkClicked.connect(self.handleLinkClicked)
        self.page =self.view.page()
        self.view.setMinimumSize(self.WINDOW_WIDTH,PARTITION*11 + 10)
        self.view.setMaximumSize(self.WINDOW_WIDTH,PARTITION*10 + 10)
        self.view.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        cwd = os.getcwd()
        self.view.load(QUrl.fromLocalFile(os.path.join(cwd,"resource","RepositoryPage.html")))
        self.WINDOW_PARENT.QApplicationRef.processEvents()
        frame = self.view.page().mainFrame()

        document = frame.documentElement()
        print(frame.toHtml())
        self.view.show()


    def fillTheDocument(self , document=None):
        if document == None :
            print("None doc")
            return
        else :
            print("fsdafdasf " + self.repositoryName)
            print(document.findAll("#RepositoryName").count())
            document.findAll("#RepositoryName").at(0).setInnerXml(self.repositoryName)

    def searchForIssue(self , repositoryName):
        pass

    def Repository(self , repositoryName):
        pass


    def addWidgets(self):
        self.background=MyWidgets.createBackground(self)
        self.loadSplash()
        dvider = MyWidgets.createLableColered(self,0,PARTITION*11 +10,self.WINDOW_WIDTH,100,"rgba(29,185,84,255)")
        footer = MyWidgets.createTextLable(self.WINDOW_FOOTER_MESSAGE, self,PARTITION*1, PARTITION*11 +15, "white", "5")
        close=MyWidgets.createBorderLessButton("EXIT",self,710,0,self.WINDOW_PARENT.quit)
        close=MyWidgets.createBorderLessButton("BACK",self,630,0,self.back)

    def handleLinkClicked(self, url):
        action=url.toString()
        if(action.__contains__("doFork")):
            self.fork()
        elif(action.__contains__("doLike")):
            self.like()

    def fork(self):
        print("Forked")

    def like(self):
        print("liked")


    def back(self):
        back=Utils.UIHelper.backPressHandler(BACK_WIDGET,self.WINDOW_PARENT)
        self.WINDOW_PARENT.setCentralWidget(back)