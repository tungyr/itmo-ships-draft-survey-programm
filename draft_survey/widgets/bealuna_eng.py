#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *

from draft_survey import calc, export, intro, storage
from draft_survey.ui.ui_bealuna_eng import Ui_Form


class MainWindowEng(QWidget):
    def __init__(self, parent=None):
        super(MainWindowEng, self).__init__(parent)

        print('BEALUNA_ENG')

        self.ui = Ui_Form()   # использование модуля с настройками интерфейса программы
        self.ui.setupUi(self)

        self.outcome = 0
        self.vessel_name = "HC Bea-Luna"

        self.draft_lines = (self.ui.F_ps_line, self.ui.F_ss_line, self.ui.M_ps_line, self.ui.M_ss_line,
                            self.ui.A_ps_line, self.ui.A_ss_line)

        self.stores_lines = (self.ui.ballast_f, self.ui.fw_f, self.ui.hfo_f, self.ui.mgo_f, self.ui.lo_f,
                             self.ui.slops_f, self.ui.sludge_f, self.ui.other_f)

        # установка значений по умолчанию для полей
        for draft_line in self.draft_lines:
            draft_line.setText('2.0')

        for store_line in self.stores_lines:
            store_line.setText('100')

        self.ui.dens_f.setText('1.025')

        # всплывающие подсказки для полей осадок
        for draft_line in self.draft_lines:
            draft_line.setToolTip('Applicable draft values only: 2 - 7.8')

        # обработка нажатия кнопки расчета
        self.ui.countBtn.clicked.connect(lambda: self.calculate(draft_lines=self.draft_lines,
                                                   stores_lines=self.stores_lines, density_line=self.ui.dens_f))

        # обработка нажатия кнопки экспортирования данных в отчет
        self.ui.export_2.clicked.connect(lambda: export.App(self.outcome, self.vessel_name))

        # обработка нажатия кнопки очистки данных полей
        self.ui.clear.clicked.connect(lambda: self.clear_forms())

        # обработка нажатия кнопки возвращения в главное меню
        self.ui.main_menu.clicked.connect(lambda: intro_window())

        def intro_window() -> None:
            """Функция запуска приветственного окна"""
            self.main_win = intro.IntroWindow()
            self.main_win.show()
            self.close()


    def clear_forms(self) -> None:
        """Функция очистки полей от значений"""
        for draft_line in self.draft_lines:
            draft_line.setText('')

        for store_line in self.stores_lines:
            store_line.setText('')

        self.ui.dens_f.setText('')

        self.ui.result.setText('')

    def calculate(self, draft_lines:list, stores_lines, density_line) -> (None, tuple):
        """Функция расчета введенных данных"""

        validates_result = self.validate_forms(draft_lines=self.draft_lines, stores_lines=self.stores_lines,
                                               density_line=self.ui.dens_f)

        if validates_result is None:
            return

        draft_lines, stores_lines, density_line = validates_result[0], validates_result[1], validates_result[2]

        params_labels = ['fwd_ps', 'fwd_ss', 'mid_ps', 'mid_ss', 'aft_ps', 'aft_ss', 'ballast', 'fw', 'hfo', 'mgo',
                         'lo', 'slops', 'sludge', 'other', 'density']

        params_values = validates_result[0] + validates_result[1]
        params_values.append(density_line)
        params = dict(zip(params_labels, params_values))

        # вызов функции расчета с передачей параметров
        outcome = calc.calculation(params)

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

        self.outcome = outcome

        self.ui.result.setText(str(show_label))

        return self.outcome


    def validate_forms(self, draft_lines, stores_lines, density_line) -> (list, list, float):
        """Функция валидации введенных пользователем данных"""

        try:
            draft_lines = [float(draft_line.text()) for draft_line in draft_lines]
            density_line = float(density_line.text())
        except ValueError:
            warn = QMessageBox.warning(self, 'Message',
                                       "Applicable draft values only: 2 - 7.8"
                                       + "\n" + "Applicable density values only: 0.1 - 2"
                                       + "\n", QMessageBox.Ok)
            return

        try:
            stores_lines = [float(store_line.text()) for store_line in stores_lines]
        except ValueError:
            warn = QMessageBox.warning(self, 'Message',
                                       "Stores not filled up!" + "\n", QMessageBox.Ok)
            return

        if max(draft_lines) > 7.8 or min(draft_lines) < 2.0:
            warn = QMessageBox.warning(self, 'Message',
                                       "Applicable draft values only: 2 - 7.8"
                                       + "\n", QMessageBox.Ok)

            return

        if 2.0 < density_line or density_line < 0.1:
            warn = QMessageBox.warning(self, 'Message', "Applicable density values only: 0.1 - 2" +
                                       "\n", QMessageBox.Ok)
            return

        if storage.connect('hydrostatic.sqlite') == "DB is missing!":
            warn = QMessageBox.warning(self, 'Message', "Database is missing!" +
                                       "\n", QMessageBox.Ok)
            return

        return draft_lines, stores_lines, density_line


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindowEng()
    mainWin.show()
    sys.exit(app.exec_())
