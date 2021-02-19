# http://johnnado.com/pyqt-qtest-example/
# https://www.riverbankcomputing.com/static/Docs/PyQt5/
# https://github.com/pytest-dev/pytest-qt
# https://pytest-qt.readthedocs.io/en/latest/reference.html#module-pytestqt.qtbot
# https://pytest-qt.readthedocs.io/en/latest/intro.html#requirements

# https://pytest-qt.readthedocs.io/en/latest/_modules/pytestqt/qtbot.html
# https://pytest-qt.readthedocs.io/en/latest/tutorial.html

# https://stackoverflow.com/questions/57065728/how-to-check-correct-opening-the-window-after-the-click-by-button-in-pytest-qt

# https://pytest-qt.readthedocs.io/en/latest/reference.html#module-pytestqt.qtbot

import sys
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from PyQt5 import QtCore

from draft_survey import intro

import pytest

from draft_survey import intro
from draft_survey.widgets import anyvsl_eng, anyvsl_rus, bealuna_eng, bealuna_rus

@pytest.fixture
def app(qtbot):
    test_intro_app = intro.IntroWindow()  # какое приложение тестируем
    qtbot.addWidget(test_intro_app)  # we are "registering" our app object to qtbot

    return test_intro_app
#
#
# def test_label(app):
#     assert app.text_label.text() == "Hello World!"


def test_letsgo_click_default_win(app, qtbot):
    qtbot.mouseClick(app.ui_intro.letsgo_btn, QtCore.Qt.LeftButton)
    # assert app.vessel_name == "HC Bea-Luna"
    # qtbot.mouseClick(app.ui_intro.rus_radiobtn, QtCore.Qt.LeftButton)
    # qtbot.mouseClick(app.ui_intro.bealuna_radiobtn, QtCore.Qt.LeftButton)
    # qtbot.mouseClick(app.ui_intro.letsgo_btn, QtCore.Qt.LeftButton)

    # assert bealuna_eng.MainWindowEng().show()
    # assert bealuna_eng.MainWindowEng().isActiveWindow()
    #
    # assert app.close()
    # assert app.show()
    # assert app.c is None
    # assert app.focusWidget()
    # qtbot.addWidget(bealuna_eng.MainWindowEng())

    assert isinstance(app.main_win, bealuna_eng.MainWindowEng) == True

def test_letsgo_click_bealuna_rus_win(app, qtbot):
    qtbot.mouseClick(app.ui_intro.rus_radiobtn, QtCore.Qt.LeftButton)
    qtbot.mouseClick(app.ui_intro.bealuna_radiobtn, QtCore.Qt.LeftButton)
    qtbot.mouseClick(app.ui_intro.letsgo_btn, QtCore.Qt.LeftButton)

    assert isinstance(app.main_win, bealuna_rus.MainwindowRus) == True

def test_letsgo_click_anyvsl_eng_win(app, qtbot):
    qtbot.mouseClick(app.ui_intro.eng_radiobtn, QtCore.Qt.LeftButton)
    qtbot.mouseClick(app.ui_intro.anyvsl_radiobtn, QtCore.Qt.LeftButton)
    qtbot.mouseClick(app.ui_intro.letsgo_btn, QtCore.Qt.LeftButton)

    assert isinstance(app.main_win, anyvsl_eng.MainWindowEng) == True

def test_letsgo_click_anyvsl_rus_win(app, qtbot):
    qtbot.mouseClick(app.ui_intro.rus_radiobtn, QtCore.Qt.LeftButton)
    qtbot.mouseClick(app.ui_intro.anyvsl_radiobtn, QtCore.Qt.LeftButton)
    qtbot.mouseClick(app.ui_intro.letsgo_btn, QtCore.Qt.LeftButton)

    assert isinstance(app.main_win, anyvsl_rus.MainWindowRus) == True
    assert app.close()

    # assert app.close()


