#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' module desiné à la gestion des actions. ainsi que point de tâches et de
qualités.

    :platform: Unix, Windows
    :synopsis: gestion des actions

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
'''
import math
import dice


class ResultatAction(object):
    """ resultat d'une action
    """
    def __init__(self, pc_reussit):
        """ init
        """
        self._lancer = dice.roll("1d100+0")
        self._reusite = pc_reussit <= self._lancer


def action(self, competance=10, ajustement=0):
    """ jouer une action
    """
    pc_reussit = 0
    if ajustement >= -8:
        pc_reussit = math.floor(competance * ((ajustement + 10) / 2))
    elif ajustement >= -10:
        pc_reussit = math.floor(competance / (ajustement * 2))
    return ResultatAction(pc_reussit)
