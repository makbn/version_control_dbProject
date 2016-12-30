import os
import sys

from PySide.QtWebKit import QWebView, QWebPage

import MyWidgets
from ui import MainWidget
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtDeclarative import *
from PySide import *
from random import  randint
from Database import DatabaseMiddleWare

PARTITION = 50
image_size = 64

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
        self.view.show()
        self.fillTheListTempo(document=self.document)


    def handleLinkClicked(self, url):
        action=url.toString()
        print(self.document)
        if action.__contains__("DoSearch") :
            query = self.document.findAll("#getSearchQuery").at(0).toPlainText()
            self.search(query=query )



    def fillTheListTempo(self , document=None):
        inner = ""
        for i in range(0,10) :
            print(i)
            username = "Navid" + str(randint(0,10))
            repoId = str(randint(0,10))
            userId = str(randint(15 , 25))
            projectName= "My Repo" + str(randint(0,5))
            searchResult = {
                "Username" : username ,
                "RepoId" : repoId ,
                "ProjectName" : projectName ,
                "UserId" : userId
            }
            inner = inner + self.addToSearchResult(searchResult=searchResult , document=document)
        document.findAll("#SearchResultList").at(0).setInnerXml(inner)




    def search(self,query) :
        print("database searching " + str(query))
        print("send the fetched data to addToSearchResult function one bye one ... ")
        self.fillTheListTempo(document=self.document)
        pass

    def addToSearchResult(self,searchResult , document):
        searchResultTemplate = """<div class="searchResult" style="color: whitesmoke;">
                        Project Name :
                        <a href="Repository/{RepoId}" class="Project-Name" style="margin: 5px">{ProjectName}</a>
                        <br>
                        User :
                        <a href="UserProfile/{UserId}" class="Username" style="margin: 5px">{Username}</a>
                        <hr></hr>
                    </div>"""
        newElement = searchResultTemplate.format(ProjectName = searchResult["ProjectName"] ,
                                                      Username= searchResult["Username"] ,
                                                      RepoId= searchResult["RepoId"] ,
                                                      UserId = searchResult["UserId"])
        return newElement

    def addWidgets(self):
        self.background=MyWidgets.createBackground(self)
        self.loadSplash()
        dvider = MyWidgets.createLableColered(self,0,PARTITION*11 +10,self.WINDOW_WIDTH,100,"rgba(29,185,84,255)")
        footer = MyWidgets.createTextLable(self.WINDOW_FOOTER_MESSAGE, self,PARTITION*1, PARTITION*11 +15, "white", "5")
        close=MyWidgets.createBorderLessButton("EXIT",self,710,0,self.WINDOW_PARENT.quit)
