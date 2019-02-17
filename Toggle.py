
from PyQt5.QtWidgets import (QPushButton , QApplication)

import sys

class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):      

        self.col = QColor(0, 0, 0)       

        toggler = QPushButton('Pause', self)
        toggler.setCheckable(True)
        toggler.move(10, 10)
        self.show()
        
        
    def yourfunction(self, pressed):  #Ekteb el functin elly 3ayzha t7sa lw el button pressed
        
        source = self.sender()
        
     if pressed:
            #El Event elly hy3ml pause (ex: event2.clear)
       else:
            #event.set>>>> 3shan y continue
                        
       
       
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
