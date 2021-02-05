# http://johnnado.com/pyqt-qtest-example/
# https://www.riverbankcomputing.com/static/Docs/PyQt5/
# https://github.com/pytest-dev/pytest-qt
# https://pytest-qt.readthedocs.io/en/latest/reference.html#module-pytestqt.qtbot
# https://pytest-qt.readthedocs.io/en/latest/intro.html#requirements

import sys
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from PyQt5 import QtCore

from draft_survey import intro

import pytestqt

# first_test = QTest()

# if QTest.mousePress(first_test, intro.bealuna_eng.qDrawWinButton(), ):
#    print('pressed')

# QTest.mousePress(intro.mainWin)

def test_hello(qtbot):
    widget = intro.IntroWindow()
    qtbot.addWidget(widget)

    qtbot.mouseClick(widget.button_greet, QtCore.Qt.LeftButton)

    assert widget.greet_label.text() == "Hello!"

