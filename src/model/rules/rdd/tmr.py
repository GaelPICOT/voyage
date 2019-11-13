#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' module desiné à la gestion du TMR par default.
A était créé à partir de https://github.com/Cyol/rdd/blob/master/js/tmr.js

    :platform: Unix, Windows
    :synopsis: gestion du haut-rêve

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
'''
from enum import Enum


class CaseTMR(object):
    """ représente une case en TMR
    """

    default_notationX = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                         'K', 'L', 'M']

    class Categorie(Enum):
        CITE = 0
        COLINE = 1
        DESERT = 2
        DESOLATION = 3
        FORET = 4
        GOUFFRE = 5
        MONTS = 6
        NECROPOLE = 7
        PLAINE = 8
        PONT = 9
        SANCTUAIRE = 10
        FLEUVE = 11
        LAC = 12
        MARAIS = 13

        @classmethod
        def special_names(cls, cat_to_name=True):
            cat_list = (cls.CITE, cls.FORET, cls.DESERT, cls.NECROPOLE,
                        cls.DESOLATION)
            name_list = ("cité", "forêt", "désert", "nécropole", "désolation")
            if cat_to_name:
                return {cat_list[i]: name_list[i]
                        for i in range(len(cat_list))}
            else:
                return {name_list[i]: cat_list[i]
                        for i in range(len(cat_list))}

        @classmethod
        def get_from_name(cls, name):
            return cls.special_names(False)[name]

        @property
        def is_humide(self):
            return self in [CaseTMR.Categorie.LAC, CaseTMR.Categorie.FLEUVE,
                            CaseTMR.Categorie.MARAIS]

        def __str__(self):
            special_names = self.special_names()
            if self in special_names.keys():
                return special_names[self]
            return self.name.lower()

    def __init__(self, coord_x, coord_y: int, categorie: Categorie, nom: str):
        """ init
        """
        if type(coord_x) is not int:
            coord_x = CaseTMR.default_notationX.index(coord_x.upper())+1
        self._coord_x = coord_x
        self._coord_y = coord_y
        self._categorie = categorie
        self._nom = nom
        # liste des bonus sort en réserve par voie au format [sort, paramétre]
        self._reserve = {"Oniros": [], "Hypnos": [], "Narcos": [], "Thanatos": []}
        # liste des bonus de case au format [sort, bonus]
        self._bonus = []
        self._humide = categorie.is_humide

    @property
    def rep_dic(self):
        rep_dic = {}
        rep_dic['coord_x'] = self._coord_x
        rep_dic['coord_y'] = self._coord_y
        rep_dic['nom'] = self._nom
        rep_dic['categorie'] = str(self._categorie)
        return rep_dic

    @property
    def nom(self) -> str:
        """ retourne le noù
        """
        return self._nom

    def __str__(self):
        return str(self._categorie) + " " + self.nom


default_TMR = (("A", 1, CaseTMR.Categorie.CITE, "VIDE"),
               ("A", 2, CaseTMR.Categorie.DESERT, "de MIEUX"),
               ("A", 3, CaseTMR.Categorie.DESOLATION, "de DEMAIN"),
               ("A", 4, CaseTMR.Categorie.FORET, "de FALCONAX"),
               ("A", 5, CaseTMR.Categorie.PLAINE, "de TRILKH"),
               ("A", 6, CaseTMR.Categorie.NECROPOLE, "de ZNIAK"),
               ("A", 7, CaseTMR.Categorie.PLAINE, "de l'ARC"),
               ("A", 8, CaseTMR.Categorie.GOUFFRE, "de SHOK"),
               ("A", 9, CaseTMR.Categorie.COLINE, "de KORREX"),
               ("A", 10, CaseTMR.Categorie.SANCTUAIRE, "d'OLIS"),
               ("A", 11, CaseTMR.Categorie.DESOLATION, "d'HIER"),
               ("A", 12, CaseTMR.Categorie.PLAINE, "SAGES"),
               ("A", 13, CaseTMR.Categorie.FLEUVE, ""),
               ("A", 14, CaseTMR.Categorie.COLINE, "de STOLIS"),
               ("A", 15, CaseTMR.Categorie.CITE, "de MIELH"),
               ("B", 1, CaseTMR.Categorie.PLAINE, "d'ASSORH"),
               ("B", 2, CaseTMR.Categorie.COLINE, "de DAWELL"),
               ("B", 3, CaseTMR.Categorie.PLAINE, "de RUBEGA"),
               ("B", 4, CaseTMR.Categorie.MONTS, "CRÂNEURS"),
               ("B", 5, CaseTMR.Categorie.COLINE, "de TANEGV"),
               ("B", 6, CaseTMR.Categorie.FORET, "de BUST"),
               ("B", 7, CaseTMR.Categorie.MARAIS, "BLUANTS"),
               ("B", 8, CaseTMR.Categorie.FLEUVE, ""),
               ("B", 9, CaseTMR.Categorie.LAC, "de LUCRE"),
               ("B", 10, CaseTMR.Categorie.MONTS, "SALÉS"),
               ("B", 11, CaseTMR.Categorie.CITE, "de BRILZ"),
               ("B", 12, CaseTMR.Categorie.FLEUVE, ""),
               ("B", 13, CaseTMR.Categorie.GOUFFRE, "des LITIGES"),
               ("B", 14, CaseTMR.Categorie.NECROPOLE, "de GORLO"),
               ("C", 1, CaseTMR.Categorie.NECROPOLE, "de KROAK"),
               ("C", 2, CaseTMR.Categorie.MARAIS, "GLIGNANTS"),
               ("C", 3, CaseTMR.Categorie.FLEUVE, ""),
               ("C", 4, CaseTMR.Categorie.PONT, "de GIOLI"),
               ("C", 5, CaseTMR.Categorie.MARAIS, "FLOUANTS"),
               ("C", 6, CaseTMR.Categorie.CITE, "PAVOIS"),
               ("C", 7, CaseTMR.Categorie.FLEUVE, ""),
               ("C", 8, CaseTMR.Categorie.FORET, "TURMIDE"),
               ("C", 9, CaseTMR.Categorie.MONTS, "TUMÉFIÉS"),
               ("C", 10, CaseTMR.Categorie.MARAIS, "de DOM"),
               ("C", 11, CaseTMR.Categorie.PONT, "de ROI"),
               ("C", 12, CaseTMR.Categorie.LAC, "de FRICASA"),
               ("C", 13, CaseTMR.Categorie.DESERT, "de NEIGE"),
               ("C", 14, CaseTMR.Categorie.FORET, "de BISSAM"),
               ("C", 15, CaseTMR.Categorie.PLAINE, "de TOUÉ"),
               ("D", 1, CaseTMR.Categorie.FLEUVE, ""),
               ("D", 2, CaseTMR.Categorie.CITE, "de FROST"),
               ("D", 3, CaseTMR.Categorie.GOUFFRE, "d'OKI"),
               ("D", 4, CaseTMR.Categorie.LAC, "de FOAM"),
               ("D", 5, CaseTMR.Categorie.FLEUVE, ""),
               ("D", 6, CaseTMR.Categorie.FLEUVE, ""),
               ("D", 7, CaseTMR.Categorie.PLAINE, "d'AFFA"),
               ("D", 8, CaseTMR.Categorie.CITE, "d'OLAK"),
               ("D", 9, CaseTMR.Categorie.PONT, "d'ORX"),
               ("D", 10, CaseTMR.Categorie.FLEUVE, ""),
               ("D", 11, CaseTMR.Categorie.DESOLATION, "de PARTOUT"),
               ("D", 12, CaseTMR.Categorie.COLINE, "d'HUAÏ"),
               ("D", 13, CaseTMR.Categorie.CITE, "SORDIDE"),
               ("D", 14, CaseTMR.Categorie.SANCTUAIRE, "PLAT"),
               ("E", 1, CaseTMR.Categorie.MONTS, "de KANAÏ"),
               ("E", 2, CaseTMR.Categorie.PLAINE, "de FIASK"),
               ("E", 3, CaseTMR.Categorie.FORET, "d'ESTOUBH"),
               ("E", 4, CaseTMR.Categorie.PLAINE, "d'ORTI"),
               ("E", 5, CaseTMR.Categorie.MONTS, "BRÛLANTS"),
               ("E", 6, CaseTMR.Categorie.SANCTUAIRE, "de PLAINE"),
               ("E", 7, CaseTMR.Categorie.FORET, "de GLUSKS"),
               ("E", 8, CaseTMR.Categorie.PLAINE, "d'IOLISE"),
               ("E", 9, CaseTMR.Categorie.FLEUVE, ""),
               ("E", 10, CaseTMR.Categorie.GOUFFRE, "de JUNK"),
               ("E", 11, CaseTMR.Categorie.LAC, "de GLINSTER"),
               ("E", 12, CaseTMR.Categorie.MONTS, "AJOURÉS"),
               ("E", 13, CaseTMR.Categorie.PLAINE, "de XNEZ"),
               ("E", 14, CaseTMR.Categorie.MONTS, "de QUATH"),
               ("E", 15, CaseTMR.Categorie.FORET, "des FURIES"),
               ("F", 1, CaseTMR.Categorie.CITE, "GLAUQUE"),
               ("F", 2, CaseTMR.Categorie.LAC, "de MISÈRE"),
               ("F", 3, CaseTMR.Categorie.FLEUVE, ""),
               ("F", 4, CaseTMR.Categorie.FLEUVE, ""),
               ("F", 5, CaseTMR.Categorie.CITE, "de PANOPLE"),
               ("F", 6, CaseTMR.Categorie.FLEUVE, ""),
               ("F", 7, CaseTMR.Categorie.FLEUVE, ""),
               ("F", 8, CaseTMR.Categorie.LAC, "des CHATS"),
               ("F", 9, CaseTMR.Categorie.PLAINE, "de FOE"),
               ("F", 10, CaseTMR.Categorie.MARAIS, "ZULTANTS"),
               ("F", 11, CaseTMR.Categorie.CITE, "de NOAPE"),
               ("F", 12, CaseTMR.Categorie.NECROPOLE, "de THROAT"),
               ("F", 13, CaseTMR.Categorie.FORET, "des CRIS"),
               ("F", 14, CaseTMR.Categorie.PLAINE, "BRISÉES"),
               ("G", 1, CaseTMR.Categorie.DESOLATION, "de JAMAIS"),
               ("G", 2, CaseTMR.Categorie.MARAIS, "NUISANTS"),
               ("G", 3, CaseTMR.Categorie.GOUFFRE, "de SUN"),
               ("G", 4, CaseTMR.Categorie.SANCTUAIRE, "BLANC"),
               ("G", 5, CaseTMR.Categorie.PONT, "d'IK"),
               ("G", 6, CaseTMR.Categorie.MARAIS, "GLUTANTS"),
               ("G", 7, CaseTMR.Categorie.CITE, "de TERWA"),
               ("G", 8, CaseTMR.Categorie.PLAINE, "SANS JOIE"),
               ("G", 9, CaseTMR.Categorie.DESERT, "de SEL"),
               ("G", 10, CaseTMR.Categorie.CITE, "de SERGAL"),
               ("G", 11, CaseTMR.Categorie.FLEUVE, ""),
               ("G", 12, CaseTMR.Categorie.PLAINE, "de LUFMIL"),
               ("G", 13, CaseTMR.Categorie.PLAINE, "CALCAIRES"),
               ("G", 14, CaseTMR.Categorie.DESERT, "de SEK"),
               ("G", 15, CaseTMR.Categorie.PLAINE, "des SOUPIRS"),
               ("H", 1, CaseTMR.Categorie.LAC, "d'ANTICALME"),
               ("H", 2, CaseTMR.Categorie.COLINE, "de PARTA"),
               ("H", 3, CaseTMR.Categorie.FORET, "de GANNA"),
               ("H", 4, CaseTMR.Categorie.PLAINE, "de PSARK"),
               ("H", 5, CaseTMR.Categorie.DESERT, "de KRANE"),
               ("H", 6, CaseTMR.Categorie.MONTS, "GURDES"),
               ("H", 7, CaseTMR.Categorie.GOUFFRE, "de KAFPA"),
               ("H", 8, CaseTMR.Categorie.FORET, "d'OURF"),
               ("H", 9, CaseTMR.Categorie.COLINE, "de NOIRSEUL"),
               ("H", 10, CaseTMR.Categorie.PLAINE, "NOIRES"),
               ("H", 11, CaseTMR.Categorie.FLEUVE, ""),
               ("H", 12, CaseTMR.Categorie.COLINE, "de TOOTH"),
               ("H", 13, CaseTMR.Categorie.DESOLATION, "de RIEN"),
               ("H", 14, CaseTMR.Categorie.PLAINE, "BLANCHES"),
               ("I", 1, CaseTMR.Categorie.PLAINE, "GRISES"),
               ("I", 2, CaseTMR.Categorie.FORET, "FADE"),
               ("I", 3, CaseTMR.Categorie.MONTS, "GRINÇANTS"),
               ("I", 4, CaseTMR.Categorie.PLAINE, "de XIAX"),
               ("I", 5, CaseTMR.Categorie.DESOLATION, "de TOUJOURS"),
               ("I", 6, CaseTMR.Categorie.NECROPOLE, "de XOTAR"),
               ("I", 7, CaseTMR.Categorie.PLAINE, "de TROO"),
               ("I", 8, CaseTMR.Categorie.FLEUVE, ""),
               ("I", 9, CaseTMR.Categorie.FLEUVE, ""),
               ("I", 10, CaseTMR.Categorie.LAC, "WANITO"),
               ("I", 11, CaseTMR.Categorie.PONT, "de YALM"),
               ("I", 12, CaseTMR.Categorie.GOUFFRE, "ABIMEUX"),
               ("I", 13, CaseTMR.Categorie.MONTS, "BIGLEUX"),
               ("I", 14, CaseTMR.Categorie.CITE, "DESTITUÉE"),
               ("I", 15, CaseTMR.Categorie.MONTS, "des DRAGÉES"),
               ("J", 1, CaseTMR.Categorie.MONTS, "FAINÉANTS"),
               ("J", 2, CaseTMR.Categorie.DESERT, "de POLY"),
               ("J", 3, CaseTMR.Categorie.CITE, "VENIN"),
               ("J", 4, CaseTMR.Categorie.COLINE, "d'ENCRE"),
               ("J", 5, CaseTMR.Categorie.MARAIS, "de JAB"),
               ("J", 6, CaseTMR.Categorie.LAC, "d'IAUPE"),
               ("J", 7, CaseTMR.Categorie.FLEUVE, ""),
               ("J", 8, CaseTMR.Categorie.MONTS, "BARASK"),
               ("J", 9, CaseTMR.Categorie.MARAIS, "GRONCHANTS"),
               ("J", 10, CaseTMR.Categorie.FLEUVE, ""),
               ("J", 11, CaseTMR.Categorie.PLAINE, "de MILTIAR"),
               ("J", 12, CaseTMR.Categorie.CITE, "FOLLE"),
               ("J", 13, CaseTMR.Categorie.GOUFFRE, "de GROMPH"),
               ("J", 14, CaseTMR.Categorie.DESERT, "de SANIK"),
               ("K", 1, CaseTMR.Categorie.CITE, "d'ONKAUSE"),
               ("K", 2, CaseTMR.Categorie.FORET, "TAMÉE"),
               ("K", 3, CaseTMR.Categorie.PLAINE, "de DOIS"),
               ("K", 4, CaseTMR.Categorie.PONT, "de FAH"),
               ("K", 5, CaseTMR.Categorie.FLEUVE, ""),
               ("K", 6, CaseTMR.Categorie.DESOLATION, "de POOR"),
               ("K", 7, CaseTMR.Categorie.CITE, "de KOLIX"),
               ("K", 8, CaseTMR.Categorie.DESERT, "de FUMÉE"),
               ("K", 9, CaseTMR.Categorie.SANCTUAIRE, "NOIR"),
               ("K", 10, CaseTMR.Categorie.PLAINE, "JAUNES"),
               ("K", 11, CaseTMR.Categorie.CITE, "TONNERRE"),
               ("K", 12, CaseTMR.Categorie.DESOLATION, "d'AMOUR"),
               ("K", 13, CaseTMR.Categorie.FORET, "de KLUTH"),
               ("K", 14, CaseTMR.Categorie.NECROPOLE, "d'ANTINÉAR"),
               ("K", 15, CaseTMR.Categorie.COLINE, "POURPRES"),
               ("L", 1, CaseTMR.Categorie.FLEUVE, ""),
               ("L", 2, CaseTMR.Categorie.FLEUVE, ""),
               ("L", 3, CaseTMR.Categorie.LAC, "LAINEUX"),
               ("L", 4, CaseTMR.Categorie.SANCTUAIRE, "MAUVE"),
               ("L", 5, CaseTMR.Categorie.COLINE, "SUAVES"),
               ("L", 6, CaseTMR.Categorie.FORET, "GUEUSE"),
               ("L", 7, CaseTMR.Categorie.GOUFFRE, "d'ÉPISOPHE"),
               ("L", 8, CaseTMR.Categorie.MONTS, "TAVELÉS"),
               ("L", 9, CaseTMR.Categorie.COLINE, "CORNUES"),
               ("L", 10, CaseTMR.Categorie.DESERT, "de NICROP"),
               ("L", 11, CaseTMR.Categorie.COLINE, "de KOL"),
               ("L", 12, CaseTMR.Categorie.PLAINE, "VENTEUSES"),
               ("L", 13, CaseTMR.Categorie.MONTS, "DORMANTS"),
               ("L", 14, CaseTMR.Categorie.PLAINE, "de JISLITH"),
               ("M", 1, CaseTMR.Categorie.CITE, "JALOUSE"),
               ("M", 2, CaseTMR.Categorie.NECROPOLE, "de LOGOS"),
               ("M", 3, CaseTMR.Categorie.MONTS, "de VDAH"),
               ("M", 4, CaseTMR.Categorie.GOUFFRE, "GRISANT"),
               ("M", 5, CaseTMR.Categorie.CITE, "RIMARDE"),
               ("M", 6, CaseTMR.Categorie.DESOLATION, "de PRESQUE"),
               ("M", 7, CaseTMR.Categorie.DESERT, "de LAVE"),
               ("M", 8, CaseTMR.Categorie.PLAINE, "LAVÉES"),
               ("M", 9, CaseTMR.Categorie.NECROPOLE, "de ZONAR"),
               ("M", 10, CaseTMR.Categorie.FORET, "de JAJOU"),
               ("M", 11, CaseTMR.Categorie.CITE, "CRAPAUD"),
               ("M", 12, CaseTMR.Categorie.COLINE, "RÉVULSANTES"),
               ("M", 13, CaseTMR.Categorie.PLAINE, "d'ANJOU"),
               ("M", 14, CaseTMR.Categorie.DESOLATION, "d'APRÈS"),
               ("M", 15, CaseTMR.Categorie.CITE, "de KLANA"))


class TMR(object):
    """ Represente les TMR pour une personne
    """

    def __init__(self):
        self._cases = {(case[0], case[1]): CaseTMR(*case)
                       for case in default_TMR}
        self._demi_reve = ['A', 1]

    @property
    def demi_reve(self):
        return self._cases[(self._demi_reve[0], self._demi_reve[1])]
