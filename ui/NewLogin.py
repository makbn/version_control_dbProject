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
from ui.DashbordWidget import DashboardWidget

PARTITION = 50
image_size = 64
BACK_WIDGET=None
class NewLoginWidget(QtGui.QWidget):
    WINDOW_WIDTH= 800
    WINDOW_HEIGHT=600
    WINDOW_TITLE="Login"
    WINDOW_FOOTER_MESSAGE="Some Text here for DataBase Project 2016"
    WINDOW_PASSWORD_TITLE="Password :"
    WINDOW_USERNAM_TITLE="Username :"
    WINDOW_PARENT=None
    currentUser = None

    def __init__(self, parent=None):
        super(NewLoginWidget, self).__init__(parent)
        self.WINDOW_PARENT=parent
        self.layout = QtGui.QHBoxLayout()
        self.addWidgets()

    def loadSplash(self):
        self.view = QWebView(self)
        self.view.linkClicked.connect(self.handleLinkClicked)
        self.page =self.view.page();
        self.view.setMinimumSize(self.WINDOW_WIDTH,PARTITION*11 + 10)
        self.view.setMaximumSize(self.WINDOW_WIDTH,PARTITION*10 + 10)
        self.view.page().setLinkDelegationPolicy(
        QtWebKit.QWebPage.DelegateAllLinks)
        cwd = os.getcwd()
        self.view.load(QUrl.fromLocalFile(os.path.join(cwd,"resource","LoginForm.html")))
        self.WINDOW_PARENT.QApplicationRef.processEvents()
        self.view.show()

    def addWidgets(self):
        self.background=MyWidgets.createBackground(self)
        self.loadSplash()

        dvider = MyWidgets.createLableColered(self,0,PARTITION*11 +10,self.WINDOW_WIDTH,100,"rgba(29,185,84,255)")
        footer = MyWidgets.createTextLable(self.WINDOW_FOOTER_MESSAGE, self,PARTITION*1, PARTITION*11 +15, "white", "5")
        close=MyWidgets.createBorderLessButton("EXIT",self,710,0,self.WINDOW_PARENT.quit)
        back = MyWidgets.createBorderLessButton("BACK", self, 630, 0, self.back)

    def handleLinkClicked(self, url):
        action=url.toString()
        if action.__contains__("doSignup"):
            self.signup()
        elif(action.__contains__("doLogin")):
            self.login()
        else:
            self.recoverPassword()

    def handleFormSubmitted(self, url):
        print(url)

    def goToDashboard(self):
        dsh = DashboardWidget(self.WINDOW_PARENT)
        dsh.BACK_WIDGET = "SplashWidget"
        self.WINDOW_PARENT.setCentralWidget(dsh)

    def login(self):
        frame = self.view.page().mainFrame()
        document = frame.documentElement()
        try:
            enteredUsr= document.findAll(".getusername").at(0).toPlainText()
            enteredPas= document.findAll(".getpassword").at(0).toPlainText()
            retrieve = DatabaseMiddleWare.fetchUser(enteredUsr)
        except:
            print("db exception!")
        if retrieve is None:
            print("Username does not exist!")
            frame = self.view.page().mainFrame()
            frame.evaluateJavaScript('show();')
        else :
            retUser = str(retrieve['username']) #TODO : change the retrieving data according to the designed database. change to username
            retId = str(retrieve['id'])#TODO : change the retrieving data according to the designed database change to id
            retPass = str(retrieve['password'])#TODO : change the retrieving data according to the designed database change to password
            if retUser == enteredUsr :
                if retPass == enteredPas :
                    print("Welcome!!!")
                    print ("retID = "+retId+"\nretPass = "+retPass+"\nretUser = "+retUser)
                    Utils.UserManager.setCurrentUser(user=retrieve)
                    self.goToDashboard()
                else :

                    frame = self.view.page().mainFrame()
                    frame.evaluateJavaScript('show();')

    def recoverPassword(self):
        print("LOL!")
        rpf=RecoverPasswordForm(self.WINDOW_PARENT)
        rpf.show()

    def signup(self):
        from ui import RegisterPage
        signup = RegisterPage.RegisterPage(self.WINDOW_PARENT)
        RegisterPage.BACK_WIDGET = "NewLoginWidget"
        self.WINDOW_PARENT.setCentralWidget(signup)

    def back(self):
        back=Utils.UIHelper.backPressHandler(BACK_WIDGET,self.WINDOW_PARENT)
        self.WINDOW_PARENT.setCentralWidget(back)

class RecoverPasswordForm(QDialog):
    def __init__(self, parent=None):
        self.WINDOW_PARENT=parent
        super(RecoverPasswordForm, self).__init__(parent)
        self.setWindowTitle("Why do you forgot your password ma nigga?whyyyyyy?")
        self.view=QWebView(self)
        self.view.linkClicked.connect(self.handleLinkClicked)
        self.page = self.view.page()
        self.view.setMinimumSize(400, 400)
        self.view.setMaximumSize(400, 400)
        self.view.page().setLinkDelegationPolicy(
            QtWebKit.QWebPage.DelegateAllLinks)
        cwd = os.getcwd()
        self.view.load(QUrl.fromLocalFile(os.path.join(cwd, "resource", "RecoveryPassword.html")))
        self.WINDOW_PARENT.QApplicationRef.processEvents()
        self.view.show()
        self.setStyleSheet("border-width: 0px; border-style: solid")
        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

    def handleLinkClicked(self, url):
        action=url.toString()
        if action.__contains__("recover"):
            frame = self.view.page().mainFrame()
            document = frame.documentElement()
            try:
                answer = document.findAll("#getanswer").at(0).toPlainText()
                email = document.findAll("#getemail").at(0).toPlainText()
                question = document.findAll("#getquestion").at(0).toPlainText()
                passwd=DatabaseMiddleWare.recoverPassword(question,answer,email)
                document.findAll("#Respond").at(0).setPlainText(passwd)
            except:
                document.findAll("#Respond").at(0).setPlainText("Enter your email please")