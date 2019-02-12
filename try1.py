#!/usr/local/bin/python
# by Daniel Rosengren, modified by e-satis
"""
Module doctring
"""
import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolTip, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPixmap, QImage
class Window(QMainWindow):
    """window class"""
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.title = "First Window"
        self.top = 100
        self.left = 100
        self.width = 680
        self.height = 500
        self.init_window()
    def init_window(self):
        """initialize window"""
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.labelImage = QLabel(self)
        btn = QPushButton("Browse", self)
        btn.setGeometry(QRect(80, 80, 150, 80)) #top,left,width,height
        self.labelImage.setGeometry(QRect(80, 250, 128, 128))
        btn.setIcon(QtGui.QIcon("browsing.png"))
        btn.setIconSize(QtCore.QSize(40, 40))
        btn.setToolTip("Browse for image")
        btn.clicked.connect(self.ButtonAction)
        self.show()
    def ButtonAction(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file','',"Image files (*.jpg *.png *jpeg)")
        if filename:
            self.img = QImage(filename)
            print(QImage.size(self.img))
            wid = QImage.width(self.img)
            hei = QImage.height(self.img)
            if wid == 128 and hei == 128:
                pixmap = QPixmap(QPixmap.fromImage(self.img))
                pixmap = pixmap.scaled(self.img.width(), self.img.height(), QtCore.Qt.KeepAspectRatio)
                self.labelImage.setPixmap(pixmap)
            else:
                msgbox = QMessageBox()
                msgbox.setIcon(QMessageBox.Warning)
                msgbox.setWindowTitle('WARNING')
                msgbox.setText('Only images of size 128x128 allowed!!!!')
                msgbox.setStandardButtons(QMessageBox.Ok)
                msgbox.exec_()
APP = QApplication(sys.argv)
WIND = Window()
sys.exit(APP.exec())
