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


class PersonnageWindow(QWidget):
    """ fenetre principale
    """
    def __init__(self):
        """ init
        """
        QWidget.__init__(self)
        current_rep = os.path.abspath(os.path.split(__file__)[0])
        loadUi(os.path.join(current_rep, "personnage.ui"), self)
