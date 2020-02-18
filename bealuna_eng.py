#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PyQt5 import Qt
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QFileInfo, QSettings, QSize
from PyQt5.QtGui import QIcon, QPixmap

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator

import __init__


from ui_bealuna_eng import Ui_Form


class MainWindowEng(QWidget):
    def __init__(self, parent=None) -> object:
        super(MainWindowEng, self).__init__(parent)

        self.ui = Ui_Form()   # использование модуля с настройками интерфейса программы
        self.ui.setupUi(self)

        self.draft_lines = (self.ui.F_ps_line, self.ui.F_ss_line, self.ui.M_ps_line, self.ui.M_ss_line,
                            self.ui.A_ps_line, self.ui.A_ss_line)

        self.stores_lines = (self.ui.ballast_f, self.ui.fw_f, self.ui.hfo_f, self.ui.mgo_f, self.ui.lo_f,
                             self.ui.slops_f, self.ui.sludge_f, self.ui.other_f)

        # установка значений по умолчанию для полей
        # TODO half-transparent values + save last values inserted by user
        # TODO previous values switches by user
        for draft_line in self.draft_lines:
            draft_line.setText('2.0')

        for store_line in self.stores_lines:
            store_line.setText('100')

        self.ui.dens_f.setText('1.025')


        # определение валидаторов на основе регулярных выражения для полей осадок
        reg_draft = QRegExp("([2-8])([.])\d{1,3}")
        input_validator = QRegExpValidator(reg_draft)

        for draft_line in self.draft_lines:
            draft_line.setValidator(input_validator)

        # всплывающие подсказки для полей осадок
        for draft_line in self.draft_lines:
            draft_line.setToolTip('Applicable draft values only: 2 - 7.8')

        # валидатор для поля плотности воды
        reg_dens = QRegExp("([0-2])([.])\d{1,3}")
        input_validator = QRegExpValidator(reg_dens, self.ui.dens_f)
        self.ui.dens_f.setValidator(input_validator)
        self.ui.dens_f.setToolTip("Applicable density values only: 0.1 - 2")

        # валидоторы полей запасов
        reg_stores = QRegExp("\d{1,4}[.]\d{1,3}")
        input_validator_stores = QRegExpValidator(reg_stores)

        for store_line in self.stores_lines:
            store_line.setValidator(input_validator_stores)

        if self.ui.countBtn.clicked:
            self.ui.countBtn.clicked.connect(lambda: self.calculate(draft_lines=self.draft_lines,
                                                   stores_lines=self.stores_lines, density_line=self.ui.dens_f))

    # TODO: density values?



    def calculate(self, draft_lines, stores_lines, density_line):
        #TODO: zip

        validates_result = self.validate_forms(draft_lines=self.draft_lines, stores_lines=self.stores_lines,
                                               density_line=self.ui.dens_f)

        draft_lines = validates_result[0]
        stores_lines = validates_result[1]
        density_line = validates_result[2]

        fwd_ps = draft_lines[0]
        fwd_ss = draft_lines[1]
        mid_ps = draft_lines[2]
        mid_ss = draft_lines[3]
        aft_ps = draft_lines[4]
        aft_ss = draft_lines[5]

        # присваивание имен значениям запасов

        ballast =   stores_lines[0]
        fw =        stores_lines[1]
        hfo =       stores_lines[2]
        mgo =       stores_lines[3]
        lo =        stores_lines[4]
        slops =     stores_lines[5]
        sludge =    stores_lines[6]
        other =     stores_lines[7]

        dens = density_line

        # вызов функции расчета с передачей параметров
        outcome = __init__.calc(fwd_ps, fwd_ss, mid_ps, mid_ss, aft_ps, aft_ss,
                                dens, ballast, fw, hfo, mgo, lo, slops, sludge,
                                other)
        # вывод значений в форму программы
        show_label = (str(outcome[0]) + '; ' + str(outcome[1]) + '; ' +
                      str(outcome[2]) + '\n' + str(outcome[3]) + '\n' +
                      str(outcome[4]) + '\n' + str(outcome[5]) + '\n' +
                      str(outcome[6]) + '\n' + str(outcome[7]) + '\n' +
                      str(outcome[8]) + '\n' + str(outcome[9]) + '\n' +
                      str(outcome[10]) + '\n' + str(outcome[11]) + '\n' +
                      str(outcome[12]) + '\n' + str(outcome[13]) + '\n' +
                      str(outcome[14]) + '\n' + str(outcome[15]) + '\n' +
                      str(outcome[16]) + '\n' + str(outcome[17]) + '\n' +
                      str(outcome[18]) + '\n' + str(outcome[19]) + '\n' +
                      str(outcome[20]) + '\n' + str(outcome[21]) + '; ' +
                      str(outcome[22]) + '\n' + str(outcome[23]) + '\n' +
                      str(outcome[24]) + '\n' + str(outcome[25]) +
                      '\n' + str(outcome[26]) + '\n' + '\n' +
                      str(outcome[27]))
        print(show_label)

        self.ui.result.setText(str(show_label))




    def validate_forms(self, draft_lines, stores_lines, density_line):

        draft_lines = [float(draft_line.text()) for draft_line in draft_lines]

        for draft_line in draft_lines:
            if draft_line not in {2, 7.8}:
                # print("Applicable draft values only: 2 - 7.8"
                #       + "\n" +
                #       "Applicable density values only: 0.1 - 2"
                #       + "\n")
                warn = QMessageBox.warning(self, 'Message',
                                           "Applicable draft values only: 2 - 7.8"
                                           + "\n" + "Applicable density values only: 0.1 - 2"
                                           + "\n", QMessageBox.Ok)
                return None

        # if float(density_line.text()) not in {0.1, 2}:
        #     warn = QMessageBox.warning(self, 'Message', "Applicable density values only: 0.1 - 2" +
        #                                "\n", QMessageBox.Ok)
        #     return None

        stores_lines = [int(store_line.text()) for store_line in stores_lines]
        # проверка заполненности форм запасов и присваивание им 0 при случаи
        # cons_raw = [self.ui.dens_f.text(),
        #         #             self.ui.ballast_f.text(),
        #         #             self.ui.fw_f.text(),
        #         #             self.ui.hfo_f.text(),
        #         #             self.ui.mgo_f.text(),
        #         #             self.ui.lo_f.text(),
        #         #             self.ui.slops_f.text(),
        #         #             self.ui.sludge_f.text(),
        #         #             self.ui.other_f.text()]

        density_line = float(density_line.text())

        return draft_lines, stores_lines, density_line


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindowEng()
    mainWin.show()
    sys.exit(app.exec_())
