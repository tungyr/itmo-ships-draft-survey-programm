#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PyQt5 import Qt
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QFileInfo, QSettings, QSize

from ui_intro import Ui_Draft_survey
import bealuna_eng
import bealuna_rus
import anyvsl_eng
import anyvsl_rus


class intro_window(QWidget):
    def __init__(self, parent=None):
        """Начальное окно с опциями выбора дальнейшей модели расчета"""
        super(intro_window, self).__init__(parent)
        # self.setObjectName("MainWindow")
        # self.setMinimumSize(QSize(400, 300))
        # self.setWindowTitle("Draft Survey")

        self.uintr = Ui_Draft_survey()
        self.uintr.setupUi(self)

        # запуск основного окна в зависимости от нажатой кнопки
        self.uintr.start_btn.clicked.connect(self.launch_main_window)

    def launch_main_window(self):
                if self.uintr.radiobtn_eng.isChecked() and self.uintr.radiobtn_bealuna.isChecked():
                    self.main_win = bealuna_eng.mainwindow_eng()
                    self.main_win.show()
                    self.close()
                elif self.uintr.radiobtn_rus.isChecked() and self.uintr.radiobtn_bealuna.isChecked():
                    self.main_win = bealuna_rus.mainwindow_rus()
                    self.main_win.show()
                    self.close()
                elif self.uintr.radiobtn_eng.isChecked() and self.uintr.radiobtn_anyvsl.isChecked():
                    self.main_win = anyvsl_eng.mainwindow_eng()
                    self.main_win.show()
                    self.close()
                elif self.uintr.radiobtn_rus.isChecked() and self.uintr.radiobtn_anyvsl.isChecked():
                    self.main_win = anyvsl_rus.mainwindow_rus()
                    self.main_win.show()
                    self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = intro_window()
    mainWin.show()
    sys.exit(app.exec_())
