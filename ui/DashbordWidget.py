import os
from datetime import datetime

from PySide import *
from PySide.QtCore import QUrl
from PySide.QtGui import QListView, QStandardItemModel, QStandardItem, QListWidget, QListWidgetItem
from PySide.QtWebKit import QWebView

import MyWidgets

PARTITION = 50
image_size = 64

class DashboardWidget(QtGui.QWidget):
    WINDOW_WIDTH= 800
    WINDOW_HEIGHT=600

    WINDOW_TITLE="Dashbord"
    WINDOW_FOOTER_MESSAGE="Some text here for DataBase Project 2016"
    WINDOW_PARENT=None
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
        self.view.move(1,1)
        self.view.page().setLinkDelegationPolicy(
        QtWebKit.QWebPage.DelegateAllLinks)
        self.view.setMinimumSize(self.WINDOW_WIDTH/2,PARTITION*11 + 10)
        self.view.setMaximumSize(self.WINDOW_WIDTH/2,PARTITION*10 + 10)
        cwd = os.getcwd()
        self.view.load(QUrl.fromLocalFile(os.path.join(cwd,"resource","RepositoryList.html")))
        self.WINDOW_PARENT.QApplicationRef.processEvents()

        frame = self.view.page().mainFrame()
        document = frame.documentElement()
        print(document.findAll("#repository_list").count())
        inner=""
        for num in range(21):
            inner+=self.createRepositoryElement(self)
        document.findAll("#repository_list").at(0).setInnerXml(inner)
        self.view.show()

    def loadPanel(self):
        self.view1 = QWebView(self)
        self.view1.linkClicked.connect(self.handleLinkClicked)
        self.view1.page().setLinkDelegationPolicy(
        QtWebKit.QWebPage.DelegateAllLinks)
        self.view1.move((self.WINDOW_WIDTH/2)+1,1)
        self.view1.setMinimumSize((self.WINDOW_WIDTH/2)-2,PARTITION*11 + 10)
        self.view1.setMaximumSize((self.WINDOW_WIDTH/2)-2,PARTITION*10 + 10)
        cwd = os.getcwd()
        self.view1.load(QUrl.fromLocalFile(os.path.join(cwd,"resource","Panel.html")))
        self.WINDOW_PARENT.QApplicationRef.processEvents()
        self.view1.show()

    def createRepositoryElement(self,repository):
        # name=repository.getName()
        # description=repository.getDesription()
        # starCount=repository.getStar()
        # availability=repository.getAvailability()
        id=232
        name="mehdi"
        description="hahahahahahha"
        availability="private"

        innerHTML="""
        <div class="item" id={id}>
            <i class="large git square icon"></i>
            <div class="content" href="{url}">
                <a class="header" href="{url}">{name}</a>
                <div class="description">{description}</div>
                <div style="display: inline-flex; margin-top: 10px">
                    <div style="padding-left: 10px">
                        <a class="ui {color} label">{availability}</a>
                    </div>
                </div>
            </div>
        </div>
        <div></div>
        """
        innerHTML=innerHTML.format(id=id, url="/" + repr(id), name=name, description=description, availability=availability,color="orange")
        return innerHTML

    def handleLinkClicked(self, url):
        action=url.toString()[8:]
        print(action)


