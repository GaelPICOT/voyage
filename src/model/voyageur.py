#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' élément pour la création et la gestion de personnage.

    :platform: Unix, Windows
    :synopsis: création et gestion de personnage

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
'''
import dice
import model.temps
import math
from model.competance import Caracteristiques, Competances


class FatigueSegmet(object):
    """ modelise un segment de fatique
    """
    def __init__(self, size):
        """ initialisation
        """
        self._size = size
        self._used = 0

    @property
    def taille(self):
        """ size getter
        """
        return self._size

    @property
    def used(self):
        """ used getter
        """
        return self._used

    @property
    def plain(self):
        """ return True si le segment et plain
        """
        if self._used >= self._size:
            return True
        else:
            return False

    def resize(self, new_size):
        """ redefine size
        """
        self._size = new_size

    def recupere(self):
        """ recupere le segment
        """
        self._used = 0

    def add_fatigue(self, fatigue):
        """ ajoute de la fatigue
        """
        self._used += fatigue
        if self._used > self._size:
            rest = self._used - self._size
            self._used = self._size
            return rest
        else:
            return 0


class FatigueCount(object):
    """ conteur de fatigue
    """
    def __init__(self):
        """ initialisation
        """
        self._segments = {0: [FatigueSegmet(2), FatigueSegmet(3),
                              FatigueSegmet(3)],
                          -1: [FatigueSegmet(2), FatigueSegmet(3),
                               FatigueSegmet(3)],
                          -2: FatigueSegmet(2),
                          -3: FatigueSegmet(3),
                          -4: FatigueSegmet(3),
                          -5: FatigueSegmet(2),
                          -6: FatigueSegmet(3),
                          -7: FatigueSegmet(3)
                          }
        self._malus = 0
        self._seg_lineaire = self._segments[0] + self._segments[-1]
        for i in range(6):
            self._seg_lineaire.append(self._segments[-2-i])

    @property
    def segments(self):
        """ getter segments
        """
        return self._segments

    def recalculate_seg(self, endurence=16):
        """ (re)calculate segment
        """
        v_max = (endurence // 6) + 1
        mod_end = endurence % 6

        def assigne_value(segment1, segmet2, mod_trans):
            if mod_end > mod_trans:
                segment1.resize(v_max)
                segmet2.resize(v_max)
            else:
                segment1.resize(v_max-1)
                segmet2.resize(v_max-1)
        assigne_value(self._segments[-7], self._segments[-1][2], 0)
        assigne_value(self._segments[-4], self._segments[0][2], 1)
        assigne_value(self._segments[-6], self._segments[-1][1], 2)
        assigne_value(self._segments[-3], self._segments[0][1], 3)
        assigne_value(self._segments[-5], self._segments[-1][0], 4)
        assigne_value(self._segments[-2], self._segments[0][0], 5)

    @property
    def malus(self):
        """ retourne le malus du à la fatigue
        """
        if self._segments[-1][0].used == 0:
            return 0
        if self._segments[-2].used == 0:
            return -1
        for i in range(6):
            if not self._segments[-2-i].plain:
                return -2-i
        return -7

    def recuperation(self):
        """ recuperation de fatigue
        """
        seg_pres = None
        for segment in self._seg_lineaire:
            if not segment.plain:
                if segment.used < segment.taille/2:
                    if seg_pres is not None:
                        seg_pres.recupere()
                elif segment.used == 0:
                    segment = seg_pres
                segment.recupere()
                break
            seg_pres = segment

    def add_fatigue(self, fatigue):
        """ ajoute de la fatigue
        """
        for segment in self._seg_lineaire:
            if not segment.plain:
                fatigue = segment.add_fatigue(fatigue)
                if fatigue == 0:
                    return 0
        return fatigue


class Personnage(object):
    """ objet permétant de créé un personnage.
    """
    def __init__(self):
        self._carac = Caracteristiques()
        self._competances = Competances()
        self._fatigue = FatigueCount()
        # points
        self._points = {}
        # seuils
        self._seuils = {}
        # ajout gestion vie est endurence
        self._carac["Taille"].value_changed.connect(self.calculate_vie)
        self._carac["Constitution"].value_changed.connect(self.calculate_vie)
        self._carac["Volonté"].value_changed.connect(self.calculate_vie)
        self.calculate_vie()
        # ajout gestion rêve
        self._carac["Rêve"].value_changed.connect(self.calculate_reve)
        self.calculate_reve()
        # + dom et enc
        self._carac["Taille"].value_changed.connect(self.calculate_p_dom)
        self._carac["Force"].value_changed.connect(self.calculate_p_dom)
        self.calculate_p_dom()
        # signe particulier
        # heure de naissance
        self._h_nais = model.temps.heures.vaisseau
        # age
        self._age = 18
        if dice.roll("1d12").pop() == 1:
            self._mainhand = "ambidextre"
        else:
            self._mainhand = "droite"

    def calculate_p_dom(self, _=None):
        """ (re)calculate +dom et encombrement
        """
        taille = self._carac["Taille"].valeur
        force = self._carac["Force"].valeur
        enc = (taille + force)/2
        # seuil d'encombrement
        self._seuils["Encombrement"] = enc
        # +dom
        if enc < 8:
            self._seuils["+dom"] = -1
        elif enc < 12:
            self._seuils["+dom"] = 0
        elif enc < 14:
            self._seuils["+dom"] = 1
        else:
            self._seuils["+dom"] = 2

    def calculate_reve(self, _=None):
        """ (re)calculate reve et seuil
        """
        if "Rêve" not in self._points.keys():
            # points de rêve
            self._points["Rêve"] = self._carac["Rêve"].valeur
            # seuil de rêve
            self._seuils["Rêve"] = self._points["Rêve"]
        else:
            if self._points["Rêve"] < self._carac["Rêve"].valeur:
                self._points["Rêve"] = self._carac["Rêve"].valeur
            if self._seuils["Rêve"] < self._carac["Rêve"].valeur:
                self._seuils["Rêve"] = self._carac["Rêve"].valeur

    def calculate_vie(self, _=None):
        """ (re)calcule la vie et la constitution et les seuilles en lien
        """
        # endurence potentiel 1
        const = self._carac["Constitution"].valeur
        taille = self._carac["Taille"].valeur
        end1 = taille + const
        # points de vie
        self._points["Vie"] = math.ceil(end1 / 2)
        # points d'endurence
        end2 = self._points["Vie"] + self._carac["Volonté"].valeur
        if end2 >= end1:
            self._points["Endurence"] = end2
        else:
            self._points["Endurence"] = end1
        self._fatigue.recalculate_seg(self._points["Endurence"])
        # seuil de constitution
        if const < 9:
            self._seuils["Constitution"] = 2
        elif const < 12:
            self._seuils["Constitution"] = 3
        elif const < 15:
            self._seuils["Constitution"] = 4
        else:
            self._seuils["Constitution"] = 5
        # seuil de sustentation
        if taille < 10:
            self._seuils["Sustentation"] = 2
        elif taille < 14:
            self._seuils["Sustentation"] = 3
        else:
            self._seuils["Sustentation"] = 4

    def passe_chateau_dormant(self):
        """ passage de chateau dormant
        """
        if self._points["Rêve"] > self._seuils["Rêve"]:
            self._points["Rêve"] -= 1

    @property
    def points(self):
        """ property to acces to points
        """
        return self._points

    @property
    def ceuils(self):
        """ property to acces to seuils
        """
        return self._seuils

    @property
    def main_principale(self):
        """ property pour la main principale
        """
        return self._mainhand

    @property
    def caracteristiques(self):
        """ property pour accédé aux caracteristiques
        """
        return self._carac

    @property
    def competances(self):
        """
        """
        return self._competances
