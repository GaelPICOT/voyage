#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' module pour la gestion de la fenetre principale.

    :platform: Unix, Windows
    :synopsis: fenetre principale

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
'''
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi
from view.personnage import PersonnageWindow
import os


class ListPerso(QWidget):
    """ fenetre principale
    """
    def __init__(self, parent=None, mdi_area=None):
        """ init
        """
        QWidget.__init__(self, parent)
        current_rep = os.path.abspath(os.path.split(__file__)[0])
        loadUi(os.path.join(current_rep, "listperso.ui"), self)
        self.nouveau_pero_button.clicked.connect(self.nouveau_perso)
        self._list_sub_windows = []
        self._mdi_area = mdi_area

    def nouveau_perso(self):
        """ création de nouveau personnage
        """
        new_perso = PersonnageWindow(mdi_area=self._mdi_area)
        self._mdi_area.addSubWindow(new_perso)
        new_perso.show()
        self._list_sub_windows.append(new_perso)
