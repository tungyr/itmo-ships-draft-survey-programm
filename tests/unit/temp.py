
#! /usr/bin/env python2
# -*- coding: utf-8 -*-
#
import sys
from PyQt5.QtGui import * # компоненты интерфейса
from PyQt5 import QtGui, QtWidgets

# Каждое приложение должно создать объект QApplication
# sys.argv - список аргументов командной строки
application = QtGui.QGuiApplication(sys.argv)

# QWidget - базовый класс для всех объектов интерфейса
# пользователя; если использовать для виджета конструктор
# без родителя, такой виджет станет окном
widget = QtWidget()

widget.resize(320, 240) # изменить размеры виджета
widget.setWindowTitle("Hello, World!") # установить заголовок
widget.show() # отобразить окно на экране

sys.exit(application.exec_()) # запуск основного цикла приложения