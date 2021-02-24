import pytest
from PyQt5 import QtCore

from draft_survey.widgets import bealuna_eng
from draft_survey import intro

@pytest.fixture
def app(qtbot):
    test_intro_app = bealuna_eng.MainWindowBealunaEng()
    qtbot.addWidget(test_intro_app)
    return test_intro_app

def test_back_to_main_menu_button(app, qtbot):
    qtbot.mouseClick(app.ui.main_menu, QtCore.Qt.LeftButton)
    assert isinstance(app.main_win, intro.IntroWindow) == True