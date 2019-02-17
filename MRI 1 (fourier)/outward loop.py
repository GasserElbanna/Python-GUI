import sys
from PIL import Image
from scipy import fftpack
import numpy as np
import cv2
import qimage2ndarray 
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMessageBox
from fourierUI import Ui_MainWindow
from matplotlib import pyplot as plt
from PyQt5 import QtTest
import time
class ApplicationWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(ApplicationWindow, self).__init__()
        #Setup window
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setMinimumSize(900,850)
        self.img = None
        self.imgMat = 0
        #Actions
        self.ui.btnBrowse.clicked.connect(self.Browse)
        self.ui.btnStart.clicked.connect(self.Start)
        self.ui.btnStart.setEnabled(True)
        self.ui.btnStart.setDefault(True)
        self.ui.btnToggle.setCheckable(True)
        self.ui.btnToggle.toggle()
        self.ui.btnToggle.clicked.connect(self.Btnstate)
        self.ui.nLines.valueChanged.connect(self.Valuechange)
        #Styling
        self.ui.btnToggle.setStyleSheet('QPushButton {background-color: #0F7173; color: white; font-weight: bold; font-size: 20px;}')
        self.ui.btnStart.setStyleSheet('QPushButton {background-color: #0F7173; color: white; font-weight: bold; font-size: 20px;}')
        self.ui.btnBrowse.setStyleSheet('QPushButton {background-color: #0F7173; color: white; font-weight: bold; font-size: 20px;}')
        self.ui.btnToggle.setText('Pause')
        self.ui.menubar.setStyleSheet('QMenuBar {background-color: #624763; color: #A4BAB7; font-weight: bold; font-size: 20px;}')
        self.ui.menuMenu.setStyleSheet('QMenu {background-color: #624763; color: #A4BAB7; font-weight: bold; font-size: 20px;}')
        self.ui.lbFFTimg.setStyleSheet('QLabel {background-color: white;}')        
        self.ui.lbImg.setStyleSheet('QLabel {background-color: white;}')    
        self.ui.lbFixedImg.setStyleSheet('QLabel {background-color: white;}') 
        self.ui.nLines.setStyleSheet('QSpinBox {background-color: white}')
        self.ui.lbnline.setStyleSheet('QLabel {font-weight: bold; font-size: 20px}')     
        self.setStyleSheet("background-color: #FACFAD;")

    def Browse(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(None, 'Open file', '', "Image files (*.jpg *.png *jpeg)")
        if filename:
            try:
                check = Image.open(filename)
                check.verify()
            except (IOError, SyntaxError):
                fileError = QMessageBox()
                fileError.setIcon(QMessageBox.Warning)
                fileError.setWindowTitle('WARNING')
                fileError.setText('There is a problem with the file (corrupt)!!!!')
                fileError.setStandardButtons(QMessageBox.Ok)
                fileError.exec_()
            else:
                pixmap = QPixmap(filename)
                img = QImage(filename)
                wid = QPixmap.width(pixmap)
                hei = QPixmap.height(pixmap)
                if wid == 128 and hei == 128:
                    pixmap = pixmap.scaled(pixmap.width(), pixmap.height())
                    self.imgMat = cv2.imread(filename,  cv2.IMREAD_GRAYSCALE )
                    self.img = pixmap
                    self.ui.lbFixedImg.setScaledContents(True)
                    self.ui.lbFixedImg.setPixmap(pixmap)
                    self.ui.btnStart.setEnabled(True)
                else:
                    sizeError = QMessageBox()
                    sizeError.setIcon(QMessageBox.Warning)
                    sizeError.setWindowTitle('WARNING')
                    sizeError.setText('Only images of size 128x128 allowed!!!!')
                    sizeError.setStandardButtons(QMessageBox.Ok)
                    sizeError.exec_()

    def Valuechange(self, i):
        self.ui.btnStart.setEnabled(True)

    def Btnstate(self):
        if self.ui.btnToggle.isChecked():
            self.ui.btnToggle.setText('Continue')
        else:
            self.ui.btnToggle.setText('Pause')

    def Display(self, img, cont):
        image = img.scaled(img.width(), img.height())
        cont.setScaledContents(True)
        cont.setPixmap(image)

    def Start(self):
        if self.img is None:
            noImg = QMessageBox()
            noImg.setIcon(QMessageBox.Warning)
            noImg.setWindowTitle('Notice')
            noImg.setText('Please choose an image first.')
            noImg.setStandardButtons(QMessageBox.Ok)
            noImg.exec_()
        else:
            self.Display(self.img, self.ui.lbImg)
            self.ui.btnStart.setEnabled(False)
            self.fft()

    def fft(self):
        n = self.ui.nLines.value()
        if 128 % n != 0:
            nLineError = QMessageBox()
            nLineError.setIcon(QMessageBox.Warning)
            nLineError.setWindowTitle('Notice')
            nLineError.setText('Please enter a factor of 128')
            nLineError.setStandardButtons(QMessageBox.Ok)
            nLineError.exec_()
        else:
            f = np.fft.fft2(self.imgMat)
            fshift = np.fft.fftshift(f)
            magnitude_spectrum = 20*np.log(np.abs(fshift))
            yourQImage=qimage2ndarray.array2qimage(magnitude_spectrum)
            pixmap = QPixmap(QPixmap.fromImage(yourQImage))
            self.Display(pixmap, self.ui.lbFFTimg)
            QtTest.QTest.qWait(200)
            i = 64 + n 
            j = 63 - n + 1
            while j > -n:
                magnitude_spectrum[j:i, j:i] = 0
                yourQImage=qimage2ndarray.array2qimage(magnitude_spectrum)
                pixmap = QPixmap(QPixmap.fromImage(yourQImage))
                self.Display(pixmap, self.ui.lbFFTimg)
                QtTest.QTest.qWait(50)
                # shift back (we shifted the center before)
                f_ishift = np.fft.ifftshift(magnitude_spectrum)
                # inverse fft to get the image back 
                img_back = np.fft.ifft2(f_ishift)
                img_back = np.abs(img_back)
                yourQImage=qimage2ndarray.array2qimage(img_back)
                pixmap = QPixmap(QPixmap.fromImage(yourQImage))
                self.Display(pixmap, self.ui.lbImg)
                i = i + n
                j = j - n
                QtTest.QTest.qWait(50)
            f = np.fft.fft2(self.imgMat)
            fshift = np.fft.fftshift(f)
            magnitude_spectrum = 20*np.log(np.abs(fshift))
            yourQImage=qimage2ndarray.array2qimage(magnitude_spectrum)
            pixmap = QPixmap(QPixmap.fromImage(yourQImage))
            self.Display(pixmap, self.ui.lbFFTimg)
            QtTest.QTest.qWait(200)
            for i in range(int(128 /(2*n))):
                magnitude_spectrum[:(i*n)+n,:] = 0
                magnitude_spectrum[:,:(i*n)+n] = 0
                magnitude_spectrum[128-((i*n)+n):,:] = 0
                magnitude_spectrum[:,128-((i*n)+n):] = 0
                #cv2.imshow('image', self.image)
                #cv2.waitKey(0)
                #cv2.destroyAllWindows()
                QtTest.QTest.qWait(50)
                #(type(self.image))
                yourQImage=qimage2ndarray.array2qimage(magnitude_spectrum)
                pixmap = QPixmap(QPixmap.fromImage(yourQImage))
                self.Display(pixmap, self.ui.lbFFTimg)
                f_ishift = np.fft.ifftshift(magnitude_spectrum) 
                img_back = np.fft.ifft2(f_ishift)
                img_back = np.abs(img_back)
                yourImage=qimage2ndarray.array2qimage(img_back)
                pix = QPixmap(QPixmap.fromImage(yourImage))
                self.Display(pix, self.ui.lbImg) 
#def main():


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()