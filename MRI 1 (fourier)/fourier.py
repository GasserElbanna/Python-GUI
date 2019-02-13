from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMessageBox
from fourierUI import Ui_MainWindow
import sys
from PIL import Image

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setMinimumSize(500,650)
        self.ui.btnBrowse.clicked.connect(self.Browse)
    def Browse(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '', "Image files (*.jpg *.png *jpeg)")
        try:
            img = Image.open(filename)
            img.verify()
        except (IOError, SyntaxError):
            fileError = QMessageBox()
            fileError.setIcon(QMessageBox.Warning)
            fileError.setWindowTitle('WARNING')
            fileError.setText('There is a problem with the file (corrupt)!!!!')
            fileError.setStandardButtons(QMessageBox.Ok)
            fileError.exec_()
        else:
            if filename:
                pixmap = QPixmap(filename)
                wid = QPixmap.width(pixmap)
                hei = QPixmap.height(pixmap)
                if wid == 128 and hei == 128:
                    pixmap = pixmap.scaled(pixmap.width(), pixmap.height())
                    self.ui.lbFixedImg.setScaledContents(True)
                    self.ui.lbFixedImg.setPixmap(pixmap)
                else:
                    sizeError = QMessageBox()
                    sizeError.setIcon(QMessageBox.Warning)
                    sizeError.setWindowTitle('WARNING')
                    sizeError.setText('Only images of size 128x128 allowed!!!!')
                    sizeError.setStandardButtons(QMessageBox.Ok)
                    sizeError.exec_()
def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()


if __name__ == "__main__":
    main()