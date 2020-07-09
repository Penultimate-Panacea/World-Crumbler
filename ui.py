from PyQt5 import QtGui, QtWidgets, uic
from sys import exit, argv
import tmap_gets

# myappid = 'fantozzi.worldcrumble.1.0'                            #  Currently not needed
# windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)  #  Currently not needed
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
        self.sectorName = "Test Sector Name"
        self.worldName = "Test World Name"
        self.hexagon = 9999
        self.dice_seed = None
        self.secondSurveyUwp = ['X', '0', '0', '0', '0', '0', '0', '0']
        self.hardTimesUwp = ['X', '0', '0', '0', '0', '0', '0', '0']
        self.ManualInputPushButton.clicked.connect(self.manual_uwp)
        self.TravellerMapGetPlanet.clicked.connect(self.api_uwp)
        self.CrumbleStage_1.clicked.connect(self.crumble1)
        self.CrumbleStage_2.clicked.connect(self.crumble2)
        self.CrumbleStage_3.clicked.connect(self.crumble3)
        self.CrumbleStage_4.clicked.connect(self.crumble4)
        self.CrumbleStage_5.clicked.connect(self.crumble5)
        self.CrumbleStage_6.clicked.connect(self.crumble6)
        self.CrumbleStage_7.clicked.connect(self.crumble7)
        self.CrumbleStage_8.clicked.connect(self.crumble8)
        self.CrumbleStage_9.clicked.connect(self.crumble9)
        self.CrumbleStage_10.clicked.connect(self.crumble10)
        self.AutoCrumble.clicked.connect(self.auto_crumble)

    def manual_uwp(self):
        self.secondSurveyUwp[0] = self.OriginalStarportInput.currentText()
        self.secondSurveyUwp[1] = self.OriginalSizeInput.currentText()
        self.secondSurveyUwp[2] = self.OriginalAtmosphereInput.currentText()
        self.secondSurveyUwp[3] = self.OriginalHydrosphereInput.currentText()
        self.secondSurveyUwp[4] = self.OriginalPopulationInput.currentText()
        self.secondSurveyUwp[5] = self.OriginalGovernmentInput.currentText()
        self.secondSurveyUwp[6] = self.OriginalLawInput.currentText()
        self.secondSurveyUwp[7] = self.OriginalTechInput.currentText()
        self.sectorName = self.SectorNameInput.currentText()
        self.worldName = self.PlanetManualInput.text()
        self.dice_seed = self.sectorName+self.worldName
        self.hardTimesUwp = self.secondSurveyUwp

    def api_uwp(self):
        self.sectorName = self.TravellerMapSector.currentText()
        self.hexagon = self.TravellerMapHex.text()  # TODO hex validator
        world = tmap_gets.get_json(self.sectorName, self.hexagon)
        uwp_returned = world["WorldUwp"]
        uwp_string = uwp_returned.replace('-', '')
        i = 0
        for char in uwp_string:
            self.secondSurveyUwp[i] = char
            i += 1
        print(self.secondSurveyUwp)
        world_string = "Sector:" + world["SectorName"] + "\nSubsector:" + world["SubsectorName"] + "\nWorld:" + \
                       world["WorldName"] + "\nUWP:" + uwp_returned
        self.ReturnedAPILabel.setText(world_string)
        self.dice_seed = self.sectorName + self.worldName
        self.hardTimesUwp = self.secondSurveyUwp


if __name__ == "__main__":
    app = QtWidgets.QApplication(argv)
    window = MyWindow()
    window.show()
    exit(app.exec_())
