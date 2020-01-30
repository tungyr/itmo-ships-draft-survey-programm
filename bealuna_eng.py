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
    def __init__(self, parent=None):
        super(MainWindowEng, self).__init__(parent)

        self.ui = Ui_Form()   # использование модуля с настройками интерфейса программы
        self.ui.setupUi(self)

        reg_draft = QRegExp("([2-8])([.])\d{1,3}")  # рег. выражения осадки
        input_validator = QRegExpValidator(reg_draft, self.ui.F_ps_line)
        self.ui.F_ps_line.setValidator(input_validator)
        input_validator = QRegExpValidator(reg_draft, self.ui.F_ss_line)
        self.ui.F_ss_line.setValidator(input_validator)
        input_validator = QRegExpValidator(reg_draft, self.ui.M_ps_line)
        self.ui.M_ps_line.setValidator(input_validator)
        input_validator = QRegExpValidator(reg_draft, self.ui.M_ss_line)
        self.ui.M_ss_line.setValidator(input_validator)
        input_validator = QRegExpValidator(reg_draft, self.ui.A_ps_line)
        self.ui.A_ps_line.setValidator(input_validator)
        input_validator = QRegExpValidator(reg_draft, self.ui.A_ss_line)
        self.ui.A_ss_line.setValidator(input_validator)

        reg_dens = QRegExp("([0-2])([.])\d{1,3}")  # рег. выражения плотность воды
        input_validator = QRegExpValidator(reg_dens, self.ui.dens_f)
        self.ui.dens_f.setValidator(input_validator)

        reg_cons = QRegExp("\d{1,4}[.]\d{1,3}")  # рег. выражения запасы
        input_validator = QRegExpValidator(reg_cons, self.ui.ballast_f)
        self.ui.ballast_f.setValidator(input_validator)
        input_validator = QRegExpValidator(reg_cons, self.ui.fw_f)
        self.ui.fw_f.setValidator(input_validator)
        input_validator = QRegExpValidator(reg_cons, self.ui.hfo_f)
        self.ui.hfo_f.setValidator(input_validator)
        input_validator = QRegExpValidator(reg_cons, self.ui.mgo_f)
        self.ui.mgo_f.setValidator(input_validator)
        input_validator = QRegExpValidator(reg_cons, self.ui.lo_f)
        self.ui.lo_f.setValidator(input_validator)
        input_validator = QRegExpValidator(reg_cons, self.ui.slops_f)
        self.ui.slops_f.setValidator(input_validator)
        input_validator = QRegExpValidator(reg_cons, self.ui.sludge_f)
        self.ui.sludge_f.setValidator(input_validator)
        input_validator = QRegExpValidator(reg_cons, self.ui.other_f)
        self.ui.other_f.setValidator(input_validator)

        # обработка кнопки, запуск расчета
        self.ui.countBtn.clicked.connect(self.calculate)

    def calculate(self):
        # отлавливание незаполненных форм
        try:
                min(float(x) for x in (self.ui.F_ps_line.text(),
                                       self.ui.F_ss_line.text(),
                                       self.ui.M_ps_line.text(),
                                       self.ui.M_ss_line.text(),
                                       self.ui.A_ps_line.text(),
                                       self.ui.A_ss_line.text()))
        except ValueError:
                warn = QMessageBox.warning(self, 'Message',
                                              "Applicable draft values only: 2 - 7.8"
                                              + "\n" +
                                              "Applicable density values only: 0.1 - 2"
                                              + "\n", QMessageBox.Ok)
                return
        # конвертирование осалок в тип float()
        fwd_ps = float(self.ui.F_ps_line.text())
        fwd_ss = float(self.ui.F_ss_line.text())
        mid_ps = float(self.ui.M_ps_line.text())
        mid_ss = float(self.ui.M_ss_line.text())
        aft_ps = float(self.ui.A_ps_line.text())
        aft_ss = float(self.ui.A_ss_line.text())

        # отлавливание осадок более 7.8
        if max(fwd_ps, fwd_ss, mid_ps, mid_ss, aft_ps, aft_ss) > 7.8:
            warn = QMessageBox.warning(self, 'Message',
                                          "Applicable draft values only: 2 - 7.8"
                                          + "\n" +
                                          "Applicable density values only: 0.1 - 2"
                                          + "\n", QMessageBox.Ok)
            return

        # проверка заполненности форм запасов и присваивание им 0 при случаи
        cons_raw = [self.ui.dens_f.text(),
                    self.ui.ballast_f.text(),
                    self.ui.fw_f.text(),
                    self.ui.hfo_f.text(),
                    self.ui.mgo_f.text(),
                    self.ui.lo_f.text(),
                    self.ui.slops_f.text(),
                    self.ui.sludge_f.text(),
                    self.ui.other_f.text()]

        cons = []
        for i in cons_raw:
            if i == '':
                i = 0
                cons.append(i)
            else:
                cons.append(float(i))

        # присваивание имен значениям запасов
        dens = cons[0]
        ballast = cons[1]
        fw = cons[2]
        hfo = cons[3]
        mgo = cons[4]
        lo = cons[5]
        slops = cons[6]
        sludge = cons[7]
        other = cons[8]

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

        self.ui.result.setText(str(show_label))




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = intro_window()
    mainWin.show()
    sys.exit(app.exec_())
