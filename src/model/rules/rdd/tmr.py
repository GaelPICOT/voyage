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
        cite = 0
        coline = 1
        desert = 2
        desolation = 3
        foret = 4
        gouffre = 5
        monts = 6
        necropole = 7
        plaine = 8
        pont = 9
        sanctuaire = 10
        fleuve = 11
        lac = 12
        marais = 13

        def __str__(self):
            return self.name

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

    @property
    def nom(self) -> str:
        """ retourne le noù
        """
        return self._nom

    def __str__(self):
        return str(self._categorie) + " " + self.nom


default_TMR = (("A", 1, CaseTMR.Categorie.cite, "VIDE"),
               ("A", 2, CaseTMR.Categorie.desert, "de MIEUX"),
               ("A", 3, CaseTMR.Categorie.desolation, "de DEMAIN"),
               ("A", 4, CaseTMR.Categorie.foret, "de FALCONAX"),
               ("A", 5, CaseTMR.Categorie.plaine, "de TRILKH"),
               ("A", 6, CaseTMR.Categorie.necropole, "de ZNIAK"),
               ("A", 7, CaseTMR.Categorie.plaine, "de l'ARC"),
               ("A", 8, CaseTMR.Categorie.gouffre, "de SHOK"),
               ("A", 9, CaseTMR.Categorie.coline, "de KORREX"),
               ("A", 10, CaseTMR.Categorie.sanctuaire, "d'OLIS"),
               ("A", 11, CaseTMR.Categorie.desolation, "d'HIER"),
               ("A", 12, CaseTMR.Categorie.plaine, "SAGES"),
               ("A", 13, CaseTMR.Categorie.fleuve, ""),
               ("A", 14, CaseTMR.Categorie.coline, "de STOLIS"),
               ("A", 15, CaseTMR.Categorie.cite, "de MIELH"),
               ("B", 1, CaseTMR.Categorie.plaine, "d'ASSORH"),
               ("B", 2, CaseTMR.Categorie.coline, "de DAWELL"),
               ("B", 3, CaseTMR.Categorie.plaine, "de RUBEGA"),
               ("B", 4, CaseTMR.Categorie.monts, "CRÂNEURS"),
               ("B", 5, CaseTMR.Categorie.coline, "de TANEGV"),
               ("B", 6, CaseTMR.Categorie.foret, "de BUST"),
               ("B", 7, CaseTMR.Categorie.marais, "BLUANTS"),
               ("B", 8, CaseTMR.Categorie.fleuve, ""),
               ("B", 9, CaseTMR.Categorie.lac, "de LUCRE"),
               ("B", 10, CaseTMR.Categorie.monts, "SALÉS"),
               ("B", 11, CaseTMR.Categorie.cite, "de BRILZ"),
               ("B", 12, CaseTMR.Categorie.fleuve, ""),
               ("B", 13, CaseTMR.Categorie.gouffre, "des LITIGES"),
               ("B", 14, CaseTMR.Categorie.necropole, "de GORLO"),
               ("C", 1, CaseTMR.Categorie.necropole, "de KROAK"),
               ("C", 2, CaseTMR.Categorie.marais, "GLIGNANTS"),
               ("C", 3, CaseTMR.Categorie.fleuve, ""),
               ("C", 4, CaseTMR.Categorie.pont, "de GIOLI"),
               ("C", 5, CaseTMR.Categorie.marais, "FLOUANTS"),
               ("C", 6, CaseTMR.Categorie.cite, "PAVOIS"),
               ("C", 7, CaseTMR.Categorie.fleuve, ""),
               ("C", 8, CaseTMR.Categorie.foret, "TURMIDE"),
               ("C", 9, CaseTMR.Categorie.monts, "TUMÉFIÉS"),
               ("C", 10, CaseTMR.Categorie.marais, "de DOM"),
               ("C", 11, CaseTMR.Categorie.pont, "de ROI"),
               ("C", 12, CaseTMR.Categorie.lac, "de FRICASA"),
               ("C", 13, CaseTMR.Categorie.desert, "de NEIGE"),
               ("C", 14, CaseTMR.Categorie.foret, "de BISSAM"),
               ("C", 15, CaseTMR.Categorie.plaine, "de TOUÉ"),
               ("D", 1, CaseTMR.Categorie.fleuve, ""),
               ("D", 2, CaseTMR.Categorie.cite, "de FROST"),
               ("D", 3, CaseTMR.Categorie.gouffre, "d'OKI"),
               ("D", 4, CaseTMR.Categorie.lac, "de FOAM"),
               ("D", 5, CaseTMR.Categorie.fleuve, ""),
               ("D", 6, CaseTMR.Categorie.fleuve, ""),
               ("D", 7, CaseTMR.Categorie.plaine, "d'AFFA"),
               ("D", 8, CaseTMR.Categorie.cite, "d'OLAK"),
               ("D", 9, CaseTMR.Categorie.pont, "d'ORX"),
               ("D", 10, CaseTMR.Categorie.fleuve, ""),
               ("D", 11, CaseTMR.Categorie.desolation, "de PARTOUT"),
               ("D", 12, CaseTMR.Categorie.coline, "d'HUAÏ"),
               ("D", 13, CaseTMR.Categorie.cite, "SORDIDE"),
               ("D", 14, CaseTMR.Categorie.sanctuaire, "PLAT"),
               ("E", 1, CaseTMR.Categorie.monts, "de KANAÏ"),
               ("E", 2, CaseTMR.Categorie.plaine, "de FIASK"),
               ("E", 3, CaseTMR.Categorie.foret, "d'ESTOUBH"),
               ("E", 4, CaseTMR.Categorie.plaine, "d'ORTI"),
               ("E", 5, CaseTMR.Categorie.monts, "BRÛLANTS"),
               ("E", 6, CaseTMR.Categorie.sanctuaire, "de PLAINE"),
               ("E", 7, CaseTMR.Categorie.foret, "de GLUSKS"),
               ("E", 8, CaseTMR.Categorie.plaine, "d'IOLISE"),
               ("E", 9, CaseTMR.Categorie.fleuve, ""),
               ("E", 10, CaseTMR.Categorie.gouffre, "de JUNK"),
               ("E", 11, CaseTMR.Categorie.lac, "de GLINSTER"),
               ("E", 12, CaseTMR.Categorie.monts, "AJOURÉS"),
               ("E", 13, CaseTMR.Categorie.plaine, "de XNEZ"),
               ("E", 14, CaseTMR.Categorie.monts, "de QUATH"),
               ("E", 15, CaseTMR.Categorie.foret, "des FURIES"),
               ("F", 1, CaseTMR.Categorie.cite, "GLAUQUE"),
               ("F", 2, CaseTMR.Categorie.lac, "de MISÈRE"),
               ("F", 3, CaseTMR.Categorie.fleuve, ""),
               ("F", 4, CaseTMR.Categorie.fleuve, ""),
               ("F", 5, CaseTMR.Categorie.cite, "de PANOPLE"),
               ("F", 6, CaseTMR.Categorie.fleuve, ""),
               ("F", 7, CaseTMR.Categorie.fleuve, ""),
               ("F", 8, CaseTMR.Categorie.lac, "des CHATS"),
               ("F", 9, CaseTMR.Categorie.plaine, "de FOE"),
               ("F", 10, CaseTMR.Categorie.marais, "ZULTANTS"),
               ("F", 11, CaseTMR.Categorie.cite, "de NOAPE"),
               ("F", 12, CaseTMR.Categorie.necropole, "de THROAT"),
               ("F", 13, CaseTMR.Categorie.foret, "des CRIS"),
               ("F", 14, CaseTMR.Categorie.plaine, "BRISÉES"),
               ("G", 1, CaseTMR.Categorie.desolation, "de JAMAIS"),
               ("G", 2, CaseTMR.Categorie.marais, "NUISANTS"),
               ("G", 3, CaseTMR.Categorie.gouffre, "de SUN"),
               ("G", 4, CaseTMR.Categorie.sanctuaire, "BLANC"),
               ("G", 5, CaseTMR.Categorie.pont, "d'IK"),
               ("G", 6, CaseTMR.Categorie.marais, "GLUTANTS"),
               ("G", 7, CaseTMR.Categorie.cite, "de TERWA"),
               ("G", 8, CaseTMR.Categorie.plaine, "SANS JOIE"),
               ("G", 9, CaseTMR.Categorie.desert, "de SEL"),
               ("G", 10, CaseTMR.Categorie.cite, "de SERGAL"),
               ("G", 11, CaseTMR.Categorie.fleuve, ""),
               ("G", 12, CaseTMR.Categorie.plaine, "de LUFMIL"),
               ("G", 13, CaseTMR.Categorie.plaine, "CALCAIRES"),
               ("G", 14, CaseTMR.Categorie.desert, "de SEK"),
               ("G", 15, CaseTMR.Categorie.plaine, "des SOUPIRS"),
               ("H", 1, CaseTMR.Categorie.lac, "d'ANTICALME"),
               ("H", 2, CaseTMR.Categorie.coline, "de PARTA"),
               ("H", 3, CaseTMR.Categorie.foret, "de GANNA"),
               ("H", 4, CaseTMR.Categorie.plaine, "de PSARK"),
               ("H", 5, CaseTMR.Categorie.desert, "de KRANE"),
               ("H", 6, CaseTMR.Categorie.monts, "GURDES"),
               ("H", 7, CaseTMR.Categorie.gouffre, "de KAFPA"),
               ("H", 8, CaseTMR.Categorie.foret, "d'OURF"),
               ("H", 9, CaseTMR.Categorie.coline, "de NOIRSEUL"),
               ("H", 10, CaseTMR.Categorie.plaine, "NOIRES"),
               ("H", 11, CaseTMR.Categorie.fleuve, ""),
               ("H", 12, CaseTMR.Categorie.coline, "de TOOTH"),
               ("H", 13, CaseTMR.Categorie.desolation, "de RIEN"),
               ("H", 14, CaseTMR.Categorie.plaine, "BLANCHES"),
               ("I", 1, CaseTMR.Categorie.plaine, "GRISES"),
               ("I", 2, CaseTMR.Categorie.foret, "FADE"),
               ("I", 3, CaseTMR.Categorie.monts, "GRINÇANTS"),
               ("I", 4, CaseTMR.Categorie.plaine, "de XIAX"),
               ("I", 5, CaseTMR.Categorie.desolation, "de TOUJOURS"),
               ("I", 6, CaseTMR.Categorie.necropole, "de XOTAR"),
               ("I", 7, CaseTMR.Categorie.plaine, "de TROO"),
               ("I", 8, CaseTMR.Categorie.fleuve, ""),
               ("I", 9, CaseTMR.Categorie.fleuve, ""),
               ("I", 10, CaseTMR.Categorie.lac, "WANITO"),
               ("I", 11, CaseTMR.Categorie.pont, "de YALM"),
               ("I", 12, CaseTMR.Categorie.gouffre, "ABIMEUX"),
               ("I", 13, CaseTMR.Categorie.monts, "BIGLEUX"),
               ("I", 14, CaseTMR.Categorie.cite, "DESTITUÉE"),
               ("I", 15, CaseTMR.Categorie.monts, "des DRAGÉES"),
               ("J", 1, CaseTMR.Categorie.monts, "FAINÉANTS"),
               ("J", 2, CaseTMR.Categorie.desert, "de POLY"),
               ("J", 3, CaseTMR.Categorie.cite, "VENIN"),
               ("J", 4, CaseTMR.Categorie.coline, "d'ENCRE"),
               ("J", 5, CaseTMR.Categorie.marais, "de JAB"),
               ("J", 6, CaseTMR.Categorie.lac, "d'IAUPE"),
               ("J", 7, CaseTMR.Categorie.fleuve, ""),
               ("J", 8, CaseTMR.Categorie.monts, "BARASK"),
               ("J", 9, CaseTMR.Categorie.marais, "GRONCHANTS"),
               ("J", 10, CaseTMR.Categorie.fleuve, ""),
               ("J", 11, CaseTMR.Categorie.plaine, "de MILTIAR"),
               ("J", 12, CaseTMR.Categorie.cite, "FOLLE"),
               ("J", 13, CaseTMR.Categorie.gouffre, "de GROMPH"),
               ("J", 14, CaseTMR.Categorie.desert, "de SANIK"),
               ("K", 1, CaseTMR.Categorie.cite, "d'ONKAUSE"),
               ("K", 2, CaseTMR.Categorie.foret, "TAMÉE"),
               ("K", 3, CaseTMR.Categorie.plaine, "de DOIS"),
               ("K", 4, CaseTMR.Categorie.pont, "de FAH"),
               ("K", 5, CaseTMR.Categorie.fleuve, ""),
               ("K", 6, CaseTMR.Categorie.desolation, "de POOR"),
               ("K", 7, CaseTMR.Categorie.cite, "de KOLIX"),
               ("K", 8, CaseTMR.Categorie.desert, "de FUMÉE"),
               ("K", 9, CaseTMR.Categorie.sanctuaire, "NOIR"),
               ("K", 10, CaseTMR.Categorie.plaine, "JAUNES"),
               ("K", 11, CaseTMR.Categorie.cite, "TONNERRE"),
               ("K", 12, CaseTMR.Categorie.desolation, "d'AMOUR"),
               ("K", 13, CaseTMR.Categorie.foret, "de KLUTH"),
               ("K", 14, CaseTMR.Categorie.necropole, "d'ANTINÉAR"),
               ("K", 15, CaseTMR.Categorie.coline, "POURPRES"),
               ("L", 1, CaseTMR.Categorie.fleuve, ""),
               ("L", 2, CaseTMR.Categorie.fleuve, ""),
               ("L", 3, CaseTMR.Categorie.lac, "LAINEUX"),
               ("L", 4, CaseTMR.Categorie.sanctuaire, "MAUVE"),
               ("L", 5, CaseTMR.Categorie.coline, "SUAVES"),
               ("L", 6, CaseTMR.Categorie.foret, "GUEUSE"),
               ("L", 7, CaseTMR.Categorie.gouffre, "d'ÉPISOPHE"),
               ("L", 8, CaseTMR.Categorie.monts, "TAVELÉS"),
               ("L", 9, CaseTMR.Categorie.coline, "CORNUES"),
               ("L", 10, CaseTMR.Categorie.desert, "de NICROP"),
               ("L", 11, CaseTMR.Categorie.coline, "de KOL"),
               ("L", 12, CaseTMR.Categorie.plaine, "VENTEUSES"),
               ("L", 13, CaseTMR.Categorie.monts, "DORMANTS"),
               ("L", 14, CaseTMR.Categorie.plaine, "de JISLITH"),
               ("M", 1, CaseTMR.Categorie.cite, "JALOUSE"),
               ("M", 2, CaseTMR.Categorie.necropole, "de LOGOS"),
               ("M", 3, CaseTMR.Categorie.monts, "de VDAH"),
               ("M", 4, CaseTMR.Categorie.gouffre, "GRISANT"),
               ("M", 5, CaseTMR.Categorie.cite, "RIMARDE"),
               ("M", 6, CaseTMR.Categorie.desolation, "de PRESQUE"),
               ("M", 7, CaseTMR.Categorie.desert, "de LAVE"),
               ("M", 8, CaseTMR.Categorie.plaine, "LAVÉES"),
               ("M", 9, CaseTMR.Categorie.necropole, "de ZONAR"),
               ("M", 10, CaseTMR.Categorie.foret, "de JAJOU"),
               ("M", 11, CaseTMR.Categorie.cite, "CRAPAUD"),
               ("M", 12, CaseTMR.Categorie.coline, "RÉVULSANTES"),
               ("M", 13, CaseTMR.Categorie.plaine, "d'ANJOU"),
               ("M", 14, CaseTMR.Categorie.desolation, "d'APRÈS"),
               ("M", 15, CaseTMR.Categorie.cite, "de KLANA"))


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
