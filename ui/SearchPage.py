import os
import sys

from PySide.QtWebKit import QWebView, QWebPage

import MyWidgets
from PySide.QtCore import *
from PySide import *
from Database import DatabaseMiddleWare
from ui import ProfileWidget
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
        self.WINDOW_PARENT.QApplicationRef.processEvents()
        self.view.show()

    def handleLinkClicked(self, url):
        outer=""
        action=url.toString()
        print(action)
        if action.__contains__("DoSearch") :
            query = self.document.findAll("#getSearchQuery").at(0).toPlainText()
            self.search(query=query )
        elif action.__contains__("Repository") :
            self.gotoRepoPage(str(action).split("-")[1])
            print("goto repo page " + str(action).split("-")[1])
        elif action.__contains__("filterUser"):
            for i in self.usr:
                inner = self.userHtml.format(UserId=i['id'], Username=i['username'],fullName=i['first_name'] + " " + i['last_name'])
                outer = outer + inner
            self.document.findAll("#SearchResultList").at(0).setInnerXml(outer)
        elif action.__contains__("filterRepo"):
            print("filter Repository")
            for i in self.rep:
                inner = ""
                inner = self.repoHtml.format(ProjectName=i['repo_name'],UserId=str(i['uid']),RepoId=str(i['rid']),Username=i['username'])
                outer = outer + inner
            self.document.findAll("#SearchResultList").at(0).setInnerXml(outer)
        elif action.__contains__("filterIssue"):
            for i in self.isu:
                inner = self.issueHtml.format(IssueId=i['iid'], IssueName=i['title'], repoId=i['rid'],RepoName=i['repo_name'])
                outer = outer + inner
            self.document.findAll("#SearchResultList").at(0).setInnerXml(outer)
        elif action.__contains__("User-"):
            action=action[13:]
            user=DatabaseMiddleWare.getUserById(action)
            if user is not None:
                self.gotToProfile(user)
            print(action)


    def gotToProfile(self,user):
        widget = ProfileWidget.ProfileWidget(self.WINDOW_PARENT,user)
        ProfileWidget.BACK_WIDGET = "SearchPage"
        self.WINDOW_PARENT.setCentralWidget(widget)

    def fillTheLeftMenu(self):

        self.document.findAll("#RepoCounter").at(0).setPlainText(str(len(self.rep)))
        self.document.findAll("#UserCounter").at(0).setPlainText(str(len(self.usr)))
        self.document.findAll("#IssueCounter").at(0).setPlainText(str(len(self.isu)))

    def fillTheListTempo(self ,repo,isu,usr):
        self.fillTheLeftMenu()
        outer = ""
        self.repoHtml = """<div class="well searchResult" >
                                Project Name :
                                <a href="Repository-{RepoId}" class="Project-Name" style="margin: 5px">{ProjectName}</a>
                                <br>
                                User :
                                <a href="/User-{UserId}" class="Username" style="margin: 5px">{Username}</a>

                            </div>"""

        self.issueHtml = """<div class="well searchResult" >
                                        Issue Title :
                                        <a href="/Issue-{IssueId}" class="Project-Name" style="margin: 5px">{IssueName}</a>
                                        <br>
                                        Repository :
                                        <a href="/Repository-{repoId}" class="Username" style="margin: 5px">{RepoName}</a>

                                    </div>"""
        self.userHtml = """<div class="well searchResult" >
                                        User :
                                        <a href="/User-{UserId}" class="Project-Name" style="margin: 5px">{Username}</a>
                                        <br>
                                        Info :
                                        <a href="/User-{UserId}" class="Username" style="margin: 5px">{fullName}</a>

                                    </div>"""
        outer=""
        for i in repo :
            inner = ""
            inner = self.repoHtml.format(ProjectName = i['repo_name'],
                                                UserId = str(i['uid']) ,
                                                RepoId = str(i['rid']) ,
                                                Username = i['username'])

            outer = outer + inner

        for i in isu:
            inner = self.issueHtml.format(IssueId=i['iid'],IssueName=i['title'],repoId=i['rid'],RepoName=i['repo_name'])
            outer = outer + inner

        for i in usr:
            inner=self.userHtml.format(UserId=i['id'],Username=i['username'],fullName=i['first_name']+" "+i['last_name'])
            outer = outer + inner

        self.document.findAll("#SearchResultList").at(0).setInnerXml(outer)

    def search(self,query) :
        self.rep = DatabaseMiddleWare.findRepositoryByName(query)
        self.isu=DatabaseMiddleWare.findIssueByName(query)
        self.usr=DatabaseMiddleWare.findUserByName(query)
        self.fillTheListTempo(repo=self.rep,isu=self.isu,usr=self.usr)


    def addWidgets(self):
        self.background=MyWidgets.createBackground(self)
        self.loadSplash()
        dvider = MyWidgets.createLableColered(self,0,PARTITION*11 +10,self.WINDOW_WIDTH,100,"rgba(29,185,84,255)")
        footer = MyWidgets.createTextLable(self.WINDOW_FOOTER_MESSAGE, self,PARTITION*1, PARTITION*11 +15, "white", "5")
        close=MyWidgets.createBorderLessButton("EXIT",self,710,0,self.WINDOW_PARENT.quit)
        back=MyWidgets.createBorderLessButton("BACK",self,630,0,self.back)

    def gotoRepoPage(self,id):
        RepoPage = RepositoryPage.RepositoryPage(self.WINDOW_PARENT,repositoryId=id)
        RepositoryPage.BACK_WIDGET = "DashboardWidget"
        self.WINDOW_PARENT.setCentralWidget(RepoPage)

    def back(self):
        import Utils
        back=Utils.UIHelper.backPressHandler(BACK_WIDGET,self.WINDOW_PARENT)
        self.WINDOW_PARENT.setCentralWidget(back)
