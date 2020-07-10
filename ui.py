from PyQt5 import QtGui, QtWidgets, uic
from sys import exit, argv
from diceroller import DiceRoller
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
        self.historyString = ""
        self.worldName = "Test World Name"
        self.hexagon = 9999
        self.dice = DiceRoller
        self.stageThreeTLBuffer = 0
        self.secondSurveyUwp = ['X', 0, 0, 0, 0, 0, 0, 0]
        self.hardTimesUwp = ['X', 0, 0, 0, 0, 0, 0, 0]
        self.warzoneStatus = None # TODO safe, warzone, intense, black ['S', 'W', 'I', 'B']
        self.areaStatus = None  # TODO determine frontier, safe, outland, wild areas  ['F', 'S', 'O', 'W']
        self.isIsolated = False
        self.ManualInputPushButton.clicked.connect(self.manual_uwp)
        self.TravellerMapGetPlanet.clicked.connect(self.api_uwp)
        self.DataEntryButton.clicked.connect(self.finalize_input)
        self.UnlockEntryButton.clicked.connect(self.unlock_input)
        self.CrumbleWidget.setDisabled(True)
        self.CrumbleStage_1a.clicked.connect(self.crumble1a)
        self.CrumbleStage_1b.clicked.connect(self.crumble1b())

    def manual_uwp(self):
        self.secondSurveyUwp[0] = self.OriginalStarportInput.currentText()
        self.secondSurveyUwp[1] = int(self.OriginalSizeInput.currentText())
        self.secondSurveyUwp[2] = int(self.OriginalAtmosphereInput.currentText())
        self.secondSurveyUwp[3] = int(self.OriginalHydrosphereInput.currentText())
        self.secondSurveyUwp[4] = int(self.OriginalPopulationInput.currentText())
        self.secondSurveyUwp[5] = int(self.OriginalGovernmentInput.currentText())
        self.secondSurveyUwp[6] = int(self.OriginalLawInput.currentText())
        self.secondSurveyUwp[7] = int(self.OriginalTechInput.currentText())
        self.sectorName = self.SectorNameInput.currentText()
        self.worldName = self.PlanetManualInput.text()

        # TODO replace the int casts to handle conversion to hexadecimal

    def api_uwp(self):
        self.sectorName = self.TravellerMapSector.currentText()
        self.hexagon = self.TravellerMapHex.text()  # TODO hex validator
        world = tmap_gets.get_json(self.sectorName, self.hexagon)
        uwp_returned = world["WorldUwp"]
        uwp_string = uwp_returned.replace('-', '')
        i = 0
        for char in uwp_string:
            self.secondSurveyUwp[i] = int(char)  # TODO replace the int casts to handle conversion to hexadecimal
            i += 1
        print(self.secondSurveyUwp)
        world_string = "Sector:" + world["SectorName"] + "\nSubsector:" + world["SubsectorName"] + "\nWorld:" + \
                       world["WorldName"] + "\nUWP:" + uwp_returned
        self.ReturnedAPILabel.setText(world_string)

    def finalize_input(self):
        dice_seed = self.sectorName + self.worldName
        self.dice = DiceRoller(dice_seed)
        self.hardTimesUwp = self.secondSurveyUwp
        self.toolBox.setDisabled(True)
        self.CrumbleWidget.setDisabled(False)

    def unlock_input(self):
        self.toolBox.setDisabled(False)
        self.CrumbleWidget.setDisabled(True)

    def crumble1a(self):
        warzone_dicemods = {'S': 0, 'W': 1, 'I': 2, 'B': 3}
        dice_modifier = 0
        if self.secondSurveyUwp[0] == "A":
            dice_modifier += 1
        if self.secondSurveyUwp[4] > 8:
            dice_modifier += 1
        dice_modifier += warzone_dicemods[self.warzoneStatus]
        roll = self.dice.roll_2d6() + dice_modifier
        if self.warzoneStatus == 'S':
            roll = 0
        if roll > 13:
            self.historyString += "Biosphere Damage\n"
            self.hardTimesUwp[0] = "X"
            if self.warzoneStatus == 'B':
                damage_roll = self.dice.roll_2d6() + 2
            else:
                damage_roll = self.dice.roll_2d6()
            if damage_roll < 4:
                years = self.dice.roll_1d6()
                self.historyString += "Average planetary temperature decreases for the next %d years\n" % years
            elif damage_roll < 6:
                temperature_decrease = self.dice.roll_1d6()+6
                self.historyString += "Permanent planetary temperature decrease of %d Kelvin" % temperature_decrease
            elif damage_roll < 9:
                taint_shift = {5: 4, 7: 6, 9: 8}
                try:
                    self.hardTimesUwp[2] = taint_shift[self.hardTimesUwp[2]]
                except KeyError:
                    pass
                self.historyString += "Atmosphere Tainted\n"
            elif damage_roll < 11:
                taint_shift = {3: 2, 5: 4, 7: 6, 9: 8}
                self.stageThreeTLBuffer += 3
                try:
                    self.hardTimesUwp[2] = taint_shift[self.hardTimesUwp[2]]
                except KeyError:
                    pass
                self.hardTimesUwp[4] -= 1
                self.historyString += "Atmosphere Tainted, leading to population loss\n"
            elif damage_roll < 13:
                self.hardTimesUwp[2] = 12
                self.stageThreeTLBuffer += 6
                self.hardTimesUwp[4] -= 2
                self.historyString += "Atmosphere Insidious, leading to population loss\n"
            elif damage_roll >= 13:
                self.hardTimesUwp[2] = 12
                self.hardTimesUwp[4] = 0
                self.hardTimesUwp[5] = 0
                self.hardTimesUwp[6] = 0
                self.hardTimesUwp[7] = 0
                self.historyString += "World Annihilated\n"

    def crumble1b(self):
        if self.secondSurveyUwp[0] == 'A':
            self.crumble1b_mode_a()
        elif self.secondSurveyUwp[0] == 'B':
            self.crumble1b_mode_b()
        elif self.secondSurveyUwp[0] == 'C':
            self.crumble1b_mode_c()
        elif self.secondSurveyUwp[0] == 'D':
            self.crumble1b_mode()
        else:
            self.hardTimesUwp[0] = self.secondSurveyUwp[0]

    def crumble1b_mode_a(self):
        dicemod = 0
        if self.areaStatus == 'F':
            dicemod += 2
        elif self.areaStatus == 'O' or 'W':
            dicemod += 3
        if self.warzoneStatus == 'W':
            dicemod += 1
        elif self.warzoneStatus == 'I':
            dicemod += 2
        elif self.warzoneStatus == 'B':
            dicemod += 3
        if self.isIsolated:
            dicemod += 2
        if self.secondSurveyUwp[4] == 0 or 1 or 2:
            dicemod += 2
        elif self.secondSurveyUwp[4] == 3 or 4:
            dicemod += 1
        if self.secondSurveyUwp[7] == 0 or 1 or 2 or 3 or 4:
            dicemod += 8
        elif self.secondSurveyUwp[7] == 5 or 6:
            dicemod += 5
        elif self.secondSurveyUwp[7] == 7 or 8:
            dicemod += 3
        elif self.secondSurveyUwp[7] == 9 or 10:
            dicemod += 1
        crumble_roll = self.dice.roll_1d6() + dicemod

    def crumble1b_mode_b(self):
        dicemod = 0
        if self.areaStatus == 'O':
            dicemod += 2
        elif self.areaStatus == 'W':
            dicemod += 3
        if self.warzoneStatus == 'W':
            dicemod += 1
        elif self.warzoneStatus == 'I' or 'B':
            dicemod += 2
        if self.isIsolated:
            dicemod += 3
        if self.secondSurveyUwp[4] == 0 or 1 or 2:
            dicemod += 2
        elif self.secondSurveyUwp[4] == 3 or 4:
            dicemod += 1
        if self.secondSurveyUwp[7] == 0 or 1 or 2 or 3 or 4:
            dicemod += 7
        elif self.secondSurveyUwp[7] == 5 or 6:
            dicemod += 4
        elif self.secondSurveyUwp[7] == 7 or 8:
            dicemod += 1
        crumble_roll = self.dice.roll_1d6() + dicemod

    def crumble1b_mode_c(self):
        dicemod = 0
        if self.areaStatus == 'O':
            dicemod += 1
        elif self.areaStatus == 'W':
            dicemod += 2
        if self.warzoneStatus == 'W' or 'I':
            dicemod += 1
        elif self.warzoneStatus == 'B':
            dicemod += 2
        if self.isIsolated:
            dicemod += 4
        if self.secondSurveyUwp[4] == 0 or 1 or 2:
            dicemod += 1
        if self.secondSurveyUwp[7] == 0 or 1 or 2 or 3 or 4:
            dicemod += 5
        elif self.secondSurveyUwp[7] == 5 or 6:
            dicemod += 3
        crumble_roll = self.dice.roll_1d6() + dicemod

    def crumble1b_mode_d(self):
        dicemod = 0
        if self.areaStatus == 'W':
            dicemod += 1
        if self.warzoneStatus == 'B':
            dicemod += 1
        if self.isIsolated:
            dicemod += 1
        if self.secondSurveyUwp[7] == 0 or 1 or 2 or 3 or 4:
            dicemod += 3
        elif self.secondSurveyUwp[7] == 5 or 6:
            dicemod += 1
        crumble_roll = self.dice.roll_1d6() + dicemod

if __name__ == "__main__":
    app = QtWidgets.QApplication(argv)
    window = MyWindow()
    window.show()
    exit(app.exec_())
