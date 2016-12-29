from PySide import *
from PySide import QtGui
from PySide import QtCore

class Styles:
    # colors
    COLOR_Light_Blue= "rgba(0, 204, 255, 255)"
    COLOR_Transparent="rgba(0,0,0,0)"

    # Styles
    STYLE_QLable="QLabel { color: rgb(50, 50, 50); font-size: 11px; background-color: rgba(0, 204, 255, 255); border: 1px solid rgba(188, 188, 188, 250);}"
    STYLE_QPushButton="QPushButton { background: #ffffff ;border-radius: 4px;font-family: Arial;color: #999999;font-size: 20px;padding: 10px 20px 10px 20px;text-decoration: none;} QPushButton:hover {background: rgba(250,250,250,255); color:rgba(29,185,84,255);text-decoration: none;}"
    STYLE_QEditText="QTextEdit, QListView {background-color: white; border-radius: 4px;border: 1px solid #e5e5e5; background-image: url(draft.png); background-attachment: fixed;}"

    def getLableStyle(backgroundColor):
        return Styles.STYLE_QLable.replace("background-color: rgba(0, 204, 255, 255)","background-color: "+backgroundColor)

    def getButtonStyle(normal,hoverd):
        return Styles.STYLE_QPushButton.replace("background: #ffffff","background: "+normal).replace("background: rgba(250,250,250,255)","background: "+hoverd)

def createPushButton(str,self,posX,posY,action):
    btn=QtGui.QPushButton(str, self)
    btn.setStyleSheet(Styles.STYLE_QPushButton)
    btn.move(posX,posY)
    btn.clicked.connect(action)
    return btn

def createEditText(str,self,posX,posY,width,height):
    edt=QtGui.QTextEdit(str,self)
    edt.setStyleSheet(Styles.STYLE_QEditText)
    edt.move(posX,posY)
    edt.setMinimumSize(width,height)
    edt.setMaximumSize(width,height)
    return edt

def createTextLable(str,self,posX,posY,color,size):
    lbl=QtGui.QLabel("<font color="+color+" size="+size+">"+str+"</font>", self)
    lbl.move(posX,posY)
    return lbl

def createLable(self,poxX,posY,width,height):
    lbl=QtGui.QLabel("", self)
    lbl.move(poxX,posY)
    lbl.setMinimumSize(width,height)
    lbl.setMaximumSize(width,height)
    lbl.setStyleSheet(Styles.STYLE_QLable)
    return lbl

def createLableColered(self,poxX,posY,width,height,color):
    lbl=QtGui.QLabel("", self)
    lbl.move(poxX,posY)
    lbl.setMinimumSize(width,height)
    lbl.setMaximumSize(width,height)
    lbl.setStyleSheet(Styles.getLableStyle(color))
    return lbl
def createBorderLessButton(str,self,posX,posY,action):
    btn=createPushButton(str,self,posX,posY,action)
    btn.setStyleSheet(Styles.getButtonStyle(Styles.COLOR_Transparent,Styles.COLOR_Transparent))
    return btn

def createBackground(self):
    return createLableColered(self,0,0,self.WINDOW_WIDTH,self.WINDOW_HEIGHT,"rgba(45,45,48,255)")

def createImage(self,poxX,posY,width,height,address):
    image_map = QtGui.QPixmap(address)

    image_map  = image_map.scaled( width, height , QtCore.Qt.KeepAspectRatio)
    lbl = createLable(self,poxX,posY,width,height )
    lbl.setPixmap(image_map)
    lbl.setStyleSheet("QLabel { background-color: rgba(0, 0, 0, 0);}")

    return lbl



