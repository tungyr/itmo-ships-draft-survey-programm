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

# TODO: springs
# TODO: tests
# TODO: report to excel
# TODO: sessions menu
# TODO: reset button
# TODO: return from calc page to intro window
class IntroWindow(QWidget):
    def __init__(self, parent=None):
        """Начальное окно с опциями выбора дальнейшей модели расчета"""
        super(IntroWindow, self).__init__(parent)
        # self.setObjectName("MainWindow")
        # self.setMinimumSize(QSize(400, 300))
        # self.setWindowTitle("Draft Survey")

        self.ui_intro = Ui_Draft_survey()
        self.ui_intro.setupUi(self)  # использование модуля с настройками интерфейса программы

        # запуск основного окна в зависимости от нажатой кнопки
        self.ui_intro.letsgo_btn.clicked.connect(self.launch_main_window)

    def launch_main_window(self):
        if self.ui_intro.eng_radiobtn.isChecked() and self.ui_intro.bealuna_radiobtn.isChecked():
            self.main_win = bealuna_eng.MainWindowEng()
            self.main_win.show()
            self.close()

        elif self.ui_intro.rus_radiobtn.isChecked() and self.ui_intro.bealuna_radiobtn.isChecked():
            self.main_win = bealuna_rus.mainwindow_rus()
            self.main_win.show()
            self.close()

        elif self.ui_intro.eng_radiobtn.isChecked() and self.ui_intro.anyvsl_radiobtn.isChecked():
            self.main_win = anyvsl_eng.mainwindow_eng()
            self.main_win.show()
            self.close()

        elif self.ui_intro.rus_radiobtn.isChecked() and self.ui_intro.anyvsl_radiobtn.isChecked():
            self.main_win = anyvsl_rus.mainwindow_rus()
            self.main_win.show()
            self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = IntroWindow()
    mainWin.show()
    sys.exit(app.exec_())
