#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' module desiné à la gestion du haut-rêve.

    :platform: Unix, Windows
    :synopsis: gestion du haut-rêve

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
'''


class Sort(object):
    """ représente un sort
    """
    def __init__(self, case_tmr):
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
