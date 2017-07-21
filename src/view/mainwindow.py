#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' module pour la gestion de la fenetre principale.

    :platform: Unix, Windows
    :synopsis: fenetre principale

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
'''
from PyQt5.QtWidgets import QMainWindow, QMdiArea
from PyQt5.uic import loadUi
from view.listperso import ListPerso
import os


class MainWindow(QMainWindow):
    """ fenetre principale
    """
    def __init__(self):
        """ init
        """
        QMainWindow.__init__(self)
        current_rep = os.path.abspath(os.path.split(__file__)[0])
        loadUi(os.path.join(current_rep, "mainwindow.ui"), self)
        self.personnages_button.clicked.connect(self.ouvrir_list_perso)

    def ouvrir_list_perso(self):
        """ ouvre la list de personnage
        """
        name_mdi = self.tabWidget.currentWidget().objectName()[:-4] + "_mdi"
        mdi_area = self.findChild(QMdiArea, name_mdi)
        self._new_list_perso = ListPerso()
        mdi_area.addSubWindow(self._new_list_perso)
        self._new_list_perso.show()
