from decimal import Decimal
from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem
from sys import exit, argv

#  myappid = 'fantozzi.worldcrumble.1.0'                            #  Currently not needed
#  windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)  #  Currently not needed
qtcreator_file = "mainwindow.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)

class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setWindowTitle('World Crumbler')
        self.setFixedSize(1000, 640)
        self.setupUi(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(argv)
    window = MyWindow()
    window.show()
    exit(app.exec_())