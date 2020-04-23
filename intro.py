#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QWidget
import sys


from draft_survey.ui.ui_intro import Ui_Draft_survey
from draft_survey.widgets import anyvsl_eng, anyvsl_rus, bealuna_eng, bealuna_rus


class IntroWindow(QWidget):
    def __init__(self, parent=None):
        """Начальное окно с опциями выбора дальнейшей модели расчета"""
        super(IntroWindow, self).__init__(parent)

        self.ui_intro = Ui_Draft_survey()
        # использование модуля с настройками интерфейса программы
        self.ui_intro.setupUi(self)

        # запуск основного окна в зависимости от нажатой кнопки
        self.ui_intro.letsgo_btn.clicked.connect(self.launch_main_window)

    def launch_main_window(self) -> None:
        if self.ui_intro.eng_radiobtn.isChecked() and self.ui_intro.bealuna_radiobtn.isChecked():
            self.main_win = bealuna_eng.MainWindowEng()
            self.main_win.show()
            self.close()

        elif self.ui_intro.rus_radiobtn.isChecked() and self.ui_intro.bealuna_radiobtn.isChecked():
            self.main_win = bealuna_rus.MainwindowRus()
            self.main_win.show()
            self.close()

        elif self.ui_intro.eng_radiobtn.isChecked() and self.ui_intro.anyvsl_radiobtn.isChecked():
            self.main_win = anyvsl_eng.MainWindowEng()
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
