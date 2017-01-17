import os
from datetime import datetime
from random import randint

from PySide import *
from PySide.QtCore import QUrl
from PySide.QtGui import QListView, QStandardItemModel, QStandardItem, QListWidget, QListWidgetItem
from PySide.QtWebKit import QWebView
from Database import DatabaseMiddleWare
import Utils
from models import Repository
import MyWidgets
from ui import SearchPage

PARTITION = 50
image_size = 64
BACK_WIDGET=None
class DashboardWidget(QtGui.QWidget):
    WINDOW_WIDTH= 800
    WINDOW_HEIGHT=600
    WINDOW_TITLE="Dashbord"
    WINDOW_FOOTER_MESSAGE="Some text here for DataBase Project 2016"
    WINDOW_PARENT=None
    pageDocument = None


    def __init__(self, parent=None):
        super(DashboardWidget, self).__init__(parent)
        self.WINDOW_PARENT = parent
        self.layout = QtGui.QHBoxLayout()
        self.addWidgets()

    def addWidgets(self):
        self.background=MyWidgets.createBackground(self)
        self.loadRepository()
        self.loadPanel()
        dvider = MyWidgets.createLableColered(self,0,PARTITION*11 +10,self.WINDOW_WIDTH,100,"rgba(29,185,84,255)")
        footer = MyWidgets.createTextLable(self.WINDOW_FOOTER_MESSAGE, self,PARTITION*1, PARTITION*11 +15, "white", "5")
        close=MyWidgets.createBorderLessButton("EXIT",self,710,0,self.WINDOW_PARENT.quit)

    def loadRepository(self):
        self.view = QWebView(self)
        self.view.linkClicked.connect(self.handleLinkClicked)
        self.view.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        self.view.move((self.WINDOW_WIDTH / 2) + 1, 1)
        self.view.setMinimumSize((self.WINDOW_WIDTH / 2) - 2, PARTITION * 11 + 10)
        self.view.setMaximumSize((self.WINDOW_WIDTH / 2) - 2, PARTITION * 10 + 10)
        cwd = os.getcwd()
        self.view.load(QUrl.fromLocalFile(os.path.join(cwd,"resource","RepositoryList.html")))
        self.WINDOW_PARENT.QApplicationRef.processEvents()
        frame = self.view.page().mainFrame()
        document = frame.documentElement()
        self.pageDocument = document
        print(document.findAll("#repository_list").count())
        inner=""
        for num in range(21):
          inner+=self.createRepositoryElement(Repository.REPOSITORY_TEST)
        document.findAll("#repository_list").at(0).setInnerXml(inner)
        self.view.show()

    def loadPanel(self):
        self.view1 = QWebView(self)
        self.view1.linkClicked.connect(self.handleLinkClicked)
        self.view1.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        self.view1.move(1, 1)
        self.view1.setMinimumSize(self.WINDOW_WIDTH / 2, PARTITION * 11 + 10)
        self.view1.setMaximumSize(self.WINDOW_WIDTH / 2, PARTITION * 10 + 10)
        cwd = os.getcwd()
        self.fillTheNotifPanel()
        self.view1.load(QUrl.fromLocalFile(os.path.join(cwd,"resource","Panel.html")))
        self.WINDOW_PARENT.QApplicationRef.processEvents()
        self.view1.show()

    def fillTheNotifPanel(self):
        try :
            #fetching all the Notifications of the current user and add them to the list
            ListElement = self.pageDocument.findAll("#NotificationList").at(0)
            fetchedHtml = self.fetchNotification()
            inner = ""
            for html in fetchedHtml :
                inner = inner + html
            ListElement.setInnerXml(inner)
        except :
            print("Exection Occured")


    def fetchNotification(self):
        #TODO : fetching notification of the user
        print("fetching  " + Utils.UserManager.getCurrentUser())
        #TODO : fill the notification Template with fetched data
        NotReadNotification = """<li><a href="/Notif/{notifId}" style="background-color: white;color: black" class="glyphicon glyphicon-envelope">
                            {NotifTitle}</a></li>"""
        ReadNotification =   """<li><a href="/Notif-{notifId}" style="background-color: gray" class="glyphicon glyphicon-envelope">Title3</a></li>"""
        userId = str(Utils.UserManager.getCurrentUser())
        try:
            tuples = DatabaseMiddleWare.getEntityByKey("notification" , userId)
            htmlNotifications = None
            i = 0
            for row in tuples :
                notification = {
                    "id": row[0] ,
                    "user_id" : row[1] ,
                    "title" : row[2] ,
                    "description" : row[3] ,
                    "link_id" : row[4] ,
                    "link_type" : row[5] ,
                    "is_read" : row[6] ,
                    "created_date" : row[7]
                }
                if notification["is_read"] == "1"  or notification["is_read"] == 1:
                    htmlNotifications[i] = ReadNotification.format(NotifId = ReadNotification["id"] , NotifTitle= ReadNotification["title"])
                else:
                    htmlNotifications[i] = NotReadNotification.format(NotifId=NotReadNotification["id"],
                                                                   NotifTitle=NotReadNotification["title"])
                i = i+ 1
                #do the same thing for the next notification
            return htmlNotifications
        except:
            print("XXX fetching exception XXX")
            pass


    def createRepositoryElement(self,repository):

        innerHTML="""
        <div class="item" id={id}>
        <i class="large git square icon"></i>
        <div class="content container">
            <a class="header" href="{url}">{name}</a>
            <div class="description">{description}</div>
            <div class="row" style="display: flex; margin-top: 10px">
                <div class = "col-xs-3" style="padding-left: 2px">
                    <a class="ui {color} label">{visibility}</a>
                </div>
                <div class = "col-xs-3" style="padding-left: 2px">
                    <div class="ui label">
                        <i class="star icon"></i> {starcount}
                    </div>
                </div>

                <div class = "col-xs-3" style="padding-left: 2px">
                    <a class="ui blue label">makbn/Semantic...</a>
                </div>
            </div>
        </div>
    </div>
        <div></div>
        """

        visibility="public"
        color="green"
        if randint(0,9)%2==0:
            visibility="private"
            color="orange"
        innerHTML=innerHTML.format(id=repository.id, url="/" + repr(repository.id),starcount=repository.getStarCount(), name=repository.name, description=repository.description, visibility=visibility,color=color)
        return innerHTML

    def handleLinkClicked(self, url):
        print("clicked")
        myUrl = url.toString()
        if(myUrl.__contains__("Notif")):
            print("Notif identifier : " + myUrl)
            segment = myUrl
        elif myUrl.__contains__("search"):
            self.goToSearch()
        else :
            print("default")

    def goToSearch(self):
        search = SearchPage.SearchPage(self.WINDOW_PARENT)
        SearchPage.BACK_WIDGET = "DashboardWidget"
        self.WINDOW_PARENT.setCentralWidget(search)
    def handleLinkClicked2(self, url):
        print("clicked")
        myUrl = url.toString()
        if(myUrl.__contains__("Notif")):
            segment = url.spit("/")
            print("Notif identifier : "+segment[1])
        else :
            print("default")

