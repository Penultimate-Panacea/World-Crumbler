from PyQt5 import QtGui, QtWidgets, uic
from sys import exit, argv
from diceroller import DiceRoller
import tmap_gets
import re

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
        self.stageThreeTLDrop = 0
        self.stageOnePopDrop = 0
        self.stageSixPopMultiplierDrop = 0
        self.biosphereDamage = False
        self.secondSurveyUwp = ['X', 0, 0, 0, 0, 0, 0, 0]
        self.hardTimesUwp = ['X', 0, 0, 0, 0, 0, 0, 0]
        self.warzoneStatus = 'S'  # TODO safe, warzone, intense, black ['S', 'W', 'I', 'B']
        self.areaStatus = 'S'  # TODO determine frontier, safe, outland, wild areas  ['F', 'S', 'O', 'W']
        self.isIsolated = False
        self.isFailing = False
        self.isDoomed = False
        self.ManualInputPushButton.clicked.connect(self.manual_uwp)
        self.TravellerMapGetPlanet.clicked.connect(self.api_uwp)
        self.DataEntryButton.clicked.connect(self.finalize_input)
        self.UnlockEntryButton.clicked.connect(self.unlock_input)
        self.CrumbleWidget.setDisabled(True)
        self.CrumbleStage_1a.clicked.connect(self.crumble1a)
        self.CrumbleStage_1b.clicked.connect(self.crumble1b)
        self.CrumbleStage_3.clicked.connect(self.crumble3)
        self.CrumbleStage_6a.clicked.connect(self.crumble6a)
        self.CrumbleStage_6b.clicked.connect(self.crumble6b)
        self.CrumbleStage_8.clicked.connect(self.crumble8)
        self.CrumbleStage_9.clicked.connect(self.crumble9)
        self.AutoCrumble.clicked.connect(self.auto_crumble)
        self.degrees_of_change_dict = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: -1, 6: -1, 7: -2, 8: -2, 9: -3, 10: -3, 11: -4,
                                       12: -4, 13: -5, 14: -5, 15: -6, 16: -6, 17: -7, 18: -7, 19: -8, 20: -8, 21: -9,
                                       22: -9, 23: -10, 24: -10, 25: -11, 26: -11, 27: -12, 28: -12, 29: -13, 30: -13}

    def api_isolation_check(self):
        jump2_json = tmap_gets.get_jump_json(self.sectorName, self.hexagon, 2)
        world_count = len(jump2_json["Worlds"])
        if world_count > 3:
            self.isIsolated = True
        else:
            self.isIsolated = False

    def manual_uwp(self):
        self.secondSurveyUwp[0] = self.OriginalStarportInput.currentText()
        self.secondSurveyUwp[1] = self.hex_char_convert_to_int(self.OriginalSizeInput.currentText())
        self.secondSurveyUwp[2] = self.hex_char_convert_to_int(self.OriginalAtmosphereInput.currentText())
        self.secondSurveyUwp[3] = self.hex_char_convert_to_int(self.OriginalHydrosphereInput.currentText())
        self.secondSurveyUwp[4] = self.hex_char_convert_to_int(self.OriginalPopulationInput.currentText())
        self.secondSurveyUwp[5] = self.hex_char_convert_to_int(self.OriginalGovernmentInput.currentText())
        self.secondSurveyUwp[6] = self.hex_char_convert_to_int(self.OriginalLawInput.currentText())
        self.secondSurveyUwp[7] = self.hex_char_convert_to_int(self.OriginalTechInput.currentText())
        self.sectorName = self.SectorNameInput.currentText()
        self.worldName = self.PlanetManualInput.text()
        self.isIsolated = self.IsolationCheckBox.isChecked()

    @staticmethod
    def hex_char_convert_to_int(char):
        if char == '0':
            return 0
        elif char == '1':
            return 1
        elif char == '2':
            return 2
        elif char == '3':
            return 3
        elif char == '4':
            return 4
        elif char == '5':
            return 5
        elif char == '6':
            return 6
        elif char == '7':
            return 7
        elif char == '8':
            return 8
        elif char == '9':
            return 9
        elif char == 'A':
            return 10
        elif char == 'B':
            return 11
        elif char == 'C':
            return 12
        elif char == 'D':
            return 13
        elif char == 'E':
            return 14
        elif char == 'F':
            return 15
        elif char == 'G':
            return 16
        elif char == 'H':
            return 17

    def api_uwp(self):
        self.sectorName = self.TravellerMapSector.currentText()
        self.hexagon = self.TravellerMapHex.text()  # TODO hex validator
        world = tmap_gets.get_hexagon_json(self.sectorName, self.hexagon)
        uwp_returned = world["WorldUwp"]
        uwp_string = uwp_returned.replace('-', '')
        i = 0
        for char in uwp_string:
            if i == 0:
                self.secondSurveyUwp[i] = char
            else:
                self.secondSurveyUwp[i] = self.hex_char_convert_to_int(char)
            i += 1
        print(self.secondSurveyUwp)
        world_string = "Sector:" + world["SectorName"] + "\nSubsector:" + world["SubsectorName"] + "\nWorld:" + \
                       world["WorldName"] + "\nUWP:" + uwp_returned
        self.ReturnedAPILabel.setText(world_string)
        self.api_isolation_check()

    def finalize_input(self):
        dice_seed = self.sectorName + self.worldName
        self.dice = DiceRoller(dice_seed)
        self.hardTimesUwp = self.secondSurveyUwp
        self.toolBox.setDisabled(True)
        self.CrumbleWidget.setDisabled(False)

    @staticmethod
    def uwp_to_string(uwp):
        output = ""
        for i in uwp:
            try:
                if i < 10:
                    output += str(i)
                elif i == 10:
                    output += "A"
                elif i == 11:
                    output += "B"
                elif i == 12:
                    output += "C"
                elif i == 13:
                    output += "D"
                elif i == 14:
                    output += "E"
                elif i == 15:
                    output += "F"
            except TypeError:
                output += str(i)
        return output
    
    def update_results(self):
        self.HistoryTextBrowser.setPlainText(self.historyString)
        second_survey_string = self.uwp_to_string(self.secondSurveyUwp)
        formatted_sss = second_survey_string[:7] + '-' + second_survey_string[7:]
        second_html = "<html><head/><body><p><span style=\" font-size:16pt;\">%s</span></p></body></html>" % \
                      formatted_sss
        self.SecondSurveyLabel.setText(second_html)
        hard_times_string = self.uwp_to_string(self.hardTimesUwp)
        formatted_hts = hard_times_string[:7] + '-' + hard_times_string[7:]
        second_html = "<html><head/><body><p><span style=\" font-size:16pt;\">%s</span></p></body></html>" % \
                      formatted_hts
        self.HardTimesLabel.setText(second_html)

    def unlock_input(self):
        self.toolBox.setDisabled(False)
        self.CrumbleWidget.setDisabled(True)

    def calc_pop_drop(self):
        pop_drop = self.secondSurveyUwp[4] - self.hardTimesUwp[4]
        return pop_drop

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
            self.biosphereDamage = True
            self.hardTimesUwp[0] = "X"
            if self.warzoneStatus == 'B':
                damage_roll = self.dice.roll_2d6() + 2
            else:
                damage_roll = self.dice.roll_2d6()
            if damage_roll < 4:
                years = self.dice.roll_1d6()
                self.historyString += "Average planetary temperature decreases for the next %d years\n" % years
                self.stageOnePopDrop = self.calc_pop_drop()
            elif damage_roll < 6:
                temperature_decrease = self.dice.roll_1d6() + 6
                self.historyString += "Permanent planetary temperature decrease of %d Kelvin" % temperature_decrease
                self.stageOnePopDrop = self.calc_pop_drop()
            elif damage_roll < 9:
                taint_shift = {5: 4, 7: 6, 9: 8}
                try:
                    self.hardTimesUwp[2] = taint_shift[self.hardTimesUwp[2]]
                except KeyError:
                    pass
                self.historyString += "Atmosphere Tainted\n"
                self.stageOnePopDrop = self.calc_pop_drop()
            elif damage_roll < 11:
                taint_shift = {3: 2, 5: 4, 7: 6, 9: 8}
                self.stageThreeTLBuffer += 3
                try:
                    self.hardTimesUwp[2] = taint_shift[self.hardTimesUwp[2]]
                except KeyError:
                    pass
                self.hardTimesUwp[4] -= 1
                self.historyString += "Atmosphere Tainted, leading to population loss\n"
                self.stageOnePopDrop = self.calc_pop_drop()
            elif damage_roll < 13:
                self.hardTimesUwp[2] = 12
                self.stageThreeTLBuffer += 6
                self.hardTimesUwp[4] -= 2
                self.historyString += "Atmosphere Insidious, leading to population loss\n"
                self.stageOnePopDrop = self.calc_pop_drop()
            elif damage_roll >= 13:
                self.hardTimesUwp[2] = 12
                self.hardTimesUwp[4] = 0
                self.hardTimesUwp[5] = 0
                self.hardTimesUwp[6] = 0
                self.hardTimesUwp[7] = 0
                self.historyString += "World Annihilated\n"
                self.stageOnePopDrop = self.calc_pop_drop()
        self.update_results()

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
        self.update_results()

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
        reduction = self.degrees_of_change_dict[crumble_roll]
        if reduction == -1:
            self.hardTimesUwp[0] = 'B'
            self.historyString += "The Starport fell from a class A one to a class B one\n"
        elif reduction == -2:
            self.hardTimesUwp[0] = 'C'
            self.historyString += "The Starport fell from a class A one to a class C one\n"
        elif reduction == -3:
            self.hardTimesUwp[0] = 'D'
            self.historyString += "The Starport fell from a class A one to a class D one\n"
        elif reduction == -4:
            self.hardTimesUwp[0] = 'E'
            self.historyString += "The Starport fell from a class A one to a class E one\n"
        elif reduction == 0:
            self.hardTimesUwp[0] = 'A'
        else:
            self.hardTimesUwp[0] = 'X'
            self.historyString += "The Starport fell from a class A and crumbled to nothing, not even a " \
                                  "landing beacon\n"

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
        reduction = self.degrees_of_change_dict[crumble_roll]
        if reduction == -1:
            self.hardTimesUwp[0] = 'C'
            self.historyString += "The Starport fell from a class B one to a class C one\n"
        elif reduction == -2:
            self.hardTimesUwp[0] = 'D'
            self.historyString += "The Starport fell from a class B one to a class D one\n"
        elif reduction == -3:
            self.hardTimesUwp[0] = 'E'
            self.historyString += "The Starport fell from a class B one to a class E one\n"
        elif reduction == 0:
            self.hardTimesUwp[0] = 'B'
        else:
            self.hardTimesUwp[0] = 'X'
            self.historyString += "The Starport fell from a class B and crumbled to nothing, not even a " \
                                  "landing beacon\n"

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
        reduction = self.degrees_of_change_dict[crumble_roll]
        if reduction == -1:
            self.hardTimesUwp[0] = 'D'
            self.historyString += "The Starport fell from a class C one to a class D one\n"
        elif reduction == -2:
            self.hardTimesUwp[0] = 'E'
            self.historyString += "The Starport fell from a class C one to a class E one\n"
        elif reduction == 0:
            self.hardTimesUwp[0] = 'C'
        else:
            self.hardTimesUwp[0] = 'X'
            self.historyString += "The Starport fell from a class C and crumbled to nothing, not even a " \
                                  "landing beacon\n"

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
        reduction = self.degrees_of_change_dict[crumble_roll]
        if reduction == -1:
            self.hardTimesUwp[0] = 'E'
            self.historyString += "The Starport fell from a class D one to a class E one\n"
        elif reduction == 0:
            self.hardTimesUwp[0] = 'D'
        else:
            self.hardTimesUwp[0] = 'X'
            self.historyString += "The Starport fell from a class D and crumbled to nothing, not even a landing" \
                                  " beacon\n"

    def crumble3(self):
        dicemod = 0
        if self.hardTimesUwp[0] == 'B':
            dicemod += 1
        elif self.hardTimesUwp[0] == 'C':
            dicemod += 2
        elif self.hardTimesUwp[0] == 'D':
            dicemod += 3
        elif self.hardTimesUwp[0] == 'E':
            dicemod += 4
        elif self.hardTimesUwp[0] == 'X':
            dicemod += 5
        if self.hardTimesUwp[2] < 4 or 10 or 11:
            dicemod += 1
        elif self.hardTimesUwp[2] == 12:
            dicemod += 2
        if self.hardTimesUwp[3] == 0 or 1 or 10:
            dicemod += 1
        if self.hardTimesUwp[2] > 9 and self.hardTimesUwp[3] > 1:  # Test for non-water fluid
            dicemod += 1
        if self.hardTimesUwp[4] < 5:
            dicemod += 4
        elif self.hardTimesUwp[4] == 5:
            dicemod += 2
        elif self.hardTimesUwp[4] == 6:
            dicemod += 1
        if self.hardTimesUwp[5] == 5 or 6:
            dicemod -= 1
        elif self.hardTimesUwp[5] == 0 or 2 or 3 or 7:
            dicemod += 1
        elif self.hardTimesUwp[5] > 10:
            dicemod += 1
        if self.secondSurveyUwp[7] == 1:
            dicemod -= 10
        elif self.secondSurveyUwp[7] == 2:
            dicemod -= 8
        elif self.secondSurveyUwp[7] == 3:
            dicemod -= 6
        elif self.secondSurveyUwp[7] == 4 or 5:
            dicemod -= 4
        elif self.secondSurveyUwp[7] == 6 or 7:
            dicemod -= 2
        elif self.secondSurveyUwp[7] == 10 or 11:
            dicemod += 1
        elif self.secondSurveyUwp[7] == 12 or 13:
            dicemod += 3
        elif self.secondSurveyUwp[7] == 14 or 15:
            dicemod += 5
        elif self.secondSurveyUwp[7] == 16:
            dicemod += 7
        if self.areaStatus == 'O':
            dicemod += 1
        elif self.areaStatus == 'W':
            dicemod += 3
        crumble_roll = self.dice.roll_1d6() + dicemod + self.stageThreeTLBuffer
        reduction = self.degrees_of_change_dict[crumble_roll]
        self.hardTimesUwp[7] = self.secondSurveyUwp[7] + reduction
        self.stageThreeTLDrop = abs(reduction)
        self.historyString += "The planets tech level fell from %d to %d during the recession\n" % (
            self.secondSurveyUwp[7], self.hardTimesUwp[7])
        self.update_results()

    def crumble6a(self):
        dicemod = 0
        if self.biosphereDamage:
            dicemod += 1
        if self.hardTimesUwp[2] < 2:
            dicemod += 1
        if self.hardTimesUwp[3] < 2:
            dicemod += 1
        if self.hardTimesUwp[2] > 9 and self.hardTimesUwp[3] > 2:  # Fluid
            dicemod += 1
        if self.hardTimesUwp[4] < 3:
            dicemod -= 1
        elif 6 <= self.hardTimesUwp[4] <= 8:
            dicemod += 1
        elif self.hardTimesUwp[4] > 8:
            dicemod += 2
        if self.areaStatus == 'O':
            dicemod += 1
        elif self.areaStatus == 'W':
            dicemod += 2
        a_decrease_dict = {'B': 1, 'C': 2, 'D': 3, 'E': 4, 'X': 5}
        b_decrease_dict = {'C': 1, 'D': 2, 'E': 3, 'X': 4}
        c_decrease_dict = {'D': 1, 'E': 2, 'X': 3}
        d_decrease_dict = {'E': 1, 'X': 2}
        e_decrease_dict = {'X': 1}
        x_decrease_dict = {'X': 0}
        starport_decrease_dict = {'A': a_decrease_dict, 'B': b_decrease_dict, 'C': c_decrease_dict,
                                  'D': d_decrease_dict, 'E': e_decrease_dict, 'X': x_decrease_dict}
        dicemod += starport_decrease_dict[self.secondSurveyUwp[0]][self.hardTimesUwp[0]]
        crumble_roll = self.dice.roll_1d6() + dicemod
        reduction = self.degrees_of_change_dict[crumble_roll]
        increase = abs(reduction)  # Law level increases for visitors
        self.hardTimesUwp[6] += increase
        self.historyString += "The society became more xenophobic, with the law level for visitors increasing to %d " \
                              "from %d\n" % (increase, self.secondSurveyUwp[6])
        self.update_results()

    def crumble6b(self):
        dicemod = 0
        if self.hardTimesUwp[2] == 5 or 6 or 8:
            dicemod += 1
        if self.hardTimesUwp[3] > 2 and self.hardTimesUwp[2] < 10:
            dicemod += 1
        if self.hardTimesUwp[7] < 5:
            dicemod += 7
        elif self.hardTimesUwp[7] == 5:
            dicemod += 3
        elif self.hardTimesUwp[7] == 6:
            dicemod += 2
        elif self.hardTimesUwp[7] == 7:
            dicemod += 1
        if self.hardTimesUwp[0] == 'A':
            dicemod -= 5
        elif self.hardTimesUwp[0] == 'B':
            dicemod -= 4
        elif self.hardTimesUwp[0] == 'C':
            dicemod -= 2
        elif self.hardTimesUwp[0] == 'D':
            dicemod -= 1
        crumble_roll = self.dice.roll_2d6() + dicemod
        if crumble_roll > 10:
            self.historyString += "The world has fallen into xenophobia and isolationism, it must have a double " \
                                  "standard law level for visitors.\n"
        else:
            self.historyString += "The world has not fallen into abject isolationism, a double standard law level is" \
                                  " at the Referee's discretion\n"
        self.update_results()

    def crumble8(self):
        tech_band = [self.crumble8_tech_band_1(), self.crumble8_tech_band_1(), self.crumble8_tech_band_1(),
                     self.crumble8_tech_band_2(), self.crumble8_tech_band_3(), self.crumble8_tech_band_4(),
                     self.crumble8_tech_band_4(), self.crumble8_tech_band_5(), self.crumble8_tech_band_5()]
        try:
            enivronmental_dicemod = tech_band[self.hardTimesUwp[7]]
        except IndexError:
            enivronmental_dicemod = 0
        if enivronmental_dicemod > 4:
            self.isDoomed = True
        elif enivronmental_dicemod > 1:
            self.isFailing = True
        pop_band = [self.crumble8_pop_band_1(), self.crumble8_pop_band_1(), self.crumble8_pop_band_1(),
                    self.crumble8_pop_band_2(), self.crumble8_pop_band_2(), self.crumble8_pop_band_2(),
                    self.crumble8_pop_band_3(), self.crumble8_pop_band_3(), self.crumble8_pop_band_3(),
                    self.crumble8_pop_band_4(), self.crumble8_pop_band_4()]
        try:
            war_dicemod = pop_band[self.hardTimesUwp[4]]
        except IndexError:
            war_dicemod = 0
        crumble_roll = self.dice.roll_1d6() + 2 + enivronmental_dicemod + war_dicemod
        reduction = self.degrees_of_change_dict[crumble_roll]
        self.historyString += "The population multiplier fell by %d due to lack of life support [note if this number" \
                              " would reduce the population modifier below one, reduce the pop UWP and wrap around to a " \
                              "population modifier of 9]\n" % reduction  # TODO auto population modifier
        self.update_results()

    def crumble8_tech_band_1(self):
        dicemod = 0
        if self.hardTimesUwp[2] == 12:
            dicemod += 5
        elif self.hardTimesUwp[2] == 0 or 1 or 10 or 11:
            dicemod += 5
        elif self.hardTimesUwp[2] == 2:
            dicemod += 5
        elif self.hardTimesUwp[2] == 3:
            dicemod += 5
        elif self.hardTimesUwp[2] == 4 or 7 or 9:
            dicemod += 3
        if self.hardTimesUwp[3] == 0:
            dicemod += 5
        elif self.hardTimesUwp[3] == 1:
            dicemod += 3
        elif self.hardTimesUwp[3] == 2 or 10:
            dicemod += 2
        if self.hardTimesUwp[3] > 1 and self.hardTimesUwp[2] > 9:
            dicemod += 5
        return dicemod

    def crumble8_tech_band_2(self):
        dicemod = 0
        if self.hardTimesUwp[2] == 12:
            dicemod += 5
        elif self.hardTimesUwp[2] == 0 or 1 or 10 or 11:
            dicemod += 5
        elif self.hardTimesUwp[2] == 2:
            dicemod += 4
        elif self.hardTimesUwp[2] == 3:
            dicemod += 3
        elif self.hardTimesUwp[2] == 4 or 7 or 9:
            dicemod += 2
        if self.hardTimesUwp[3] == 0:
            dicemod += 4
        elif self.hardTimesUwp[3] == 1:
            dicemod += 2
        elif self.hardTimesUwp[3] == 2 or 10:
            dicemod += 1
        if self.hardTimesUwp[3] > 1 and self.hardTimesUwp[2] > 9:
            dicemod += 3
        return dicemod

    def crumble8_tech_band_3(self):
        dicemod = 0
        if self.hardTimesUwp[2] == 12:
            dicemod += 4
        elif self.hardTimesUwp[2] == 0 or 1 or 10 or 11:
            dicemod += 2
        elif self.hardTimesUwp[2] == 2:
            dicemod += 2
        elif self.hardTimesUwp[2] == 3:
            dicemod += 2
        elif self.hardTimesUwp[2] == 4 or 7 or 9:
            dicemod += 1
        if self.hardTimesUwp[3] == 0:
            dicemod += 2
        elif self.hardTimesUwp[3] == 1:
            dicemod += 1
        if self.hardTimesUwp[3] > 1 and self.hardTimesUwp[2] > 9:
            dicemod += 2
        return dicemod

    def crumble8_tech_band_4(self):
        dicemod = 0
        if self.hardTimesUwp[2] == 12:
            dicemod += 2
        elif self.hardTimesUwp[2] == 0 or 1 or 10 or 11:
            dicemod += 1
        elif self.hardTimesUwp[2] == 2:
            dicemod += 1
        elif self.hardTimesUwp[2] == 3:
            dicemod += 1
        if self.hardTimesUwp[3] == 0:
            dicemod += 1
        if self.hardTimesUwp[3] > 1 and self.hardTimesUwp[2] > 9:
            dicemod += 1
        return dicemod

    def crumble8_tech_band_5(self):
        dicemod = 0
        if self.hardTimesUwp[2] == 12:
            dicemod += 1
        return  dicemod

    def crumble8_pop_band_1(self):
        dicemod = -3
        if self.warzoneStatus == 'I':
            dicemod += 1
        elif self.warzoneStatus == 'B':
            dicemod += 1
        return dicemod

    def crumble8_pop_band_2(self):
        dicemod = -2
        if self.warzoneStatus == 'W':
            dicemod += 1
        elif self.warzoneStatus == 'I':
            dicemod += 2
        elif self.warzoneStatus == 'B':
            dicemod += 3
        return dicemod

    def crumble8_pop_band_3(self):
        dicemod = 0
        if self.warzoneStatus == 'W':
            dicemod += 2
        elif self.warzoneStatus == 'I':
            dicemod += 3
        elif self.warzoneStatus == 'B':
            dicemod += 5
        return dicemod

    def crumble8_pop_band_4(self):
        dicemod = 1
        if self.warzoneStatus == 'W':
            dicemod += 1
        elif self.warzoneStatus == 'I':
            dicemod += 2
        elif self.warzoneStatus == 'B':
            dicemod += 3
        return dicemod

    def crumble9(self):
        if self.stageThreeTLDrop > 0 or self.stageSixPopMultiplierDrop > 0:
            dicemod = 0
            if self.stageThreeTLDrop > 1:
                dicemod += self.stageThreeTLDrop - 2
            if self.stageSixPopMultiplierDrop > 1:
                dicemod += self.stageSixPopMultiplierDrop - 1
            crumble_roll = self.dice.roll_1d6() + dicemod
            reduction = self.degrees_of_change_dict[crumble_roll]
            pluralism_list = [0, 2, 4, 7, 8, 9, 5, 1, 6, 3, 12, 10, 11, 14, 0]
            government_dictionary = {0: "anarchy", 2: "a participatory democracy", 4: "a representative democracy",
                                     7: "a balkanization of governments", 8: "a civil service bureaucracy",
                                     9: "an impersonal bureaucracy", 5: "technocratic feudalism", 1: "corporate rule",
                                     6: "martial law", 3: "a self-perpetuating oligarchy", 12: "a charismatic oligarchy",
                                     10: "a charismatic dictatorship", 11: "a noncharismatic or religious dictatorship",
                                     14: "a totalitarian oligarhy or religious autocracy"}
            try:
                if self.secondSurveyUwp[5] > 0:
                    starting_pluralism = pluralism_list.index(self.secondSurveyUwp[5])
                else:
                    starting_pluralism = -1
            except IndexError:
                if self.secondSurveyUwp[5] == 13:
                    starting_pluralism = pluralism_list.index(11)
                elif self.secondSurveyUwp[5] == 15:
                    starting_pluralism = pluralism_list.index(14)
                else:
                    starting_pluralism = pluralism_list.index(7)  # If no government type applies, assume balkanized
            final_pluralism = starting_pluralism - reduction  # Reduction is negative here because the table on page 24
            self.hardTimesUwp[5] = pluralism_list[final_pluralism]
            self.historyString += "The planet went through a retrenchment of political beliefs, with the government " \
                                  "falling from %s to %s.\n" % (government_dictionary[self.secondSurveyUwp[5]],
                                                                government_dictionary[self.hardTimesUwp[5]])
        law_level_roll = self.dice.roll_1d6() + self.hardTimesUwp[5]
        if law_level_roll < 0:
            law_level_roll = 0
        self.hardTimesUwp[6] = law_level_roll
        self.historyString += "The law level fell to %d.\n" % self.hardTimesUwp[6]

    def auto_crumble(self):
        # Stage 1 300-1124
        # Stage 3 181-1125
        # Stage 6 001-1127
        # Stage 8 001-1128
        # Stage 9 181-1128
        date = self.DateSpinBox.value()
        try:
            year = int(self.YearComboBox.currentText())
            if year == 1124 and date > 299:
                self.crumble1a()
                self.crumble1b()
                self.update_results()
            elif year == 1125 and date > 180:
                self.crumble1a()
                self.crumble1b()
                self.crumble3()
                self.update_results()
            elif year == 1127:
                self.crumble1a()
                self.crumble1b()
                self.crumble3()
                self.crumble6a()
                self.crumble6b()
                self.update_results()
            elif year == 1128 and date < 181:
                self.crumble1a()
                self.crumble1b()
                self.crumble3()
                self.crumble6a()
                self.crumble6b()
                self.crumble8()
                self.update_results()
            elif year == 1128 and date > 180:
                self.crumble1a()
                self.crumble1b()
                self.crumble3()
                self.crumble6a()
                self.crumble6b()
                self.crumble8()
                self.crumble9()
                self.update_results()
            else:
                self.historyString = "Hard Times not applicable"
                self.hardTimesUwp = self.secondSurveyUwp
                self.update_results()
        except ValueError:
            if self.YearComboBox.currentText() == "1129+":
                self.crumble1a()
                self.crumble1b()
                self.crumble3()
                self.crumble6a()
                self.crumble6b()
                self.crumble8()
                self.crumble9()
                self.update_results()
            else:
                self.historyString = "Hard Times not applicable"
                self.hardTimesUwp = self.secondSurveyUwp
                self.update_results()


if __name__ == "__main__":
    app = QtWidgets.QApplication(argv)
    window = MyWindow()
    window.show()
    exit(app.exec_())
