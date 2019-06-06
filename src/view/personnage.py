#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' module pour la gestion de la fenetre gestion de personnage.

    :platform: Unix, Windows
    :synopsis: fenetre gestion de personnage

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
'''
from PyQt5.QtWidgets import QWidget, QSpinBox, QLabel
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
        QWidget.__init__(self, parent)
        current_rep = os.path.abspath(os.path.split(__file__)[0])
        loadUi(os.path.join(current_rep, "personnage.ui"), self)
        self._mdi_area = mdi_area
        if personnage is None:
            self._init_creation(perso_creat)
        else:
            self._init_personnage(personnage)

    def _init_creation(self, perso_creat):
        if perso_creat is None:
            self._personnage_createur = PersonnageCreateur()
        else:
            self._personnage_createur = perso_creat
        self._personnage = self._personnage_createur.personnage
        self.revant_button.clicked.connect(self.change_reve_statu)
        for child in self.frame.children() + self.frame_2.children():
            if isinstance(child, QSpinBox):
                child.valueChanged.connect(self.changed_carac_creator(child.objectName()[5:], child))
                self.findChild(QLabel, "label_" + child.objectName()[5:]).setVisible(False)

    def changed_carac_creator(self, caract, spin):
        #TODO: corect changement de taille inférieur à 4+Force n'influ pas sur la force
        caract = caract[0].upper() + caract[1:]
        def changed_carac(value):
            old_value = self._personnage.caracteristiques[caract].valeur
            if self.carac_spin.value() == 0 and old_value < value:
                spin.setValue(old_value)
                return
            self._personnage.caracteristiques[caract].valeur = value
            if self._personnage.caracteristiques[caract].valeur == value:
                if value > old_value:
                    self.carac_spin.setValue(self.carac_spin.value()-1)
                elif value < old_value:
                    self.carac_spin.setValue(self.carac_spin.value()+1)
            else:
                spin.setValue(self._personnage.caracteristiques[caract].valeur)
        return changed_carac

    def _init_personnage(self, personnage):
        """ init for existant personnage
        """
        for child in self.frame.children() + self.frame_2.children():
            if isinstance(child, QSpinBox):
                child.setVisible(False)
        self._personnage = personnage

    def change_reve_statu(self):
        """ change haut revant en vrai revant et inversement
        """
        if self.revant_button.text() != "Haut-rêvant":
            self.revant_button.setStyleSheet("QPushButton {color : blue; }")
            self.revant_button.setText("Haut-rêvant")
            self._personnage.haut_revant = True
        else:
            self.revant_button.setStyleSheet("QPushButton {color : green; }")
            self.revant_button.setText("Vrai-rêvant")
            self._personnage.haut_revant = False
