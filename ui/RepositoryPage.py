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

PARTITION = 50
image_size = 64
BACK_WIDGET = None
class RepositoryPage(QtGui.QWidget):
    WINDOW_WIDTH= 800
    WINDOW_HEIGHT=600
    WINDOW_TITLE="Login"
    WINDOW_FOOTER_MESSAGE="Some Text here for DataBase Project 2016"
    WINDOW_PASSWORD_TITLE="Password :"
    WINDOW_USERNAM_TITLE="Username :"
    WINDOW_PARENT=None
    repositoryName = ""
    repositoryId = ""
    page_document = None
    MyRepo=None

    def __init__(self,parent=None , repositoryId=None):
        super(RepositoryPage, self).__init__(parent)
        self.WINDOW_PARENT=parent
        self.layout = QtGui.QHBoxLayout()
        self.repositoryId = repositoryId
        print(self.repositoryName)
        self.addWidgets()

    def addWidgets(self):
        self.background=MyWidgets.createBackground(self)
        self.loadSplash()
        dvider = MyWidgets.createLableColered(self,0,PARTITION*11 +10,self.WINDOW_WIDTH,100,"rgba(29,185,84,255)")
        footer = MyWidgets.createTextLable(self.WINDOW_FOOTER_MESSAGE, self,PARTITION*1, PARTITION*11 +15, "white", "5")
        close=MyWidgets.createBorderLessButton("EXIT",self,710,0,self.WINDOW_PARENT.quit)
        close=MyWidgets.createBorderLessButton("BACK",self,630,0,self.back)

    def loadSplash(self):
        self.view = QWebView(self)
        self.view.linkClicked.connect(self.handleLinkClicked)
        self.page =self.view.page()
        self.view.setMinimumSize(self.WINDOW_WIDTH,PARTITION*11 + 10)
        self.view.setMaximumSize(self.WINDOW_WIDTH,PARTITION*10 + 10)
        self.view.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        cwd = os.getcwd()
        self.view.load(QUrl.fromLocalFile(os.path.join(cwd,"resource","RepPage.html")))
        self.WINDOW_PARENT.QApplicationRef.processEvents()
        frame = self.view.page().mainFrame()
        document = frame.documentElement()
        self.page_document = document
        self.fillTheDocument(document=document)
        self.view.show()

    def fillTheDocument(self , document=None):
        self.MyRepo = DatabaseMiddleWare.fetchRepoDataById(self.repositoryId)[0]
        starCount = DatabaseMiddleWare.getStarCount(self.repositoryId)
        isForked = self.isForked(repId=self.MyRepo["id"],userId=Utils.UserManager.getCurrentUser()["id"])
        if isForked == True : document.findAll("#ForkButton").at(0).setPlainText("Forked")
        else : document.findAll("#ForkButton").at(0).setPlainText("Fork")
        document.findAll("#RepositoryName").at(0).setPlainText(self.MyRepo["repo_name"])
        document.findAll("#StarCount").at(0).setPlainText(str(starCount["stars"]))
        document.findAll("#exampleTextarea").at(0).setPlainText(self.MyRepo["description"])
        allIssues = DatabaseMiddleWare.fetchIssuesForRepo(self.repositoryId)
        issueHtml = self.createIssueList(allIssues)
        document.findAll("#IssueList").at(0).setInnerXml(issueHtml)
        hasStar = DatabaseMiddleWare.checkStarForRepo(repId=self.MyRepo["id"],
                                                      userId=Utils.UserManager.getCurrentUser()["id"])
        if hasStar is None : document.findAll("#StarButton").at(0).setPlainText("Star")
        else:document.findAll("#StarButton").at(0).setPlainText("Un-Star")

    def createIssueList(self , issues):
        is_open_color = "deepskyblue"
        not_open_color = "lawngreen"
        template = """<li class="list-group-item " style="margin-outside: 1px">
                            <span class="glyphicon glyphicon-pushpin"></span>
                            Title :
                            <a href="/Issue-{IssueId}" style="color: {Color} ">{IssueTitle}</a>
                            <p>{IssueDesc}</p>
                        </li>"""
        outer = ""

        for issue in issues:
            inner = template.format(IssueId =issue["id"] ,
                                    Color=is_open_color if issue["is_open"] == 1 else not_open_color ,
                                    IssueTitle =issue["title"] ,
                                    IssueDesc = issue["description"])
            outer = outer + inner
        return outer

    def Repository(self , repositoryName):
        pass

    def handleLinkClicked(self, url):
        action=url.toString()
        if(action.__contains__("doFork")):

            if self.isForked(repId=self.repositoryId,userId=Utils.UserManager.current_user["id"]) == False :
                self.fork()
        elif(action.__contains__("doLike")):
            self.starUnstar()
        elif action.__contains__("Issue"):
            self.selectIssue(action.split("-")[1])
            self.issue_id = action.split("-")[1]
        elif action.__contains__("doAnswer"):
            self.addAnswer()
        elif action.__contains__("doissue"):
            self.addIssue()
        elif action.__contains__("doCommit"):
            self.commit()


    def selectIssue(self,issue_id):
        print("selected Issue ->" + issue_id)
        self.issue_id=issue_id
        #TODO : get the answers of this issue from db
        answersList = DatabaseMiddleWare.getTheAnswerOfIssue(issue_id)
        #TODO : put them in the menu
        answerHtml = self.giveAnswersHtml(answerList=answersList)
        self.page_document.findAll("#AnswerList").at(0).setInnerXml(answerHtml)
        pass

    def giveAnswersHtml(self,answerList):
        correctColor = "lawngreen"
        notCorrectColor = "orange"
        outer = ""
        template = """<li class="list-group-item " style="margin-outside: 1px;margin-bottom : 3px">
                            <span style="color: {Color}" class="glyphicon glyphicon-comment"></span>
                            <a href="user-{UserId}">{Username}</a>
                            <p class="IssueAnswer">{Answer}</p>
                        </li>"""

        for answer in answerList :
            username=""
            inner = template.format(    Answer=answer["description"],
                                        UserId=answer["user_id"],
                                        Username=(answer["first_name"] + " "+ answer["last_name"]),
                                        Color=correctColor if (answer["is_correct"] == 1) else notCorrectColor)
            outer = outer + inner
        print(outer)
        return outer

    def fork(self):
        result = DatabaseMiddleWare.forkRepository(source=self.MyRepo , user_id=Utils.UserManager.getCurrentUser()["id"])
        if(result == False) : print("You cannot fork this repository!!!")
        else : print("Forked successfully")

    def isForked(self,repId,userId):
        isForked = DatabaseMiddleWare.checkForked(repId=repId,userId=userId)
        if isForked is not None : return False
        else:return True

    def updateForked(self):
        self.page_document.findAll("#FrokButton").at(0).setPlainText("Forked")

    def starUnstar(self):
        hasStar = DatabaseMiddleWare.checkStarForRepo(repId=self.MyRepo["id"],
                                                      userId=Utils.UserManager.getCurrentUser()["id"])

        print(str(hasStar))
        if hasStar is None :
            DatabaseMiddleWare.giveStarToRepository(repId=self.MyRepo["id"] ,userId=Utils.UserManager.getCurrentUser()["id"])
            print("giving star")
        else :
            DatabaseMiddleWare.takeStarFromRepository(repId=self.MyRepo["id"] ,userId=Utils.UserManager.getCurrentUser()["id"])
            print("unStar")
        self.updateStar()

    def updateStar(self):
        starCount = DatabaseMiddleWare.getStarCount(self.repositoryId)
        self.page_document.findAll("#StarCount").at(0).setPlainText(str(starCount["stars"]))
        hasStar = DatabaseMiddleWare.checkStarForRepo(repId=self.MyRepo["id"],
                                                      userId=Utils.UserManager.getCurrentUser()["id"])
        if hasStar is None:
            self.page_document.findAll("#StarButton").at(0).setPlainText("Star")
        else:
            self.page_document.findAll("#StarButton").at(0).setPlainText("Un-Star")

    def back(self):
        back=Utils.UIHelper.backPressHandler(BACK_WIDGET,self.WINDOW_PARENT)
        self.WINDOW_PARENT.setCentralWidget(back)

    def addAnswer(self):
        ad=AddAnswerForm(self,self.WINDOW_PARENT)
        ad.show()
    def addIssue(self):
        ai=AddIssueForm(self,self.WINDOW_PARENT)
        ai.show()
    def commit(self):
        c=CommitForm(self,self.WINDOW_PARENT)
        c.show()



