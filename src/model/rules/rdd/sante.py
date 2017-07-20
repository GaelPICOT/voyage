#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' module desiné à la gestion de la santé

    :platform: Unix, Windows
    :synopsis: gestion de la santé

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
'''
from enum import Enum
from model.rules.rdd import voyageur
import dice


class PremierSoin(object):
    """ représente des premier soin
    """


class SoinComplet(object):
    """ représente des soin complet
    """


class encaissement(object):
    """ représente un jet d'encaissement pour un personnage
    """
    class Table(Enum):
        """ table coup non-mortel ou blessures
        """
        nonmortel = 0
        blessure = 1

    def __init__(self, personnage: voyageur, lancer: int=None, pdom: int=0,
                 table: encaissement.Table=encaissement.Table.blessure):
        """ init
        """
        if lancer is None:
            lancer = dice.roll("2d10+0")
        self._personnage = personnage
        self._lancer = lancer + pdom
        self._pdom = pdom
        self._table = table


class Blessure(object):
    """ decris une blessure
    """
    class TypeB(Enum):
        """ diferant type de blessure
        """
        legere = 2
        grave = 4
        critique = 6

    def __init__(self, typeB: Blessure.TypeB=Blessure.TypeB.eraflure):
        """ init
        """
        self._type = typeB
