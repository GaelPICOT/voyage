#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' élément pour la gestion de l'équipement.

    :platform: Unix, Windows
    :synopsis: création et gestion de personnage

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
'''


class TypeObjet(object):
    """ decrit un type d'objet. (son prix moyen, où le trouvé...)
    """
    def __init__(self):
        """ init
        """
        # prix en denier
        self._prix = 1
        # encombrement
        self._enc = 0

    @property
    def encombrement(self):
        """ encombrement
        """
        return self._enc


class Objet(TypeObjet):
    """ decrit une "instence" d'objet
    """
    def __init__(self, type_objet: TypeObjet=None):
        """ init
        """
        self._type_objet = type_objet
        # encombrement
        self._enc = 0


class Contenant(Objet):
    """ contenant divers
    """
    def __init__(self):
        """ init
        """
        self._list_objet = []
        # encombrement
        self._enc = 0

    @property
    def encombrement(self):
        """ calcule encombrement contenant + contenu
        """
        enc = self._enc
        for objet in self._list_objet:
            enc += objet.encombrement
        return enc
