from PyQt5.QtWidgets import QWidget, QLabel, QPushButton
from PyQt5.QtGui import QFont

from SODEW import SODEW

class Main(QWidget):
    def __init__(self):
        try:
            super(QWidget, self).__init__()
            self.setWindowTitle('Main')
            self.setFixedSize(400, 150)
            self.font = QFont()
            self.font.setPixelSize(20)

            self.welcome = QLabel(self)
            self.welcome.setText('Time-varying linear systems analyser')
            self.welcome.setFont(self.font)
            self.welcome.move(30,50)

            self.btn1 = QPushButton(self)
            self.btn1.setText('Start')
            self.btn1.move(75,100)
            self.btn1.clicked.connect(self.start1_btn)

            self.btn2 = QPushButton(self)
            self.btn2.setText('Exit')
            self.btn2.move(250,100)
            self.btn2.clicked.connect(self.exit_btn)

            self.sodew = None
        except Exception as e:
            print(e)
            pass

    def start1_btn(self):
        try:
            if self.sodew != None:
                self.sodew.closew()
            self.sodew = SODEW()
            self.sodew.show()
        except Exception as e:
            print(e)
            pass

    def exit_btn(self):
        #self.conn.close()
        self.closew()

    def closew(self):
        if self.sodew != None:
            self.sodew.closew()
        self.close()
        self.destroy()
