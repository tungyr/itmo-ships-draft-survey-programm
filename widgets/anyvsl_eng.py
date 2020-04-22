#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from functools import partial

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator

import anyvsl_init
import __init__, export, intro

from ui.ui_anyvsl_eng import Ui_Form


class MainWindowEng(QWidget):
    def __init__(self, parent=None):
        super(MainWindowEng, self).__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.vessel_name = self.ui.ships_name.text()

        self.result_label_momc = ''
        self.result_label_displ = ''

        self.draft_lines = (self.ui.F_ps_line, self.ui.F_ss_line, self.ui.M_ps_line, self.ui.M_ss_line,
                            self.ui.A_ps_line, self.ui.A_ss_line)

        self.additional_params_first = (self.ui.dens_f, self.ui.LBP_f, self.ui.fwd_delta_f, self.ui.mid_delta_f,
                                        self.ui.aft_delta_f)

        self.additional_params_second = (self.ui.displ_momc_f, self.ui.TPC_f, self.ui.LCF_f, self.ui.MTC_f,
                                         self.ui.MTC_plus_f, self.ui.MTC_minus_f, self.ui.light_ship_f)

        self.stores_lines = (self.ui.ballast_f, self.ui.fw_f, self.ui.hfo_f, self.ui.mgo_f, self.ui.lo_f,
                             self.ui.slops_f, self.ui.sludge_f, self.ui.other_f)

        # установка значений по умолчанию для полей
        for draft_line in self.draft_lines:
            draft_line.setText('2.0')

        self.ui.ships_name.setText('unnamed')
        self.ui.dens_f.setText('1.025')
        self.ui.LBP_f.setText('145')
        self.ui.fwd_delta_f.setText('2.0')
        self.ui.mid_delta_f.setText('2.0')
        self.ui.aft_delta_f.setText('2.0')

        self.ui.displ_momc_f.setText('3000')
        self.ui.TPC_f.setText('16')
        self.ui.LCF_f.setText('65')
        self.ui.MTC_f.setText('107')
        self.ui.MTC_plus_f.setText('110')
        self.ui.MTC_minus_f.setText('103')
        self.ui.light_ship_f.setText('2500')

        for store_line in self.stores_lines:
            store_line.setText('100')

        # всплывающие подсказки для полей осадок
        for draft_line in self.draft_lines:
            draft_line.setToolTip('Applicable draft values only: 2 - 7.8')


        self.ui.countBtn_momc.clicked.connect(self.calculate_momc)
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

        self.ui.ships_name.setText('')
        self.ui.result_anyvsl.setText('')

        for draft_line in self.draft_lines:
            draft_line.setText('')

        for store_line in self.stores_lines:
            store_line.setText('')

        for line in self.additional_params_first:
            line.setText('')

        for line in self.additional_params_second:
            line.setText('')

    def calculate_momc(self):

        validates_result = self.validate_forms('momc', self.draft_lines, self.additional_params_first)

        if validates_result is None:
            return

        params_labels = ['fwd_ps', 'fwd_ss', 'mid_ps', 'mid_ss', 'aft_ps', 'aft_ss', 'dens', 'lbp', 'fwd_delta',
                         'mid_delta', 'aft_delta']

        params_values = validates_result[0] + validates_result[1]
        params = dict(zip(params_labels, params_values))

        # вызов функции расчета с передачей параметров
        outcome = anyvsl_init.calc_momc(params=params)

        self.result_label_momc = (str(outcome[0]) + '; ' + str(outcome[1]) + '; ' + str(outcome[2]) + '\n' +
                                str(params['fwd_delta']) + '\n' +
                                str(params['mid_delta']) + '\n' +
                                str(params['aft_delta']) + '\n' +
                                str(outcome[3]) + '\n' +
                                str(outcome[4]) + '\n' +
                                str(outcome[5]) + '\n' +
                                str(outcome[6]) + '\n' +
                                str(outcome[7]) + '\n' +
                                str(outcome[8]) + '\n' +
                                str(outcome[9]) + '\n' +
                                str(outcome[10]) + '\n' +
                                str(outcome[11]) + '\n' +
                                str(outcome[12]) + '\n')

        self.ui.result_anyvsl.setText(str(self.result_label_momc))

        self.ui.countBtn_displ.setEnabled(True)
        self.ui.displ_momc_f.setEnabled(True)
        self.ui.TPC_f.setEnabled(True)
        self.ui.LCF_f.setEnabled(True)
        self.ui.MTC_f.setEnabled(True)
        self.ui.MTC_plus_f.setEnabled(True)
        self.ui.MTC_minus_f.setEnabled(True)
        self.ui.light_ship_f.setEnabled(True)

        self.ui.light_ship_f.setEnabled(True)
        self.ui.ballast_f.setEnabled(True)
        self.ui.fw_f.setEnabled(True)
        self.ui.hfo_f.setEnabled(True)
        self.ui.mgo_f.setEnabled(True)
        self.ui.lo_f.setEnabled(True)
        self.ui.slops_f.setEnabled(True)
        self.ui.sludge_f.setEnabled(True)
        self.ui.other_f.setEnabled(True)
        self.ui.export_2.setEnabled(True)

        QMessageBox.information(self, 'Message',
                            "Please fill up next fields using calculated data and your hydrostatic tables"
                            + "\n", QMessageBox.Ok)

        self.ui.countBtn_displ.clicked.connect(partial(self.calculate_displ, params['lbp'], params['dens'],
                                                       true_trim=outcome[10]))


    def calculate_displ(self, lbp, dens, true_trim):

        validates_result = self.validate_forms(self.additional_params_second, self.stores_lines)

        if validates_result is None:
            return

        params_labels = ['lbp', 'true_trim', 'dens', 'displ_momc', 'tpc', 'lcf', 'mtc', 'mtc_plus',
                         'mtc_minus', 'light_ship', 'ballast', 'fw', 'hfo', 'mgo', 'lo', 'slops', 'sludge', 'other']

        params_values = [lbp, true_trim, dens] + validates_result[0] + validates_result[1]
        params = dict(zip(params_labels, params_values))

        # вызов функции расчета с передачей параметров
        outcome = anyvsl_init.calc_displ(params=params)
        self.result_label_displ = (str(params['displ_momc']) + '\n' +
                                   str(params['tpc']) + '\n' +
                                   str(params['lcf']) + '\n' +
                                   str(outcome[0]) + '\n' +
                                    str(params['mtc']) + '\n' +
                                    str(params['mtc_plus']) + '; ' + str(params['mtc_minus']) + '\n' +
                                   str(outcome[1]) + '\n' +
                                   str(outcome[2]) + '\n' +
                                   str(outcome[3]) + '\n' +
                                   str(outcome[4]) + '\n' + '\n' +
                                   str(outcome[5]))

        self.ui.result_anyvsl.setText(str(self.result_label_momc + self.result_label_displ))
        self.ui.countBtn_displ.setDisabled(True)

    # def validate_forms(self, forms, draft_lines, additional_params_first) -> (list, list, float):
    def validate_forms(self, *args) -> (list, list, float):
        """Функция валидации введенных пользователем данных"""

        # проверка значений для первой части вычислений
        if args[0] == "momc":

            # проверка валидности полей осадок и доп. параметров
            try:
                draft_lines = [float(draft_line.text()) for draft_line in args[1]]
                additional_params_first = [float(param.text()) for param in args[2]]

            except ValueError:
                QMessageBox.warning(self, 'Message',
                                           "Applicable draft values only: 0.1 - 99"
                                           + "\n" + "Applicable density values only: 0.1 - 2"
                                           + "\n" + "Applicable additional parameters only: 0.1 - 99"
                                           + "\n", QMessageBox.Ok)
                return

            # проверка названия судна
            # TO-DO: move to export func
            if len(self.ui.ships_name.text()) == 0:
                QMessageBox.warning(self, 'Message',
                                           "Vessel's name is empty!", QMessageBox.Ok)

                return

            if max(draft_lines) > 99:
                QMessageBox.warning(self, 'Message',
                                           "Applicable draft values only: 2 - 7.8"
                                           + "\n" + "Applicable density values only: 0.1 - 2"
                                           + "\n", QMessageBox.Ok)

                return

            return draft_lines, additional_params_first

        # проверка значений для второй части вычислений
        else:
            try:
                additional_params_second = [float(param.text()) for param in args[0]]
            except ValueError:
                QMessageBox.warning(self, 'Message',
                                           "Applicable additional parameters only: 0 - 99"
                                           + "\n", QMessageBox.Ok)
                return

            try:
                stores_lines = [float(store_line.text()) for store_line in args[1]]
            except ValueError:
                QMessageBox.warning(self, 'Message',
                                           "Stores not filled up!" + "\n", QMessageBox.Ok)
                return

            return additional_params_second, stores_lines


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindowEng()
    mainWin.show()
    sys.exit(app.exec_())
