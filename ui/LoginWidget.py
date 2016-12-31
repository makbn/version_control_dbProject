import sys
import MyWidgets
from ui import MainWidget
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtDeclarative import *
from PySide import *
from Database import DatabaseMiddleWare
from ui import RegisterPage

PARTITION = 50
image_size = 64

class LoginWidget(QtGui.QWidget):
    WINDOW_WIDTH= 800
    WINDOW_HEIGHT=600

    WINDOW_TITLE="Login"
    WINDOW_FOOTER_MESSAGE="Some text here for DataBase Project 2016"
    WINDOW_PASSWORD_TITLE="Password :"
    WINDOW_USERNAM_TITLE="Username :"
    WINDOW_PARENT=None

    def __init__(self, backWidget, parent=None):
        super(LoginWidget, self).__init__(parent)
        self.WINDOW_PARENT=parent
        self.layout = QtGui.QHBoxLayout()
        self.addWidgets()
        self.backWidget=backWidget

    def addWidgets(self):

        self.background=MyWidgets.createBackground(self)
        dvider = MyWidgets.createLableColered(self,0,PARTITION*10 + 10,self.WINDOW_WIDTH,100,"rgba(29,185,84,255)")
        footer = MyWidgets.createTextLable(self.WINDOW_FOOTER_MESSAGE, self,PARTITION*1, PARTITION*10 +20, "white", "5")

        #LoginWidget.add_info(self) #adding the General information to the welcome scene


        usernameTitle = MyWidgets.createTextLable(self.WINDOW_USERNAM_TITLE,self,PARTITION*1,PARTITION*4,"white","5")
        self.username=MyWidgets.createEditText("",self,PARTITION*1,PARTITION*5,350,24)
        self.usernameError=MyWidgets.createTextLable("Something Wrong With your Username",self,100,75,"red","4")
        self.usernameError.setVisible(False)

        passwordTitle = MyWidgets.createTextLable(self.WINDOW_PASSWORD_TITLE,self,PARTITION*1,PARTITION*6,"white","5")
        self.password=MyWidgets.createEditText("",self,PARTITION*1,PARTITION*7,350,24)
        self.passwordError=MyWidgets.createTextLable("Something Wrong With your Password",self,100,145,"red","4")
        self.passwordError.setVisible(False)


        loginbtn=MyWidgets.createPushButton("Login",self,PARTITION *1,PARTITION*8,self.login)
        signupbtn = MyWidgets.createPushButton("Signup",self,PARTITION *4,PARTITION * 8,self.signup)
        close=MyWidgets.createBorderLessButton("EXIT",self,710,16,self.WINDOW_PARENT.quit)



        self.layout.addWidget(self.passwordError)

    def add_info(self):
        user_image = MyWidgets.createImage(self, PARTITION * 2, PARTITION * 1, image_size, image_size,
                                           "/home/navid/Desktop/User_Green.png")
        user_numbers_info = MyWidgets.createTextLable("1234", self, PARTITION * 2, PARTITION * 3,
                                               "white", "2")

        repo_image = MyWidgets.createImage(self, PARTITION * 6, PARTITION * 1, image_size, image_size,
                                           "/home/navid/Desktop/Repo_Green.png")

        user_numbers_info = MyWidgets.createTextLable("3211", self, PARTITION * 6, PARTITION * 3,
                                                  "white", "2")


    def login(self):
        m="sd"
        enteredUsr= self.username.toPlainText()+""
        enteredPas= self.password.toPlainText()+""
        retrieve = DatabaseMiddleWare.fetchUser(enteredUsr)
        if retrieve is None:
            print("Username does not exist!")
        else :
            retUser = str(retrieve['customerNumber']) #TODO : change the retrieving data according to the designed database. change to username
            retId = str(retrieve['country'])#TODO : change the retrieving data according to the designed database change to id
            retPass = str(retrieve['phone'])#TODO : change the retrieving data according to the designed database change to password
            if retUser == enteredUsr :
                if retPass == enteredPas :
                    print("Welcome!!!")
                    print ("retID = "+retId+"\nretPass = "+retPass+"\nretUser = "+retUser)
                else :
                    print("Username or Password is incorrect!!!")

    def signup(self):
        signUp = RegisterPage.RegisterPage(self,self)
        self.WINDOW_PARENT.setCentralWidget(signUp)

    def back(self):
        self.WINDOW_PARENT.setCentralWidget(self.backWidget)
