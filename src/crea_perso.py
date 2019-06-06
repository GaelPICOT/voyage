#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' module pour démarer le programme de création de personnage seulement.

    :platform: Unix, Windows
    :synopsis: programme de création de personnage

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
'''
from PyQt5.QtWidgets import QApplication
from view.personnage import PersonnageWindow
import sys


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = PersonnageWindow()
    main_window.show()

    sys.exit(app.exec_())
