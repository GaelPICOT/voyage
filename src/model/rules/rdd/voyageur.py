#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' élément pour la création et la gestion de personnage.

    :platform: Unix, Windows
    :synopsis: création et gestion de personnage

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
'''
import dice
import math
from model.rules.rdd.competance import Caracteristiques, Competances
from model.rules.rdd.temps import DateTime, heures


class ConteurLimiteError(Exception):
    """ conteur depassant une limites
    """
    def __init__(self, depacement=0, is_inf=True, info=None):
        """ init
        """
        self._depacement = depacement
        self._is_inf = is_inf
        self._info = info

    @property
    def is_inf(self):
        """
        """
        return self._is_inf

    @property
    def depacement(self):
        """ valeur de depacement
        """
        return self._depacement

    @property
    def info(self):
        """
        """
        return self._info


class FatigueSegment(object):
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
        self._segments = {0: [FatigueSegment(2), FatigueSegment(3),
                              FatigueSegment(3)],
                          -1: [FatigueSegment(2), FatigueSegment(3),
                               FatigueSegment(3)],
                          -2: FatigueSegment(2),
                          -3: FatigueSegment(3),
                          -4: FatigueSegment(3),
                          -5: FatigueSegment(2),
                          -6: FatigueSegment(3),
                          -7: FatigueSegment(3)
                          }
        self._malus = 0
        self._seg_lineaire = self._segments[0] + self._segments[-1]
        for i in range(6):
            self._seg_lineaire.append(self._segments[-2-i])
        # limite à la récupération de point de fatigue (ex : point d'endurence
        # manquant)
        self._limite_recuperation = 0

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
        raise ConteurLimiteError(fatigue)


class Cheveux(object):
    """ decrit les cheveux d'une personne
    """
    def __init__(self):
        self._coul = "brun"  # couleur de cheveux
        self._long = "court"  # longueur de cheveux
        self._quantite = "nombreux"  # quantité de cheveux

    @property
    def coul(self):
        """ couleur de cheveu
        """
        return self._coul

    @property
    def long(self):
        """ longueur de cheveu
        """
        return self._long

    @property
    def quantite(self):
        """ quantité de cheveu
        """
        return self.quantite

    def edite_param(self, coul=None, long=None, quantite=None):
        """ edite un ou plusieur parametre des cheveux
        """
        if coul is not None:
            self._coul = coul
        if long is not None:
            self._long = long
        if quantite is not None:
            self._quantite = quantite


class SignesParticuliers(object):
    """ regroupe tous les signe particuliers
    """
    def __init__(self):
        """ init
        """
        self._nom = ""
        self._sexe = "Femme"  # peut être multiple en fonction de la race
        self._HN = heures.vaisseau  # heure de naissance
        self._beaute = 10  # beauté
        self._age_debut = 18
        self._taille = 1.7  # en m
        self._poids = 70  # en kG
        self._cheveux = Cheveux()
        self._yeux = "vert"
        self._autres = ""

    @property
    def nom(self):
        return self._nom

    @nom.setter
    def nom(self, nom):
        self._nom = nom


class Compteur(object):
    """ definit tous les compteur (vie, endurence,...)
    """
    def __init__(self, vinit, vmax=None, negatif=0, valeur=None):
        """ init
        """
        self._vinit = vinit
        if vmax is None:
            self._vmax = vinit
        else:
            self._vmax = vmax
        self._negatif = negatif
        if valeur is None:
            self._valeur = vinit
        else:
            self._valeur = valeur

    @property
    def vinit(self):
        """ return valeur vinit
        """
        return self._vinit

    @vinit.setter
    def vinit(self, vinit):
        """ setter vinit
        """
        self._vinit = vinit
        self._valeur = vinit

    @property
    def vmax(self):
        """ return valeur vinit
        """
        return self._vinit

    @vmax.setter
    def vmax(self, vinit):
        """ setter vinit
        """
        self._vinit = vinit

    @property
    def valeur(self):
        """  return actual value
        """
        return self._valeur

    @valeur.setter
    def valeur(self, valeur):
        """ setter valeur
        """
        self._valeur = valeur
        if self._valeur >= self._vmax:
            raise ConteurLimiteError(valeur-self._vmax, False)
        if self._valeur <= self._vinit:
            raise ConteurLimiteError(0-self._valeur)
        if self._valeur <= self._negatif:
            raise ConteurLimiteError(0-self._valeur, info="limite negative")

    @property
    def negatif(self):
        """
        """
        return self._negatif

    @negatif.setter
    def negatif(self, negatif):
        """
        """
        self._negatif = negatif

    def __iadd__(self, valeur):
        """
        """
        self._valeur += valeur
        if self._valeur >= self._vmax:
            raise ConteurLimiteError(valeur-self._vmax, False)

    def __isub__(self, valeur):
        """
        """
        self._valeur -= valeur
        if self._valeur <= self._vinit:
            raise ConteurLimiteError(0-self._valeur)
        if self._valeur <= self._negatif:
            raise ConteurLimiteError(0-self._valeur, info="limite negative")


class VraiRevant(object):
    """ ajout info vrai revant : competances de vocation
    """
    def __init__(self):
        """ init
        """
        self._vocation = []

    def ajoute_cmp_vocation(self, cmp: str):
        """ ajoute une compétence de vocation
        """
        self._vocation.append(cmp)

    @property
    def vocation(self):
        """ compétance de vocation
        """
        return self._vocation


class Personnage(object):
    """ objet permétant de créé un personnage.
    """
    def __init__(self):
        self._carac = Caracteristiques()
        self._competances = Competances()
        self._fatigue = FatigueCount()
        # points
        self._points = {"destinee": Compteur(0, 7),
                        "chance": Compteur(self._carac["Chance"].valeur)}
        # seuils
        self._seuils = {}
        # ajout gestion vie est endurence
        self._carac["Taille"].value_changed.connect(self.calculate_vie)
        self._carac["Constitution"].value_changed.connect(self.calculate_vie)
        self._carac["Volonte"].value_changed.connect(self.calculate_vie)
        self.calculate_vie()
        # ajout gestion rêve
        self._carac["Reve"].value_changed.connect(self.calculate_reve)
        self.calculate_reve()
        # + dom et enc
        self._carac["Taille"].value_changed.connect(self.calculate_p_dom)
        self._carac["Force"].value_changed.connect(self.calculate_p_dom)
        self.calculate_p_dom()
        # signe particulier
        self._signes_particuliers = SignesParticuliers()
        self._list_event = []
        if dice.roll("1d12").pop() == 1:
            self._mainhand = "ambidextre"
        else:
            self._mainhand = "droite"
        self._time = DateTime()
        self._statu_revant = VraiRevant()

    def calculate_chance(self):
        """ (re)calculate point de chance
        """
        self._points["chance"].vinit = self._carac["Chance"].valeur

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
        elif enc < 16:
            self._seuils["+dom"] = 2
        elif enc < 18:
            self._seuils["+dom"] = 3
        elif enc < 21:
            self._seuils["+dom"] = 4
        elif enc < 23:
            self._seuils["+dom"] = 5
        elif enc < 25:
            self._seuils["+dom"] = 6
        elif enc < 27:
            self._seuils["+dom"] = 7
        elif enc < 29:
            self._seuils["+dom"] = 8
        elif enc < 31:
            self._seuils["+dom"] = 9
        elif enc < 32:
            self._seuils["+dom"] = 10
        else:
            self._seuils["+dom"] = 11

    def calculate_reve(self, _=None):
        """ (re)calculate reve et seuil
        """
        if "Rêve" not in self._points.keys():
            # points de rêve
            self._points["Reve"] = self._carac["Reve"].valeur
            # seuil de rêve
            self._seuils["Reve"] = self._points["Reve"]
        else:
            if self._points["Reve"] < self._carac["Reve"].valeur:
                self._points["Reve"] = self._carac["Reve"].valeur
            if self._seuils["Reve"] < self._carac["Reve"].valeur:
                self._seuils["Reve"] = self._carac["Reve"].valeur

    def calculate_vie(self, _=None):
        """ (re)calcule la vie et la constitution et les seuilles en lien
        """
        # endurence potentiel 1
        const = self._carac["Constitution"].valeur
        taille = self._carac["Taille"].valeur
        end1 = taille + const
        # points de vie
        if "Vie" not in self._points.keys():
            self._points["Vie"] = Compteur(math.ceil(end1 / 2))
        else:
            self._points["Vie"].vinit = math.ceil(end1 / 2)
        # points d'endurence
        end2 = self._points["Vie"].valeur + self._carac["Volonte"].valeur
        if end2 >= end1:
            end = end2
        else:
            end = end1
        if "Endurence" not in self._points.keys():
            self._points["Endurence"] = Compteur(end)
        else:
            self._points["Endurence"].vinit = end
        self._fatigue.recalculate_seg(self._points["Endurence"].vinit)
        # seuil de constitution
        if const < 9:
            sc = 2
        elif const < 12:
            sc = 3
        elif const < 15:
            sc = 4
        else:
            sc = 5
        self._seuils["Constitution"] = sc
        # seuil de sustentation
        if taille < 10:
            self._seuils["Sustentation"] = 2
        elif taille < 14:
            self._seuils["Sustentation"] = 3
        else:
            self._seuils["Sustentation"] = 4
        # vie
        self._points["Vie"].negatif = sc

    def passe_chateau_dormant(self):
        """ passage de chateau dormant
        """
        if self._points["Reve"] > self._seuils["Reve"]:
            self._points["Reve"] -= 1

    def mort(self):
        """ tue le personnage
        """
        self._competances = Competances()
        self._signes_particuliers = SignesParticuliers()
        self._list_event.append("mort")

    def add_event(self, event):
        """ ajouté un evenement dans la liste d'événement
        """
        self._list_event.append(event)
        self._time += event.duree

    @property
    def statut_revant(self):
        """ statu : vrais ou haut rêvant
        """
        return self._statu_revant

    @statut_revant.setter
    def statut_revant(self, valeur):
        """ set statut rêvant
        """
        self._statu_revant = valeur

    @property
    def time(self):
        """ current timestemp du personnage
        """
        return self._time

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

    @property
    def fatigue(self):
        """ getter fatigue
        """
        return self._fatigue

    @property
    def etat_general(self):
        """ calcule l'état generale
        """
        malus_fatigue = self._fatigue.malus
        pv_manquant = self._points["Vie"].vinit - self._points["Vie"].valeur
        return malus_fatigue - pv_manquant

    @property
    def signes_particuliers(self):
        return self._signes_particuliers

    @property
    def data_dict(self):
        data = {"caracteristique": self._carac.data_dict}            
        return data

    @data_dict.setter
    def data_dict(self, value):
        """ load data from dictionnary
        """
        self._carac.data_dict = value["caracteristique"]
