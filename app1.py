import sys

from PyQt5.QtWidgets import QApplication
from Main import Main

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
