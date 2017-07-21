#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' module pour démarer le programme.

    :platform: Unix, Windows
    :synopsis: demarage

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
'''
from PyQt5.QtWidgets import QApplication
from view.mainwindow import MainWindow
import sys


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.showMaximized()

    sys.exit(app.exec_())
