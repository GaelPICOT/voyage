#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' module desiné à la gestion de la santé

    :platform: Unix, Windows
    :synopsis: gestion de la santé

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
'''
from enum import Enum


class PremierSoin(object):
    """ représente des premier soin
    """


class SoinComplet(object):
    """ représente des soin complet
    """


class Blessure(object):
    """ decris une blessure
    """
    class TypeB(Enum):
        """ diferant type de blessure
        """
        eraflure = 0
        legere = 2
        grave = 4
        critique = 6

    def __init__(self, typeB=Blessure.TypeB.eraflure):
        """ init
        """
        self._type = typeB