class AddAnswerForm(QDialog):
    def __init__(self, main,parent=None):
        self.WINDOW_PARENT=parent
        self.main=main
        super(AddAnswerForm, self).__init__(parent)
        self.setWindowTitle("Add Answer")
        self.view=QWebView(self)
        self.view.linkClicked.connect(self.handleLinkClicked)
        self.page = self.view.page()
        self.view.setMinimumSize(400, 400)
        self.view.setMaximumSize(400, 400)
        self.view.page().setLinkDelegationPolicy(
            QtWebKit.QWebPage.DelegateAllLinks)
        cwd = os.getcwd()
        self.view.load(QUrl.fromLocalFile(os.path.join(cwd, "resource", "AddAnswer.html")))
        self.WINDOW_PARENT.QApplicationRef.processEvents()
        self.view.show()
        self.setStyleSheet("border-width: 0px; border-style: solid")
        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

    def handleLinkClicked(self, url):
        action=url.toString()
        if action.__contains__("answer"):
            frame = self.view.page().mainFrame()
            document = frame.documentElement()
            try:
                self.title = document.findAll("#title").at(0).toPlainText()
                self.answer = document.findAll("#answer").at(0).toPlainText()
                self.addAnswer()
                self.close()

            except:
                document.findAll("#Respond").at(0).setPlainText("Enter your email please")
    def addAnswer(self):
        DatabaseMiddleWare.addAnswer(Utils.UserManager.getCurrentUser()["id"],self.main.issue_id,str(self.title),str(self.answer))
        self.main.selectIssue(self.main.issue_id)

