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
from ui import CreateRepWidget
from ui import CrtRepositoryWidget
from ui import LoginWidget
from ui import RepositoryPage
from ui import SearchPage

PARTITION = 50
image_size = 64
BACK_WIDGET=None
class DashboardWidget(QtGui.QWidget):
    WINDOW_WIDTH= 800
    WINDOW_HEIGHT= 600
    WINDOW_TITLE="Dashbord"
    WINDOW_FOOTER_MESSAGE="Some text here for DataBase Project 2016"
    WINDOW_PARENT=None
    pageDocument = None
    currentUser = None


    def __init__(self, parent=None):
        super(DashboardWidget, self).__init__(parent)
        self.WINDOW_PARENT = parent
        self.currentUser = Utils.UserManager.getCurrentUser()
        self.layout = QtGui.QHBoxLayout()
        self.addWidgets()


    def addWidgets(self):
        self.background=MyWidgets.createBackground(self)
        self.loadRepository()
        self.loadPanel()
        dvider = MyWidgets.createLableColered(self,0,PARTITION*11 +10,self.WINDOW_WIDTH,100,"rgba(29,185,84,255)")
        lable=MyWidgets.createLableColered(self,0,0,(1.5*self.WINDOW_WIDTH / 3)+1,50,"rgb(64, 64, 64)")
        lable=MyWidgets.createLableColered(self,0,50,(1.5*self.WINDOW_WIDTH / 3)+1,1,"rgb(14, 164, 50)")
        profile= MyWidgets.createTextLable("Profile & Notifications", self,10, 15, "white", "5")
        footer = MyWidgets.createTextLable(self.WINDOW_FOOTER_MESSAGE, self,PARTITION*1, PARTITION*11 +15, "white", "5")
        close=MyWidgets.createBorderLessButton("EXIT",self,710,0,self.WINDOW_PARENT.quit)

    def loadRepository(self):
        self.view = QWebView(self)
        self.view.linkClicked.connect(self.handleLinkClicked)
        self.view.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        self.view.move((1.5 * self.WINDOW_WIDTH / 3) + 1, 0)
        self.view.setMinimumSize((1.5*self.WINDOW_WIDTH / 3) - 2, PARTITION * 11 + 10)
        self.view.setMaximumSize((1.5*self.WINDOW_WIDTH / 3) - 2, PARTITION * 10 + 10)
        cwd = os.getcwd()
        self.view.load(QUrl.fromLocalFile(os.path.join(cwd,"resource","RepositoryList.html")))
        self.WINDOW_PARENT.QApplicationRef.processEvents()
        frame = self.view.page().mainFrame()
        document = frame.documentElement()
        self.pageDocument = document
        repoHtml = self.fetchRepo()
        document.findAll("#repository_list").at(0).setInnerXml(repoHtml)
        self.view.show()

    def loadPanel(self):
        self.view1 = QWebView(self)
        self.view1.linkClicked.connect(self.handleLinkClicked)
        self.view1.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        self.view1.move(0, 50)
        self.view1.setMinimumSize(1.5*self.WINDOW_WIDTH / 3, PARTITION * 11 )
        self.view1.setMaximumSize(1.5*self.WINDOW_WIDTH / 3, PARTITION * 10 )
        cwd = os.getcwd()

        self.fillTheNotifPanel()

        self.view1.load(QUrl.fromLocalFile(os.path.join(cwd,"resource","Panel.html")))

        self.WINDOW_PARENT.QApplicationRef.processEvents()
        doc = self.view1.page().mainFrame().documentElement()
        doc.findAll("#namePlaceHolder").at(0).setPlainText(str(self.currentUser["first_name"]) + " " + str(self.currentUser["last_name"]))
        doc.findAll("#usernamePlaceHolder").at(0).setPlainText(str(self.currentUser["username"]))

        self.view1.show()

    # ----- Notification ----
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
    #------ END Notification ----

    def createRepositoryElement(self):
        outerHtml = ""
        private_label = "orange"
        public_label = "green"
        innerHTML="""
        <div class="item" id={user_id}>
        <i class="large git square icon"></i>
        <div class="content container">
            <a class="header" href="{url}">{name}</a>
            <div class="description">{description}</div>
            <div class="row" style="display: flex; margin-top: 10px">
                <div class = "col-xs-3" style="padding-left: 5px">
                    <a class="ui label {color}">{visibility}</a>
                </div>
                <div class = "col-xs-3" style="padding-left: 5px">
                    <div class="ui label">
                        <i class="star icon"></i> {StarCounter}
                    </div>
                </div>

                <div class = "col-xs-3" style="padding-left: 5px">
                    <a class="ui blue label">{name2}</a>
                </div>
            </div>
        </div>
    </div>
        <div></div>
        """
        repoList = DatabaseMiddleWare.getAllRepoOfTheUser(self.currentUser)
        for i in repoList :
            starCount = DatabaseMiddleWare.getStarCount(i["id"])
            print(starCount)
            temp=innerHTML.format(      user_id=str(i["user_id"]),
                                        url="/Repository-{RepoId}".format(RepoId=str(i["id"])),
                                        name=i["repo_name"],
                                        StarCounter=str(starCount["stars"]),
                                        description=i["description"][:10] + "...",
                                        visibility="private" if (int(i["is_private"]) == 1) else "public",
                                        color=private_label if (int(i["is_private"]) == 1) else public_label,
                                        name2=str(str(Utils.UserManager.getCurrentUser()['username'])+"/"+str(i["repo_name"]))[:14]+"..."
            )
            outerHtml = outerHtml + temp
        return outerHtml

    def handleLinkClicked(self, url):
        myUrl = url.toString()
        if(myUrl.__contains__("Notif")):
            print("Notif identifier : " + myUrl)
            segment = myUrl
        elif myUrl.__contains__("search"):
            print("searching ... ")
            self.goToSearch()
        elif myUrl.__contains__("logOut"):
            print("Loging out ...")
            self.logOut()
        elif myUrl.__contains__("createRepo"):
            self.goToCreateRepo()
        elif myUrl.__contains__("Repository"):
            self.goToRepoPage(myUrl.split("-")[1])
        else :
            print("default")

    def goToCreateRepo(self):
        CrtRepPage = CreateRepWidget.CreateRepWidget(self.WINDOW_PARENT)
        SearchPage.BACK_WIDGET = "DashboardWidget"
        self.WINDOW_PARENT.setCentralWidget(CrtRepPage)

    def goToRepoPage(self,id):
        print(id)
        RepoPage = RepositoryPage.RepositoryPage(self.WINDOW_PARENT, repositoryId=id)
        SearchPage.BACK_WIDGET = "DashboardWidget"
        self.WINDOW_PARENT.setCentralWidget(RepoPage)

    def goToSearch(self):
        search = SearchPage.SearchPage(self.WINDOW_PARENT)
        SearchPage.BACK_WIDGET = "DashboardWidget"
        self.WINDOW_PARENT.setCentralWidget(search)

    def logOut(self):
        Utils.UserManager.resetUser()
        from ui import NewLogin
        login= NewLogin.NewLoginWidget(self.WINDOW_PARENT)
        self.WINDOW_PARENT.setCentralWidget(login)

    def handleLinkClicked2(self, url):
        myUrl = url.toString()
        if(myUrl.__contains__("Notif")):
            segment = url.spit("/")
        else :
            print("default")

    def fetchRepo(self):
        return self.createRepositoryElement()

    def setUsername(self,document):
        nameHolder = document.findAll("#namePlaceHolder").at(0)
        usernameHolder = document.findAll("#usernamePlaceHolder").at(0)
        document.findAll("namePlaceHolder").at(0).setPlainText(str(self.currentUser["first_name"]) + " " + str(self.currentUser["last_name"]))
        document.findAll("usernamePlaceHolder").at(0).setInnerXml(str(self.currentUser["username"]))