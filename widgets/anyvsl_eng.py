#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from functools import partial

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator

import anyvsl_init


from ui.ui_anyvsl_eng import Ui_Form


class mainwindow_eng(QWidget):
    def __init__(self, parent=None):
        super(mainwindow_eng, self).__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        reg_draft = QRegExp("\d{0,2}[.]\d{1,3}")
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

        reg_dens = QRegExp("([0-2])([.])\d{1,3}")
        input_validator = QRegExpValidator(reg_dens, self.ui.dens_f)
        self.ui.dens_f.setValidator(input_validator)

        reg_addparam = QRegExp("([-])?([0-9])([.])\d{1,3}")
        input_validator = QRegExpValidator(reg_addparam, self.ui.fwd_delta_f)
        self.ui.fwd_delta_f.setValidator(input_validator)
        input_validator = QRegExpValidator(reg_addparam, self.ui.mid_delta_f)
        self.ui.mid_delta_f.setValidator(input_validator)
        input_validator = QRegExpValidator(reg_addparam, self.ui.aft_delta_f)
        self.ui.aft_delta_f.setValidator(input_validator)

        reg_addparam_lower = QRegExp("\d{1,5}[.]\d{1,5}")
        input_validator = QRegExpValidator(reg_addparam_lower, self.ui.LBP_f)
        self.ui.LBP_f.setValidator(input_validator)
        input_validator = QRegExpValidator(reg_addparam_lower, self.ui.displ_momc_f)
        self.ui.displ_momc_f.setValidator(input_validator)
        input_validator = QRegExpValidator(reg_addparam_lower, self.ui.TPC_f)
        self.ui.TPC_f.setValidator(input_validator)
        input_validator = QRegExpValidator(reg_addparam_lower, self.ui.LCF_f)
        self.ui.LCF_f.setValidator(input_validator)
        input_validator = QRegExpValidator(reg_addparam_lower, self.ui.MTC_f)
        self.ui.MTC_f.setValidator(input_validator)
        input_validator = QRegExpValidator(reg_addparam_lower, self.ui.MTC_plus_f)
        self.ui.MTC_plus_f.setValidator(input_validator)
        input_validator = QRegExpValidator(reg_addparam_lower, self.ui.MTC_minus_f)
        self.ui.MTC_minus_f.setValidator(input_validator)
        input_validator = QRegExpValidator(reg_addparam_lower, self.ui.light_ship_f)
        self.ui.light_ship_f.setValidator(input_validator)

        reg_cons = QRegExp("\d{1,4}[.]\d{1,3}")
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

        self.ui.countBtn_momc.clicked.connect(self.calculate_momc)

    def calculate_momc(self):
        try:
                min(float(x) for x in (self.ui.F_ps_line.text(),
                                       self.ui.F_ss_line.text(),
                                       self.ui.M_ps_line.text(),
                                       self.ui.M_ss_line.text(),
                                       self.ui.A_ps_line.text(),
                                       self.ui.A_ss_line.text(),
                                       self.ui.LBP_f.text(),
                                       self.ui.fwd_delta_f.text(),
                                       self.ui.mid_delta_f.text(),
                                       self.ui.aft_delta_f.text()))

        except ValueError:
            warn = QMessageBox.warning(self, 'Message',
                                       "Applicable draft values only: 0 - 99"
                                       + "\n" +
                                       "Applicable density values only: 0 - 2"
                                       + "\n" +
                                       "Applicable additional parameters only: 0 - 99"
                                       + "\n", QMessageBox.Ok)
            return

        fwd_ps = float(self.ui.F_ps_line.text())
        fwd_ss = float(self.ui.F_ss_line.text())
        mid_ps = float(self.ui.M_ps_line.text())
        mid_ss = float(self.ui.M_ss_line.text())
        aft_ps = float(self.ui.A_ps_line.text())
        aft_ss = float(self.ui.A_ss_line.text())
        lbp = float(self.ui.LBP_f.text())
        fwd_delta = float(self.ui.fwd_delta_f.text())
        mid_delta = float(self.ui.mid_delta_f.text())
        aft_delta = float(self.ui.aft_delta_f.text())

        if min(fwd_ps, fwd_ss, mid_ps, mid_ss, aft_ps, aft_ss, lbp, fwd_delta,
               mid_delta, aft_delta) == 0:
            warn = QMessageBox.warning(self, 'Message',
                                         "Applicable draft values only: 0 - 99"
                                         + "\n" +
                                         "Applicable density values only: 0 - 2"
                                         + "\n" +
                                         "Applicable additional parameters only: 0 - 99"
                                         + "\n", QMessageBox.Ok)
            return

        outcome = anyvsl_init.calc_momc(fwd_ps, fwd_ss, mid_ps, mid_ss, aft_ps,
                                        aft_ss, lbp, fwd_delta, mid_delta,
                                        aft_delta)

        show_label = (str(outcome[0]) + '; ' + str(outcome[1]) + '; ' +
                      str(outcome[2]) + '\n' + str(outcome[3]) + '\n' +
                      str(outcome[4]) + '\n' + str(outcome[5]) + '\n' +
                      str(outcome[6]) + '\n' + str(outcome[7]) + '\n' +
                      str(outcome[8]) + '\n' + str(outcome[9]) + '\n' +
                      str(outcome[10]) + '\n' + str(outcome[11]) + '\n' +
                      str(outcome[12]))

        true_trim = outcome[10]

        self.ui.result.setText(str(show_label))

        self.ui.countBtn_displ.setEnabled(True)
        self.ui.dens_f.setEnabled(True)
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

        # self.ui.countBtn_displ.clicked.connect(self.calculate_displ)
        self.ui.countBtn_displ.clicked.connect(partial(self.calculate_displ, lbp, true_trim))

    # def keyPressEvent(self, event):
    #     if event.key() == Qt.Key_Return:
    #         partial(self.calculate_displ, lbp, true_trim))


    def calculate_displ(self, lbp, true_trim):
            try:
                min(float(x) for x in (self.ui.dens_f.text(),
                                       self.ui.displ_momc_f.text(),
                                               self.ui.TPC_f.text(),
                                               self.ui.LCF_f.text(),
                                               self.ui.MTC_f.text(),
                                               self.ui.MTC_plus_f.text(),
                                               self.ui.MTC_minus_f.text(),
                                               self.ui.light_ship_f.text(),
                                               self.ui.LBP_f.text(),
                                               self.ui.fwd_delta_f.text(),
                                               self.ui.mid_delta_f.text(),
                                               self.ui.aft_delta_f.text()))

            except ValueError:
                warn = QMessageBox.warning(self, 'Message',
                                              "Applicable draft values only: 0.1 - 99"
                                              + "\n" +
                                              "Applicable density values only: 0.1 - 2"
                                              + "\n" +
                                              "Applicable additional parameters only: 0.1 - 99"
                                              + "\n", QMessageBox.Ok)

            cons_raw = [self.ui.ballast_f.text(),
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

            dens = float(self.ui.dens_f.text())
            displ_momc = float(self.ui.displ_momc_f.text())
            tpc = float(self.ui.TPC_f.text())
            lcf = float(self.ui.LCF_f.text())
            mtc = float(self.ui.MTC_f.text())
            mtc_plus = float(self.ui.MTC_plus_f.text())
            mtc_minus = float(self.ui.MTC_minus_f.text())
            light_ship = float(self.ui.light_ship_f.text())
            ballast = cons[0]
            fw = cons[1]
            hfo = cons[2]
            mgo = cons[3]
            lo = cons[4]
            slops = cons[5]
            sludge = cons[6]
            other = cons[7]
            outcome = anyvsl_init.calc_displ(lbp, true_trim, dens, displ_momc, tpc, lcf, mtc, mtc_plus,
                                mtc_minus, light_ship, ballast, fw, hfo,
                                mgo, lo, slops, sludge, other)
            show_label = (str(outcome[0]) + '\n' + str(outcome[1]) + '\n' + str(outcome[2]) + '\n' + str(outcome[3]) + '\n' +
                  str(outcome[4]) + '\n' + '\n' + str(outcome[5]))

            self.ui.result_anyvsl.setText(str(show_label))



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = mainwindow_eng()
    mainWin.show()
    sys.exit(app.exec_())
