# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'intro.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Draft_survey(object):
    def setupUi(self, Draft_survey):

        Draft_survey.setObjectName("Draft_survey")
        Draft_survey.resize(400, 330)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Draft_survey.sizePolicy().hasHeightForWidth())
        Draft_survey.setSizePolicy(sizePolicy)

        self.gridLayout = QtWidgets.QGridLayout(Draft_survey)
        self.gridLayout.setObjectName("gridLayout")

        self.start_btn = QtWidgets.QPushButton(Draft_survey)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.start_btn.setFont(font)
        self.start_btn.setObjectName("start_btn")
        self.gridLayout.addWidget(self.start_btn, 5, 1, 1, 1)

        self.welcome_label = QtWidgets.QLabel(Draft_survey)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.welcome_label.setFont(font)
        self.welcome_label.setAlignment(QtCore.Qt.AlignCenter)
        self.welcome_label.setWordWrap(True)
        self.welcome_label.setIndent(-1)
        self.welcome_label.setObjectName("welcome_label")
        self.gridLayout.addWidget(self.welcome_label, 2, 1, 1, 1)

        self.bea_luna_pic = QtWidgets.QLabel(Draft_survey)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bea_luna_pic.sizePolicy().hasHeightForWidth())
        self.bea_luna_pic.setSizePolicy(sizePolicy)
        self.bea_luna_pic.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.bea_luna_pic.setMidLineWidth(1)
        self.bea_luna_pic.setText("")
        self.bea_luna_pic.setPixmap(QtGui.QPixmap("HC_BEA_LUNAcr.jpg"))
        self.bea_luna_pic.setAlignment(QtCore.Qt.AlignCenter)
        self.bea_luna_pic.setObjectName("bea_luna_pic")
        self.gridLayout.addWidget(self.bea_luna_pic, 1, 1, 1, 1)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.lang_label = QtWidgets.QLabel(Draft_survey)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lang_label.setFont(font)
        self.lang_label.setObjectName("lang_label")
        self.horizontalLayout.addWidget(self.lang_label)

        self.radiobtn_eng = QtWidgets.QRadioButton(Draft_survey)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        self.radiobtn_eng.setFont(font)
        self.radiobtn_eng.setChecked(True)
        self.radiobtn_eng.setObjectName("radiobtn_eng")

        self.buttonGroup = QtWidgets.QButtonGroup(Draft_survey)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.radiobtn_eng)
        self.horizontalLayout.addWidget(self.radiobtn_eng)

        self.radiobtn_rus = QtWidgets.QRadioButton(Draft_survey)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        self.radiobtn_rus.setFont(font)
        self.radiobtn_rus.setChecked(False)
        self.radiobtn_rus.setObjectName("radiobtn_rus")
        self.buttonGroup.addButton(self.radiobtn_rus)
        self.horizontalLayout.addWidget(self.radiobtn_rus)

        self.gridLayout.addLayout(self.horizontalLayout, 3, 1, 1, 1)

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.vessel_label = QtWidgets.QLabel(Draft_survey)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.vessel_label.setFont(font)
        self.vessel_label.setObjectName("vessel_label")
        self.horizontalLayout_2.addWidget(self.vessel_label)

        self.radiobtn_bealuna = QtWidgets.QRadioButton(Draft_survey)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        self.radiobtn_bealuna.setFont(font)
        self.radiobtn_bealuna.setChecked(True)
        self.radiobtn_bealuna.setObjectName("radiobtn_bealuna")

        self.buttonGroup_2 = QtWidgets.QButtonGroup(Draft_survey)
        self.buttonGroup_2.setObjectName("buttonGroup_2")
        self.buttonGroup_2.addButton(self.radiobtn_bealuna)
        self.horizontalLayout_2.addWidget(self.radiobtn_bealuna)

        self.radiobtn_anyvsl = QtWidgets.QRadioButton(Draft_survey)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        self.radiobtn_anyvsl.setFont(font)
        self.radiobtn_anyvsl.setChecked(False)
        self.radiobtn_anyvsl.setObjectName("radiobtn_anyvsl")
        self.buttonGroup_2.addButton(self.radiobtn_anyvsl)
        self.horizontalLayout_2.addWidget(self.radiobtn_anyvsl)

        self.gridLayout.addLayout(self.horizontalLayout_2, 4, 1, 1, 1)

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 5, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 6, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 5, 2, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 0, 1, 1, 1)

        self.retranslateUi(Draft_survey)
        QtCore.QMetaObject.connectSlotsByName(Draft_survey)

    # TODO: ?
    def retranslateUi(self, Draft_survey):
        _translate = QtCore.QCoreApplication.translate
        Draft_survey.setWindowTitle(_translate("Draft_survey", "Draft survey"))
        self.start_btn.setText(_translate("Draft_survey", "Let\'s go!"))
        self.welcome_label.setText(_translate("Draft_survey", "Welcome to application! Please choose your language and vessel."))
        self.lang_label.setText(_translate("Draft_survey", "Language:"))
        self.radiobtn_eng.setText(_translate("Draft_survey", "English"))
        self.radiobtn_rus.setText(_translate("Draft_survey", "Russian"))
        self.vessel_label.setText(_translate("Draft_survey", "Vessel:"))
        self.radiobtn_bealuna.setText(_translate("Draft_survey", "HC Bea-Luna"))
        self.radiobtn_anyvsl.setText(_translate("Draft_survey", "Any vessel"))