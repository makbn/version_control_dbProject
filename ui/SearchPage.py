import os
import sys

from PySide.QtWebKit import QWebView, QWebPage

import MyWidgets
from PySide.QtCore import *
from PySide import *
from Database import DatabaseMiddleWare
from ui import RepositoryPage

PARTITION = 50
image_size = 64
BACK_WIDGET = None
class SearchPage(QtGui.QWidget):
    WINDOW_WIDTH= 800
    WINDOW_HEIGHT=600

    WINDOW_TITLE="Login"
    WINDOW_FOOTER_MESSAGE="Some Text here for DataBase Project 2016"
    WINDOW_PASSWORD_TITLE="Password :"
    WINDOW_USERNAM_TITLE="Username :"
    WINDOW_PARENT=None

    def __init__(self, parent=None):
        super(SearchPage, self).__init__(parent)
        self.WINDOW_PARENT=parent
        self.document= None
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
        self.view.load(QUrl.fromLocalFile(os.path.join(cwd,"resource","Search.html")))
        self.WINDOW_PARENT.QApplicationRef.processEvents()
        frame = self.view.page().mainFrame()
        self.document = frame.documentElement()
        self.fillTheLeftMenu(document=self.document)
        self.WINDOW_PARENT.QApplicationRef.processEvents()
        self.view.show()

    def handleLinkClicked(self, url):
        action=url.toString()
        print(self.document)
        if action.__contains__("DoSearch") :
            query = self.document.findAll("#getSearchQuery").at(0).toPlainText()
            self.search(query=query )
        elif action.__contains__("Repository") :
            self.gotoRepoPage(str(action).split("-")[1])
            print("goto repo page " + str(action).split("-")[1])

    def fillTheLeftMenu(self,document):
        repCount = DatabaseMiddleWare.getRepoNumber()
        userCount = DatabaseMiddleWare.getUsersNumber()
        issueCount = DatabaseMiddleWare.getIssueNumber()
        document.findAll("#RepoCounter").at(0).setPlainText(str(repCount[0]['count']))
        document.findAll("#UserCounter").at(0).setPlainText(str(userCount[0]['count']))
        document.findAll("#IssueCounter").at(0).setPlainText(str(issueCount[0]['count']))

    def fillTheListTempo(self ,fetchedResult, document=None):
        outer = ""
        searchResultTemplate = """<div class="searchResult" >
                                Project Name :
                                <a href="Repository-{RepoId}" class="Project-Name" style="margin: 5px">{ProjectName}</a>
                                <br>
                                User :
                                <a href="UserProfile-{UserId}" class="Username" style="margin: 5px">{Username}</a>
                                <hr></hr>
                            </div>"""
        for i in fetchedResult :
            inner = ""
            inner = searchResultTemplate.format(ProjectName = i['repo_name'],
                                                UserId = str(i['user_id']) ,
                                                RepoId = str(i['repo_id']) ,
                                                Username = i['first_name']+ " " + i['last_name'])

            outer = outer + inner
        document.findAll("#SearchResultList").at(0).setInnerXml(outer)

    def search(self,query) :
        searchResult = DatabaseMiddleWare.getAllRepoByName(query)
        self.fillTheListTempo(fetchedResult=searchResult,document=self.document)
        pass

    def addWidgets(self):
        self.background=MyWidgets.createBackground(self)
        self.loadSplash()
        dvider = MyWidgets.createLableColered(self,0,PARTITION*11 +10,self.WINDOW_WIDTH,100,"rgba(29,185,84,255)")
        footer = MyWidgets.createTextLable(self.WINDOW_FOOTER_MESSAGE, self,PARTITION*1, PARTITION*11 +15, "white", "5")
        close=MyWidgets.createBorderLessButton("EXIT",self,710,0,self.WINDOW_PARENT.quit)
        back=MyWidgets.createBorderLessButton("Back",self,630,0,self.back)

    def gotoRepoPage(self,id):
        RepoPage = RepositoryPage.RepositoryPage(self.WINDOW_PARENT,repositoryId=id)
        SearchPage.BACK_WIDGET = "DashboardWidget"
        self.WINDOW_PARENT.setCentralWidget(RepoPage)

    def back(self):
        import Utils
        back=Utils.UIHelper.backPressHandler(BACK_WIDGET,self.WINDOW_PARENT)
        self.WINDOW_PARENT.setCentralWidget(back)
