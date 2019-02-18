import sys
import time
import numpy as np
from scipy import fftpack 
from PIL import Image
import qimage2ndarray
import matplotlib.pyplot as plt
import cv2
from PyQt5 import QtGui, QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QMessageBox, QProgressBar, QLineEdit
from PyQt5.QtCore import QRect, QThread, Qt, pyqtSignal, QObject, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
import os
import threading
from queue import Queue
class Window(QMainWindow,QObject):
    increment_value = pyqtSignal()
    decrement_value = pyqtSignal()
    text_changed = pyqtSignal()
    #event = threading.Event()
    def __init__(self):
        super(Window, self).__init__()
        #self.event = threading.Event()
        self.setGeometry(50, 50, 900, 700)
        self.setWindowTitle("Dummy Task...SERIOUSLY")
        self.setWindowIcon(QtGui.QIcon("baby.jpg"))
        self.image = None
        self.imageColor = None
        self.filename = None
        self.value = None
        self.increment = 0
        self.decrement = 100
        self.increment_value.connect(self.increment_progress)
        self.decrement_value.connect(self.decrement_progress)
        self.text_changed.connect(self.update_i)
        
        
        self.btnT = QPushButton("Fourier Transform", self)
        self.btnT.setGeometry(QRect(0,50,100,30))
        self.btnT.clicked.connect(self.img_processing)
        self.btnP = QPushButton("Pause", self)
        self.btnP.setGeometry(QRect(0,200,100,30))
        self.btnP.setEnabled(False)
        #btnP.clicked.connect()
        self.btnB = QPushButton("Browse Image", self)
        self.btnB.setGeometry(QRect(0,100,100,30))
        self.btnB.setIcon(QtGui.QIcon("browse.png"))
        self.btnB.clicked.connect(self.getimage)
        self.button = QPushButton('Show text', self)
        self.button.move(70,200)
        self.button.clicked.connect(self.insertNumber)
        
        self.textbox = QLineEdit(self)
        self.textbox.move(70, 150)
        self.textbox.resize(280,40)
        
        extractAction = QtWidgets.QAction("&Browse Image", self)
        extractAction.setShortcut("Ctrl+B")
        extractAction.triggered.connect(self.getimage)

        extractAction1 = QtWidgets.QAction("&Close Application", self)
        extractAction1.setShortcut("Ctrl+Q")
        extractAction1.triggered.connect(self.closeApp)

        extractAction2 = QtWidgets.QAction("&Fourier Transform", self)
        extractAction2.setShortcut("Ctrl+T")
        extractAction2.triggered.connect(self.img_processing)

        #extractAction2 = QtWidgets.QAction("&Continue/Pause", self)
        #extractAction2.setShortcut("Ctrl+P")
        #extractAction2.triggered.connect(self.cont_pause)

        self.labelImage1 = QtWidgets.QLabel(self)
        self.labelImage1.setGeometry(QRect(80, 0, 128, 128))
        self.labelImage2 = QtWidgets.QLabel(self)
        self.labelImage2.setGeometry(QRect(80, 250, 128, 128))
        self.labelImage3 = QtWidgets.QLabel(self)
        self.labelImage3.setGeometry(QRect(200, 250, 128, 128))
        
        self.progress = QProgressBar(self)
        self.progress.setGeometry(200,500,400,80)
        #t2 = threading.Thread(target = self.update_progress, name = 'T2', args =(self.value,))
        #t2.start()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(extractAction)
        fileMenu.addAction(extractAction1)
        fileMenu.addAction(extractAction2)

        self.show()

    def insertNumber(self):

        try:
            self.text_changed.emit()
            print(int(self.textbox.text()))
            #self.value = int(self.textbox.text())
            if 128 % self.value == 0:
                #self.event.clear()
                self.displayImage(1)
                #self.event.set()
            else:
                msgbox = QMessageBox()
                msgbox.setIcon(QMessageBox.Warning)
                msgbox.setWindowTitle('WARNING')
                msgbox.setText('The Number Is Invalid!!!!')
                msgbox.setStandardButtons(QMessageBox.Ok)
                msgbox.exec_()      
        except:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Warning)
            msgbox.setWindowTitle('WARNING')
            msgbox.setText('Please Insert Integers Only!!!!')
            msgbox.setStandardButtons(QMessageBox.Ok)
            msgbox.exec_()
            
    #def update_progress(self):
        #global i, i_lock
        #self.event.wait()
        #self.progress.setValue(50)
        
    def closeApp(self):
        sys.exit()
        
    def loadimage(self, filename):
        self.imageColor = cv2.imread(filename, -1)
        self.image = cv2.cvtColor(self.imageColor, cv2.COLOR_BGR2GRAY)
        h, w = self.image.shape
        #bytesPerLine = 3 * w
        qimg = QImage(self.image.data, w, h, QImage.Format_Grayscale8).rgbSwapped()
        self.labelImage2.setPixmap(QPixmap.fromImage(qimg))
        self.labelImage2.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        
    def img_processing(self, value):
        #self.event.wait()
        if self.filename:
            f = np.fft.fft2(self.image)
            fshift = np.fft.fftshift(f)
            magnitude_spectrum = 20*np.log(np.abs(fshift))
            yourQImage=qimage2ndarray.array2qimage(magnitude_spectrum)
            pixmap = QPixmap(QPixmap.fromImage(yourQImage))
            image = pixmap.scaled(pixmap.width(), pixmap.height())
            self.labelImage3.setScaledContents(True)
            self.labelImage3.setPixmap(image)
            for i in range(int(128 /(2*self.value))+1):
                #self.event.clear()
                magnitude_spectrum[:(i*self.value)+self.value,:] = 0
                magnitude_spectrum[:,:(i*self.value)+self.value] = 0
                magnitude_spectrum[128-((i*self.value)+self.value):,:] = 0
                magnitude_spectrum[:,128-((i*self.value)+self.value):] = 0
                fshift[:(i*self.value)+self.value,:] = 0
                fshift[:,:(i*self.value)+self.value] = 0
                fshift[128-((i*self.value)+self.value):,:] = 0
                fshift[:,128-((i*self.value)+self.value):] = 0
                #cv2.imshow('image', self.image)
                #cv2.waitKey(0)
                #cv2.destroyAllWindows()
                time.sleep(0.1)
                #(type(self.image))
                yourQImage=qimage2ndarray.array2qimage(magnitude_spectrum)
                pixmap = QPixmap(QPixmap.fromImage(yourQImage))
                image = pixmap.scaled(pixmap.width(), pixmap.height())
                self.labelImage3.setScaledContents(True)
                self.labelImage3.setPixmap(image)
                f_ishift = np.fft.ifftshift(fshift) 
                img_back = np.fft.ifft2(f_ishift)
                img_back = np.abs(img_back)
                yourImage=qimage2ndarray.array2qimage(img_back)
                pix = QPixmap(QPixmap.fromImage(yourImage))
                img = pix.scaled(pix.width(), pix.height())
                self.labelImage2.setScaledContents(True)
                self.labelImage2.setPixmap(img)
                #self.update_value.connect(update_progress)
                self.increment = int((100/(128/(2*self.value)))*i)
                #print('h')
                self.increment_value.emit()
            time.sleep(0.5)
            f = np.fft.fft2(self.image)
            fshift = np.fft.fftshift(f)
            magnitude_spectrum = 20*np.log(np.abs(fshift))
            yourQImage=qimage2ndarray.array2qimage(magnitude_spectrum)
            pixmap = QPixmap(QPixmap.fromImage(yourQImage))
            image = pixmap.scaled(pixmap.width(), pixmap.height())
            self.labelImage3.setScaledContents(True)
            self.labelImage3.setPixmap(image)
            time.sleep(0.5)
            x = 64 + self.value
            j = 63 - self.value + 1
            while j > -(self.value):
                magnitude_spectrum[j:x, j:x] = 0
                fshift[j:x, j:x] = 0
                time.sleep(0.1)
                yourQImage=qimage2ndarray.array2qimage(magnitude_spectrum)
                pixmap = QPixmap(QPixmap.fromImage(yourQImage))
                image = pixmap.scaled(pixmap.width(), pixmap.height())
                self.labelImage3.setScaledContents(True)
                self.labelImage3.setPixmap(image)
                # shift back (we shifted the center before)
                f_ishift = np.fft.ifftshift(fshift)
                # inverse fft to get the image back 
                img_back = np.fft.ifft2(f_ishift)
                img_back = np.abs(img_back)
                yourQImage=qimage2ndarray.array2qimage(img_back)
                pixmap = QPixmap(QPixmap.fromImage(yourQImage))
                img = pixmap.scaled(pixmap.width(), pixmap.height())
                self.labelImage2.setScaledContents(True)
                self.labelImage2.setPixmap(img)
                #self.Display(pixmap, self.ui.lbImg)
                self.decrement = int((100/(128/(2*self.value)))*(j+self.value))
                self.decrement_value.emit()
                x = x + self.value
                j = j - self.value
        
            self.img_processing(self.value)
        else:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Warning)
            msgbox.setWindowTitle('WARNING')
            msgbox.setText('There is no Image!!!!')
            msgbox.setStandardButtons(QMessageBox.Ok)
            msgbox.exec_()

    def displayImage(self, window):
        qformat = QImage.Format_Indexed8
        if len(self.image.shape)==3:
            if(self.image.shape[2])==4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(self.image, self.image.shape[1], self.image.shape[0], self.image.strides[0],qformat)
        img = img.rgbSwapped()
        if window== 1:
            self.labelImage3.setPixmap(QPixmap.fromImage(img))
            self.labelImage3.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            #self.update_value.connect(self.update_progress)
            t1 = threading.Thread(target = self.img_processing, name = 'T1', args =(self.value,))
            #t2 = threading.Thread(target = self.update_progress, name = 'T2', args =(self.value,))
            t1.start()
            #t2.start()
        
        
    def getimage(self):
         self.filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file','',"Image files (*.jpg *.png *jpeg)")
         if self.filename:
             self.loadimage(self.filename)
             print(type(self.filename))
             self.img = QImage(self.filename)
             print(QImage.size(self.img))
             wid = QImage.width(self.img)
             hei = QImage.height(self.img)
             if wid == 128 and hei == 128:
                 pixmap = QPixmap(QPixmap.fromImage(self.img))
                 pixmap = pixmap.scaled(self.img.width(), self.img.height(), QtCore.Qt.KeepAspectRatio)
                 self.labelImage1.setPixmap(pixmap)
                 #print('d')
                 #self.labelImage2.setPixmap(pixmap)
                 
             else:
                 msgbox = QMessageBox()
                 msgbox.setIcon(QMessageBox.Warning)
                 msgbox.setWindowTitle('WARNING')
                 msgbox.setText('Only images of size 128x128 allowed!!!!')
                 msgbox.setStandardButtons(QMessageBox.Ok)
                 msgbox.exec_()
        
    def editor(self):
        self.textEdit = QtGui.QTextEdit()
        self.setCentralWidget(self.textEdit)
        
    @pyqtSlot()       
    def increment_progress(self):
        self.progress.setValue(self.increment)

    @pyqtSlot()       
    def decrement_progress(self):
        self.progress.setValue(self.decrement)

    @pyqtSlot()       
    def update_i(self):
        self.value = int(self.textbox.text())
    
                
def main():
    app = QtWidgets.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())
    
main()

