''' gestiobn des dés virtuel.

    :platform: Unix, Windows
    :synopsis: création et gestion de personnage

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
'''
import random


class Des(object):
    def __init__(self, value):
        self._value = value

    @property
    def roll(self):
        return random.randrange(self._value) + 1

    def __mul__(self, mult):
        return sum([self.roll for _ in range(mult)])
