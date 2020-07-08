from decimal import Decimal
from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem
from sys import exit, argv
import tmap_gets

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
        self.secondSurveyUwp = ['X', '0', '0', '0', '0', '0', '0', '0']
        self.hardTimesUwp = ['X', '0', '0', '0', '0', '0', '0', '0']
        self.ManualInputPushButton.clicked.connect(self.manual_uwp)
        self.TravellerMapGetPlanet.clicked.connect(self.api_uwp)

    def manual_uwp(self):
        self.secondSurveyUwp[0] = self.OriginalStarportInput.currentText()
        self.secondSurveyUwp[1] = self.OriginalSizeInput.currentText()
        self.secondSurveyUwp[2] = self.OriginalAtmosphereInput.currentText()
        self.secondSurveyUwp[3] = self.OriginalHydrosphereInput.currentText()
        self.secondSurveyUwp[4] = self.OriginalPopulationInput.currentText()
        self.secondSurveyUwp[5] = self.OriginalGovernmentInput.currentText()
        self.secondSurveyUwp[6] = self.OriginalLawInput.currentText()
        self.secondSurveyUwp[7] = self.OriginalTechInput.currentText()
        print(self.secondSurveyUwp)

    def api_uwp(self):
        sector = self.TravellerMapSector.currentText()
        hexagon = self.TravellerMapHex.text()
        uwp_returned = tmap_gets.get_json(sector, hexagon)["WorldUwp"]
        uwp_string = uwp_returned.replace('-', '')
        i = 0
        for char in uwp_string:
            self.secondSurveyUwp[i] = char
            i += 1
        print(self.secondSurveyUwp)

if __name__ == "__main__":
    app = QtWidgets.QApplication(argv)
    window = MyWindow()
    window.show()
    exit(app.exec_())