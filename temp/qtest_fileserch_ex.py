from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget
import sys

class MyWindow(QApplication):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__()
        self.setObjectName("Draft_survey")
        self.resize(330, 314)
        self.sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MyWindow()
    print(mainWin, type(mainWin))
    mainWin.show()
    sys.exit(app.exec_())