class AddIssueForm(QDialog):
    def __init__(self, main,parent=None):
        self.WINDOW_PARENT=parent
        self.main=main
        super(AddIssueForm, self).__init__(parent)
        self.setWindowTitle("Add Issue")
        self.view=QWebView(self)
        self.view.linkClicked.connect(self.handleLinkClicked)
        self.page = self.view.page()
        self.view.setMinimumSize(400, 400)
        self.view.setMaximumSize(400, 400)
        self.view.page().setLinkDelegationPolicy(
            QtWebKit.QWebPage.DelegateAllLinks)
        cwd = os.getcwd()
        self.view.load(QUrl.fromLocalFile(os.path.join(cwd, "resource", "AddIssue.html")))
        self.WINDOW_PARENT.QApplicationRef.processEvents()
        self.view.show()
        self.setStyleSheet("border-width: 0px; border-style: solid")

    def handleLinkClicked(self, url):
        action=url.toString()
        if action.__contains__("issue"):
            frame = self.view.page().mainFrame()
            document = frame.documentElement()
            try:
                self.title = document.findAll("#title").at(0).toPlainText()
                self.desc = document.findAll("#desc").at(0).toPlainText()
                self.addIssue()
                self.close()
            except Exception as e:
                print("exception "+str(e))
    def addIssue(self):
        DatabaseMiddleWare.addIssue(self.title,self.desc,self.main.repositoryId,Utils.UserManager.getCurrentUser()['id'])
        allIssues = DatabaseMiddleWare.fetchIssuesForRepo(self.main.repositoryId)
        issueHtml = self.main.createIssueList(allIssues)
        self.main.page_document.findAll("#IssueList").at(0).setInnerXml(issueHtml)

class CommitForm(QDialog):
    def __init__(self, main,parent=None):
        self.WINDOW_PARENT=parent
        self.main=main
        super(CommitForm, self).__init__(parent)
        self.setWindowTitle("commit")
        self.view=QWebView(self)
        self.view.linkClicked.connect(self.handleLinkClicked)
        self.page = self.view.page()
        self.view.setMinimumSize(400, 400)
        self.view.setMaximumSize(400, 400)
        self.view.page().setLinkDelegationPolicy(
            QtWebKit.QWebPage.DelegateAllLinks)
        cwd = os.getcwd()
        self.view.load(QUrl.fromLocalFile(os.path.join(cwd, "resource", "commit.html")))
        self.WINDOW_PARENT.QApplicationRef.processEvents()
        self.view.show()
        self.setStyleSheet("border-width: 0px; border-style: solid")

    def handleLinkClicked(self, url):
        action=url.toString()
        if action.__contains__("commit"):
            frame = self.view.page().mainFrame()
            document = frame.documentElement()
            try:
                self.title = document.findAll("#title").at(0).toPlainText()
                self.desc = document.findAll("#desc").at(0).toPlainText()
                self.commit(self.main.repositoryId,Utils.UserManager.getCurrentUser()['id'],self.title,self.desc)
                self.close()
            except Exception as e:
                print("exception "+str(e))
    def commit(self,rep_id,user_id,title,desc):
        DatabaseMiddleWare.addCommit(rep_id,user_id,title,desc)





