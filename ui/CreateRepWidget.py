import os
import sys

from PySide.QtWebKit import QWebView, QWebPage

import MyWidgets
import Utils
from PySide.QtCore import *
from PySide import *
from Database import DatabaseMiddleWare

PARTITION = 50
image_size = 64
BACK_WIDGET = None
class CreateRepWidget(QtGui.QWidget):
    WINDOW_WIDTH= 800
    WINDOW_HEIGHT=600

    WINDOW_TITLE="CreateRepository"
    WINDOW_FOOTER_MESSAGE="Some Text here for DataBase Project 2016"
    WINDOW_PASSWORD_TITLE="Password :"
    WINDOW_USERNAM_TITLE="Username :"
    WINDOW_PARENT=None

    def __init__(self, parent=None):
        super(CreateRepWidget, self).__init__(parent)
        self.WINDOW_PARENT=parent
        self.currentUser = Utils.UserManager.getCurrentUser()
        self.layout = QtGui.QHBoxLayout()
        self.addWidgets()

    def loadPage(self):
        self.view = QWebView(self)
        #self.view.webkit.page().userAgentForUrl = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:37.0) Gecko/20100101 Firefox/37.0"
        self.view.linkClicked.connect(self.handleLinkClicked)
        self.page =self.view.page()
        self.view.setMinimumSize(self.WINDOW_WIDTH,PARTITION*11 + 10)
        self.view.setMaximumSize(self.WINDOW_WIDTH,PARTITION*10 + 10)
        self.view.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        cwd = os.getcwd()
        self.view.load(QUrl.fromLocalFile(os.path.join(cwd,"resource","CreateRepository.html")))
        self.WINDOW_PARENT.QApplicationRef.processEvents()
        frame = self.view.page().mainFrame()
        self.document = frame.documentElement()
        doc = self.view.page().mainFrame().documentElement()
        if self.currentUser!=None:
            doc.findAll("#username_field").at(0).setPlainText(str(self.currentUser["username"]) + "/ ")
        else:
            doc.findAll("#username_field").at(0).setPlainText("Username Fetch Error!")
        self.view.show()



    def handleLinkClicked(self, url):
        action=url.toString()
        print(action)
        if action.__contains__("back") :
            self.back()
        elif action.__contains__("createRep"):
            self.createRepository()



    def addWidgets(self):
        self.background=MyWidgets.createBackground(self)
        self.loadPage()
        dvider = MyWidgets.createLableColered(self,0,PARTITION*11 +10,self.WINDOW_WIDTH,100,"rgba(29,185,84,255)")
        footer = MyWidgets.createTextLable(self.WINDOW_FOOTER_MESSAGE, self,PARTITION*1, PARTITION*11 +15, "white", "5")
        close=MyWidgets.createBorderLessButton("EXIT",self,710,0,self.WINDOW_PARENT.quit)
        back=MyWidgets.createBorderLessButton("Back",self,630,0,self.back)

    def back(self):
        import Utils
        back=Utils.UIHelper.backPressHandler(BACK_WIDGET,self.WINDOW_PARENT)
        self.WINDOW_PARENT.setCentralWidget(back)
    def createRepository(self):
        frame = self.view.page().mainFrame()
        document = frame.documentElement()
        name = document.findAll("#getRepName").at(0).toPlainText()
        desc = document.findAll("#getRepDesc").at(0).toPlainText()
        visibility = document.findAll("#getRepVisibility").at(0).toPlainText()
        if visibility=="public":
            visibility=0;
        else:
            visibility=1;
        try:
            user_id=Utils.UserManager.getCurrentUser()["id"]
        except Exception as e:
            print(str(e))
            frame.evaluateJavaScript('show();')

        if len(desc)<1 or len(name)<1:
            frame.evaluateJavaScript('show();')
        else:
            repository=DatabaseMiddleWare.getRepositoryByNameId(name,user_id)

            if repository is not None and repository["owner_id"]==user_id:
                frame.evaluateJavaScript('show();')
            else:
                try:
                    frame.evaluateJavaScript('hide();')
                    DatabaseMiddleWare.createRepository(name,user_id,desc,visibility)
                    self.back()
                except Exception as e:
                    frame.evaluateJavaScript('show();')
                    print("exception=" +str(e))

