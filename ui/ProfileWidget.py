import os

from PySide import QtGui, QtWebKit
from PySide.QtCore import QUrl
from PySide.QtWebKit import QWebView

import MyWidgets
import Utils
from Database import DatabaseMiddleWare
from ui import RepositoryPage

PARTITION = 50
image_size = 64
BACK_WIDGET = None


class ProfileWidget(QtGui.QWidget):
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    WINDOW_TITLE = "Profile"
    WINDOW_FOOTER_MESSAGE = "Some Text here for DataBase Project 2016"
    WINDOW_PARENT = None
    currentUser = None
    thisUser = None

    def __init__(self, parent=None, user=None):
        super(ProfileWidget, self).__init__(parent)
        self.thisUser = user
        self.WINDOW_PARENT = parent
        self.addWidgets()

    def addWidgets(self):
        self.background = MyWidgets.createBackground(self)
        self.loadPage()
        dvider = MyWidgets.createLableColered(self, 0, PARTITION * 11 + 10, self.WINDOW_WIDTH, 100,
                                              "rgba(29,185,84,255)")

        footer = MyWidgets.createTextLable(self.WINDOW_FOOTER_MESSAGE, self, PARTITION * 1, PARTITION * 11 + 15,
                                            "white", "5")
        close = MyWidgets.createBorderLessButton("EXIT", self, 710, 0, self.WINDOW_PARENT.quit)
        back = MyWidgets.createBorderLessButton("BACK", self, 630, 0, self.back)
        if Utils.UserManager.getCurrentUser()['id']==self.thisUser['id']:
            print("its your own page")
        elif DatabaseMiddleWare.isFolowing(Utils.UserManager.getCurrentUser()['id'],self.thisUser['id']) is None:
            self.followbtn = MyWidgets.createBorderLessButton("FOLLOW+", self, 520, 0, self.follow)
        else:
            self.followbtn = MyWidgets.createBorderLessButton("FOLLOW+", self, 520, 0, self.unfollow)

    def createRepositoryElement(self):
        outerHtml = ""
        private_label = "orange"
        public_label = "green"
        innerHTML = """
           <div class="item" id={user_id}>
           <i class="large git square icon"></i>
           <div class="content container">
               <a class="header" href="{url}">{name}</a>
               <div class="description">{description}</div>
               <div class="row" style="display: flex; margin-top: 10px">
                   <div class = "col-xs-3" style="padding-left: 15px">
                       <a class="ui label {color}">{visibility}</a>
                   </div>
                   <div class = "col-xs-3" style="padding-left: 15px">
                       <div class="ui label">
                           <i class="star icon"></i> {StarCounter}
                       </div>
                   </div>

                   <div class = "col-xs-3" style="padding-left: 15px">
                       <a class="ui blue label">{username}/{name2}</a>
                   </div>
               </div>
           </div>
       </div>
           <div></div>
           """
        repoList = DatabaseMiddleWare.getAllRepoOfTheUser(self.thisUser)
        for i in repoList:
            if i["is_private"] == 1:
                continue
            starCount = DatabaseMiddleWare.getStarCount(i["id"])
            print(starCount)
            temp = innerHTML.format(user_id=str(i["user_id"]),
                                    url="/Repository-{RepoId}".format(RepoId=str(i["id"])),
                                    name=i["repo_name"],
                                    StarCounter=str(starCount["stars"]),
                                    description=i["description"][:10] + "...",
                                    visibility="private" if (int(i["is_private"]) == 1) else "public",
                                    color=private_label if (int(i["is_private"]) == 1) else public_label,
                                    username=Utils.UserManager.getCurrentUser()['username'],
                                    name2=i["repo_name"]
                                    )
            outerHtml += temp
        return outerHtml

    def loadPage(self):
        self.view = QWebView(self)
        #self.view.webkit.page().userAgentForUrl = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:37.0) Gecko/20100101 Firefox/37.0"
        self.view.linkClicked.connect(self.handleLinkClicked)
        self.page =self.view.page()
        self.view.setMinimumSize(self.WINDOW_WIDTH+50,PARTITION*11 + 10)
        self.view.setMaximumSize(self.WINDOW_WIDTH+50,PARTITION*10 + 10)
        self.view.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        cwd = os.getcwd()
        self.view.load(QUrl.fromLocalFile(os.path.join(cwd,"resource","UserProfile.html")))
        self.WINDOW_PARENT.QApplicationRef.processEvents()
        frame = self.view.page().mainFrame()
        self.document = frame.documentElement()
        self.WINDOW_PARENT.QApplicationRef.processEvents()
        frame = self.view.page().mainFrame()
        document = frame.documentElement()
        self.pageDocument = document
        repoHtml = self.createRepositoryElement()
        document.findAll("#repository_list").at(0).setInnerXml(repoHtml)
        document.findAll("#username").at(0).setInnerXml("@"+str(self.thisUser['username']))
        document.findAll("#fullName").at(0).setInnerXml(str(self.thisUser['first_name']) +" "+str(self.thisUser['last_name']))
        self.view.show()

    def back(self):
        back=Utils.UIHelper.backPressHandler(BACK_WIDGET,self.WINDOW_PARENT)
        self.WINDOW_PARENT.setCentralWidget(back)

    def handleLinkClicked(self, url):
        myUrl = url.toString()
        print(myUrl)
        if myUrl.__contains__("Repository"):
            self.gotoRepoPage(str(myUrl).split("-")[1])
            print("goto repo page " + str(myUrl).split("-")[1])

    def follow(self):
        print("follow")
        if Utils.UserManager.getCurrentUser()['id']==self.thisUser['id']:
            print("you cant Follow yourself dude!be gentle please!")
        else:
            DatabaseMiddleWare.follow(Utils.UserManager.getCurrentUser()['id'],self.thisUser['id'])
            self.followbtn.setText("Unfollow!")
            self.followbtn.clicked.connect(self.unfollow)


    def unfollow(self):
        print("UN-FOLLOW!")
        DatabaseMiddleWare.unfollow(Utils.UserManager.getCurrentUser()['id'],self.thisUser['id'])
        self.followbtn.setText("Follow!")
        self.followbtn.clicked.connect(self.follow)

    def gotoRepoPage(self,id):
        RepoPage = RepositoryPage.RepositoryPage(self.WINDOW_PARENT,repositoryId=id)
        RepositoryPage.BACK_WIDGET = "DashboardWidget"
        self.WINDOW_PARENT.setCentralWidget(RepoPage)
