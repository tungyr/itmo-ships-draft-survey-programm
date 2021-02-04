# http://johnnado.com/pyqt-qtest-example/

import sys
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest

from draft_survey import intro

# first_test = QTest()

# if QTest.mousePress(first_test, intro.bealuna_eng.qDrawWinButton(), ):
#    print('pressed')

QTest.mousePress(intro.mainWin)