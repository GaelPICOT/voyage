#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' module pour la gestion de la fenetre gestion de personnage.

    :platform: Unix, Windows
    :synopsis: fenetre gestion de personnage

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
'''
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi
import os
from model.rules.rdd.creation_perso import PersonnageCreateur


class PersonnageWindow(QWidget):
    """ fenetre principale
    """
    def __init__(self, parent=None, mdi_area=None, personnage=None,
                 perso_creat=None):
        """ init
        """
        if personnage is None:
            if perso_creat is None:
                self._personnage_createur = PersonnageCreateur()
            else:
                self._personnage_createur = perso_creat
        QWidget.__init__(self, parent)
        current_rep = os.path.abspath(os.path.split(__file__)[0])
        loadUi(os.path.join(current_rep, "personnage.ui"), self)
        self._mdi_area = mdi_area
        self.revant_button.clicked.connect(self.change_reve_statu)

    def change_reve_statu(self):
        """ change haut revant en vrai revant et inversement
        """
        self.revant_button.setStyleSheet("QPushButton {color : blue; }")
