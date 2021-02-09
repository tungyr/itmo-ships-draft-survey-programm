# http://johnnado.com/pyqt-qtest-example/
# https://www.riverbankcomputing.com/static/Docs/PyQt5/
# https://github.com/pytest-dev/pytest-qt
# https://pytest-qt.readthedocs.io/en/latest/reference.html#module-pytestqt.qtbot
# https://pytest-qt.readthedocs.io/en/latest/intro.html#requirements

# https://stackoverflow.com/questions/57065728/how-to-check-correct-opening-the-window-after-the-click-by-button-in-pytest-qt

import sys
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from PyQt5 import QtCore

from draft_survey import intro

import pytest

from draft_survey import intro

@pytest.fixture
def app(qtbot):
    test_intro_app = intro.IntroWindow()
    qtbot.addWidget(test_intro_app)  # we are "registering" our app object to qtbot

    return test_intro_app
#
#
# def test_label(app):
#     assert app.text_label.text() == "Hello World!"


def test_letsgo_after_click(app, qtbot):
    qtbot.mouseClick(app.ui_intro.letsgo_btn, QtCore.Qt.LeftButton)
    # assert app.main_win.show()
    assert app.close()


