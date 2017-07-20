#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' module desiné à la gestion du haut-rêve.

    :platform: Unix, Windows
    :synopsis: gestion du haut-rêve

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
'''
from enum import Enum


class CaseTMR(object):
    """ représente une case en TMR
    """
    class Categorie(Enum):
        cite = 0
        coline = 1
        desert = 2
        desolation = 3
        foret = 4
        gouffre = 5
        monts = 6
        necropole = 7
        plaine = 8
        pont = 9
        sanctuaire = 10
        fleuve = 11
        lac = 12
        marais = 13

    def __init__(self):
        """ init
        """


class TMR(object):
    """ Represente les TMR pour une personne
    """


class Sort(object):
    """ représente un sort
    """
    def __init__(self):
        """ init
        """


class Rituel(Sort):
    """ représente un rituel
    """


class HautReve(object):
    """ gestion du haut-rêve
    """
    def __init__(self):
        """ init
        """
        # point de sort
        self._pt_sort = {"Oniros": 0, "Hypnos": 0, "Narcos": 0, "Thanatos": 0}
