#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' élément pour la création et la gestion de personnage.

    :platform: Unix, Windows
    :synopsis: création et gestion de personnage

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
'''
import dice
from model.competance import Caracteristiques


class Personnage(object):
    """ objet permétant de créé un personnage.
    """
    def __init__(self):
        self._caractéristiques = Caracteristiques()
        if dice.roll("d12").pop() == 1:
            self._mainhand = "ambidextre"
        else:
            self._mainhand = "droite"
