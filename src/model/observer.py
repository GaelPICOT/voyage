#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' module pour géré les signaux sans Qt.

    :platform: Unix, Windows
    :synopsis: gestion des signaux sans Qt

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
'''


class Observable(object):
    """ class pour les objet observable
    """
    def __init__(self):
        """ initialisation
        """
        self.observer = []

    def emit(self, option=None):
        """ emit signal to all observer
        """
        for observer in self.observer:
            if option is not None:
                observer(option)
            else:
                observer()

    def connect(self, observer):
        self.observer.append(observer)
