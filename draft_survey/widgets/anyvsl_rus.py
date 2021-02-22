#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from functools import partial

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator

from draft_survey import anyvsl_init, export, intro

from draft_survey.ui.ui_anyvsl_rus import Ui_Form


class MainWindowAnyvslRus(QWidget):
    def __init__(self, parent=None):
        super(MainWindowAnyvslRus, self).__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.result_momc = ()
        self.result_displ = ()
        self.params = {}
        print('ANYVSL_RUS')

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

        # обработка нажатия кнопки расчета momc
        self.ui.countBtn_momc.clicked.connect(self.calculate_momc_rus)

        # обработка нажатия кнопки расчета водоизмещения
        self.ui.countBtn_displ.clicked.connect(partial(self.calculate_displ))

        # обработка нажатия кнопки экспортирования данных в отчет
        self.ui.export_2.clicked.connect(lambda: export.App(self.result_momc + self.result_displ,
                                                            vessel_name=self.ui.ships_name.text()))
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

    def calculate_momc_rus(self):

        validates_result = self.validate_forms('momc', self.draft_lines, self.additional_params_first)

        if validates_result is None:
            return

        params_labels = ['fwd_ps', 'fwd_ss', 'mid_ps', 'mid_ss', 'aft_ps', 'aft_ss', 'dens', 'lbp', 'fwd_delta',
                         'mid_delta', 'aft_delta']

        params_values = validates_result[0] + validates_result[1]

        # словарь для хранения принятых от пользователя значений, по которым будет расчет в anyvsl_init.calc_momc
        self.params = dict(zip(params_labels, params_values))

        # вызов функции расчета с передачей параметров
        self.result_momc = anyvsl_init.calc_momc(params=self.params)

        self.result_label_momc = (str(self.result_momc[0]) + '; ' + str(self.result_momc[1]) + '; '
                                + str(self.result_momc[2]) + '\n' +
                                str(self.result_momc[3]) + '\n' +
                                str(self.result_momc[4]) + '\n' +
                                str(self.result_momc[5]) + '\n' +
                                str(self.result_momc[6]) + '\n' +
                                str(self.result_momc[7]) + '\n' +
                                str(self.result_momc[8]) + '\n' +
                                str(self.result_momc[9]) + '\n' +
                                str(self.result_momc[10]) + '\n' +
                                str(self.result_momc[11]) + '\n' +
                                str(self.result_momc[12]) + '\n' +
                                str(self.result_momc[13]) + '\n' +
                                str(self.result_momc[14]) + '\n' +
                                str(self.result_momc[15]) + '\n')

        # вывод первоначального результата в программе
        self.ui.result_anyvsl.setText(str(self.result_label_momc))

        # активирование полей для ввода пользователем следующих вводных данных для расчета водоизмещения
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

        # сообщение о необходимости заполнения доп. параметров
        if self.ui.displ_momc_f.text() == '':
            QMessageBox.information(self, 'Message', "Заполните оставшиеся поля с помощью гидростатических таблиц"
                                    + "\n", QMessageBox.Ok)

        return


    def calculate_displ(self,):

        validates_result = self.validate_forms(self.additional_params_second, self.stores_lines)

        if validates_result is None:
            return

        lbp = self.params['lbp']
        dens = self.params['dens']
        true_trim = self.result_momc[13]

        params_labels = ['lbp', 'true_trim', 'dens', 'displ_momc', 'tpc', 'lcf', 'mtc', 'mtc_plus',
                         'mtc_minus', 'light_ship', 'ballast', 'fw', 'hfo', 'mgo', 'lo', 'slops', 'sludge', 'other']

        params_values = [lbp, true_trim, dens] + validates_result[0] + validates_result[1]
        params = dict(zip(params_labels, params_values))

        # вызов функции расчета с передачей параметров
        self.result_displ = anyvsl_init.calc_displ(params=params)

        self.result_label_displ = (str(self.result_displ[0]) + '\n' +
                                    str(self.result_displ[1]) + '\n' +
                                    str(self.result_displ[2]) + '\n' +
                                    str(self.result_displ[3]) + '\n' +
                                    str(self.result_displ[4]) + '\n' +
                                    str(self.result_displ[5]) + '; ' + str(self.result_displ[6]) + '\n' +
                                    str(self.result_displ[7]) + '\n' +
                                    str(self.result_displ[8]) + '\n' +
                                    str(self.result_displ[9]) + '\n' +
                                    str(self.result_displ[10]) + '\n' + '\n' +
                                    str(self.result_displ[11]))

        self.ui.result_anyvsl.setText(str(self.result_label_momc + self.result_label_displ))
        self.ui.countBtn_displ.setDisabled(True)

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
                                           "Допустимые значения осадок: 0.1 - 99"
                                           + "\n" + "Допустимое значение плотности воды: 0.1 - 2"
                                           + "\n" + "Допустимые значения доп. параметров: 0.1 - 99"
                                           + "\n", QMessageBox.Ok)
                return

            if max(draft_lines) > 99:
                QMessageBox.warning(self, 'Message',
                                           "Допустимые значения осадок: 0.1 - 99"
                                           + "\n" + "Допустимое значение плотности воды: 0.1 - 2"
                                           + "\n", QMessageBox.Ok)

                return

            return draft_lines, additional_params_first

        # проверка значений для второй части вычислений
        else:
            try:
                additional_params_second = [float(param.text()) for param in args[0]]
            except ValueError:
                QMessageBox.warning(self, 'Message',
                                           "Допустимые значения доп. параметров: 0.1 - 99"
                                           + "\n", QMessageBox.Ok)
                return

            try:
                stores_lines = [float(store_line.text()) for store_line in args[1]]
            except ValueError:
                QMessageBox.warning(self, 'Message',
                                           "Значения запасов не заполнены!" + "\n", QMessageBox.Ok)
                return

            return additional_params_second, stores_lines


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindowAnyvslRus()
    mainWin.show()
    sys.exit(app.exec_())
