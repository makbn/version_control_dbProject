import sys
import MyWidgets
from PySide.QtCore import *
from PySide.QtGui import *
from ui import NewLogin
from ui import SplashWidget
from ui import DashbordWidget
from ui import  RegisterPage
from PySide.QtDeclarative import *
from PySide import *
from Database import DatabaseMiddleWare


# Our main window
from ui import RepositoryPage
from ui.CreateRepWidget import CreateRepWidget


class MainWindow(QtGui.QMainWindow):
    WINDOW_WIDTH= 800
    WINDOW_HEIGHT=600
    WINDOW_TITLE="Login"
    WINDOW_FOOTER_MESSAGE="Some Text here for DataBase Project 2016"
    WINDOW_PASSWORD_TITLE="Password"
    WINDOW_USERNAM_TITLE="Username"

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.central_widget = QtGui.QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.QApplicationRef = qApp
        print(self.QApplicationRef)



        #splash_widget=SplashWidget.SplashWidget(self)
        splash_widget=CreateRepWidget(self)
        #.splash_widget=RepositoryPage.RepositoryPage(self,"navid","gozo")

        self.central_widget.addWidget(splash_widget)
        #self.setWindowTitle(self.WINDOW_TITLE)
        self.setMinimumSize(self.WINDOW_WIDTH,self.WINDOW_HEIGHT)
        self.setMaximumSize(self.WINDOW_WIDTH,self.WINDOW_HEIGHT)
        self.setStyleSheet("border-width: 0px; border-style: solid")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)


    def setWidget(self,widget):
        self.setCentralWidget(widget)

    def quit(self):
        app.quit()






if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    DatabaseMiddleWare.initialize()
    # Create and show the main window
    window = MainWindow()
    window.show()
    # Run the main Qt loop
    sys.exit(app.exec_())