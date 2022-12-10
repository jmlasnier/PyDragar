
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QThreadPool
from PyQt5.QtGui import QMovie, QFont,QPixmap, QIcon
import sys
import tkinter as tk
tk.Tk().withdraw()
# import db_queries


############

class MyWindow(QMainWindow):
    xpos = 200
    ypos = 500
    width = 1200
    height = 600
    file_path = ""
    folder_path = ""
    fileName = ""
    isReleased = 0
    isFolder = None
    filesInFolder = []
    backEnd_Feedback_Message = None


    def __init__(self):
        super(MyWindow, self).__init__()

        self.setGeometry(self.xpos,self.ypos, self.width, self.height)

        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        self.setWindowTitle("Dragar Admin")
        self.setWindowIcon(QIcon("soccer.png"))
        self.initUI()
        
        # self.fillReleasedTable()

    def initUI(self):
        w = QtWidgets.QWidget()
        self.setCentralWidget(w)
        grid = QtWidgets.QGridLayout(w)

        self.setFont(QFont('Arial', 18))

        ###LABELS
        self.lempty = QtWidgets.QLabel(self)
        self.lempty.setText("")
        self.lempty.adjustSize()
        self.lempty.move(50,50)

        bigpixmap = QPixmap("soccer.png")
        self.pixmap = bigpixmap.scaled(int(self.width/3), int(self.height/3), Qt.KeepAspectRatio, Qt.FastTransformation)
        self.llogo = QtWidgets.QLabel(self)
        self.llogo.setPixmap(self.pixmap)
        self.llogo.adjustSize()
        self.llogo.move(50,50)
        # Optional, resize label to image size
        self.llogo.resize(self.pixmap.width(),
                          self.pixmap.height())


        ###BUTTONS
        self.lPyDragar = QtWidgets.QLabel(self)
        self.lPyDragar.setText("PyDragar")
        self.lPyDragar.adjustSize()
        self.lPyDragar.setFont(QFont('Arial', 12))

        self.bAchat = QtWidgets.QPushButton(self)
        self.bAchat.setText("Achat")
        self.bAchat.adjustSize()
        self.bAchat.clicked.connect(self.achat_OnClick)

        
        self.bSoumission = QtWidgets.QPushButton(self)
        self.bSoumission.setText("bSoumission")
        self.bSoumission.adjustSize()
        self.bSoumission.clicked.connect(self.soumission_OnClick)

        self.bShippingLabel = QtWidgets.QPushButton(self)
        self.bShippingLabel.setText("ShippingLabel")
        self.bShippingLabel.adjustSize()
        self.bShippingLabel.clicked.connect(self.label_onClick)


        mainW = QtWidgets.QWidget()
        layout = QVBoxLayout()
        mainW.setLayout(layout)
        self.setCentralWidget(mainW)


        layout.addWidget(self.llogo)
        layout.addWidget(self.lPyDragar)
        layout.addWidget(self.bAchat)
        layout.addWidget(self.bSoumission)
        layout.addWidget(self.bShippingLabel)
        layout.addStretch()

   
        

### Clicked functi

    def achat_OnClick(self):
        print("achat")

    def soumission_OnClick(self):
        print("soumission")

    def label_onClick(self):
        print("label")
        text, ok = QInputDialog.getText(self, "Input", "Enter security digits")
        print("Text: ", text)
        print("Ok: ", ok)

    def update(self):
        self.lFileName.adjustSize()



def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())


window()