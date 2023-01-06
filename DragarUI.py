import webbrowser

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QIcon
import sys
import clipboard
import googlesheet
import poste_canada
from DragarAdmin import DragarAdmin


class MyWindow(QMainWindow):
    xpos = 200
    ypos = 500
    width = 500
    height = 500
    file_path = ""
    folder_path = ""
    fileName = ""
    dragarAdmin = DragarAdmin()
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
        self.setWindowIcon(QIcon("./dg.png"))
        self.initUI()
        
        # self.fillReleasedTable()

    def initUI(self):
        w = QtWidgets.QWidget()
        self.setCentralWidget(w)
        self.setFont(QFont('Arial', 18))

        ###LABELS
        # self.lempty = QtWidgets.QLabel(self)
        # self.lempty.setText("")
        # self.lempty.adjustSize()
        # self.lempty.move(50, 50)

        bigpixmap = QPixmap("./logo.png")
        self.pixmap = bigpixmap.scaled(int(self.width), int(self.height), Qt.KeepAspectRatio, Qt.FastTransformation)
        self.llogo = QtWidgets.QLabel(self)
        self.llogo.setPixmap(self.pixmap)
        self.llogo.adjustSize()
        # self.llogo.move(50, 50)
        # Optional, resize label to image size
        self.llogo.resize(self.pixmap.width(),
                          self.pixmap.height())


        ###BUTTONS
        # self.lPyDragar = QtWidgets.QLabel(self)
        # self.lPyDragar.setText("Admin Menu")
        # self.lPyDragar.adjustSize()
        # self.lPyDragar.setFont(QFont('Arial', 12))

        self.bVente = QtWidgets.QPushButton(self)
        self.bVente.setText("Run Vente")
        # self.bVente.adjustSize()
        self.bVente.clicked.connect(self.vente_on_click)

        self.bSoumission = QtWidgets.QPushButton(self)
        self.bSoumission.setText("Run Soumission")
        # self.bSoumission.adjustSize()
        self.bSoumission.clicked.connect(self.soumission_on_click)

        self.bShippingLabel = QtWidgets.QPushButton(self)
        self.bShippingLabel.setText("Run ShippingLabel")
        # self.bShippingLabel.adjustSize()
        self.bShippingLabel.clicked.connect(self.shipping_label_on_click)

        self.bClipboardFrench = QtWidgets.QPushButton(self)
        self.bClipboardFrench.setText("Fill Clipboard French")
        # self.bClipboardFrench.adjustSize()
        self.bClipboardFrench.clicked.connect(self.french_clipboard_on_click)

        self.bClipboardEnglish = QtWidgets.QPushButton(self)
        self.bClipboardEnglish.setText("Fill Clipboard English")
        # self.bClipboardEnglish.adjustSize()
        self.bClipboardEnglish.clicked.connect(self.english_clipboard_on_click)

        self.bNewSS = QtWidgets.QPushButton(self)
        self.bNewSS.setText("New spreadsheet")
        # self.bNewSS.adjustSize()
        self.bNewSS.clicked.connect(self.new_ss_on_click)

        mainW = QtWidgets.QWidget()
        layout = QVBoxLayout()
        mainW.setLayout(layout)
        self.setCentralWidget(mainW)

        layout.addWidget(self.llogo)
        # layout.addWidget(self.lPyDragar)
        layout.addWidget(self.bNewSS)
        layout.addWidget(self.bVente)
        layout.addWidget(self.bClipboardFrench)
        layout.addWidget(self.bClipboardEnglish)
        layout.addStretch()
        layout.addWidget(self.bSoumission)
        layout.addWidget(self.bShippingLabel)
        layout.addStretch()

    # Clicked functi
    def vente_on_click(self):
        self.dragarAdmin.vente(self)
        print("vente")

    def soumission_on_click(self):
        self.dragarAdmin.soumission()
        print("soumission")

    def new_ss_on_click(self):
        new_ss_id = googlesheet.copy_source_spreadsheet()
        ss_url = 'https://docs.google.com/spreadsheets/d/' + new_ss_id
        webbrowser.open(ss_url)

    def french_clipboard_on_click(self):
        clipboard.fill_french_clipboard()
        self.bClipboardFrench.setText("Clipboard Filled in french")
        self.bClipboardFrench.setDisabled(True)

    def english_clipboard_on_click(self):
        clipboard.fill_english_clipboard()
        self.bClipboardEnglish.setText("Clipboard Filled in english")
        self.bClipboardEnglish.setDisabled(True)

    def shipping_label_on_click(self):
        # todo: disable shipping label button
        name_ship = "Jean-Michel Lasnier"
        email_ship = "guil.lvsq@gmail.com"
        adress_ship = "133 Rue Lapointe, Lachute, QC J8H 4L8"
        PO_ship = "D22091865-1"
        type_ship = "S"
        [label_path, shipping_price] = poste_canada.poste_can(email_ship, name_ship, adress_ship, PO_ship, type_ship, self)
        print('label_path: ', label_path)
        print('shipping_price: ', shipping_price)

    def update(self):
        self.lFileName.adjustSize()


def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())


window()
