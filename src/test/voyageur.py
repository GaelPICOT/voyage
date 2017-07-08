#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' module de test pour la gestion de personnage

    :platform: Unix, Windows
    :synopsis: création et gestion de personnage

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
'''
import unittest
import model.competance
import model.voyageur


class TestCaracteristique(unittest.TestCase):

    def test_caracteristique_evolution(self):
        c1 = model.competance.Caracteristique("test")
        self.assertEqual(int(c1), 10)
        c1.exp += 8
        self.assertEqual(int(c1), 11)
        self.assertEqual(int(c1.exp), 0)
        c1.exp += 9
        self.assertEqual(int(c1), 12)
        self.assertEqual(int(c1.exp), 1)
        c1.exp += 8
        self.assertEqual(int(c1), 13)
        self.assertEqual(int(c1.exp), 0)
        c1.exp += 19
        self.assertEqual(int(c1), 15)
        self.assertEqual(int(c1.exp), 0)
        c1.exp += 19
        self.assertEqual(int(c1), 15)
        self.assertEqual(int(c1.exp), 19)
        c1.exp += 19
        self.assertEqual(int(c1), 16)
        self.assertEqual(int(c1.exp), 18)
        c1.exp += 32
        self.assertEqual(int(c1), 17)
        self.assertEqual(int(c1.exp), 20)
        c1.exp += 20
        self.assertEqual(int(c1), 18)
        self.assertEqual(int(c1.exp), 0)
        c1.exp += 50
        self.assertEqual(int(c1), 19)
        self.assertEqual(int(c1.exp), 0)

    def test_caracteristiques(self):
        carac = model.competance.Caracteristiques()
        carac["Rêve"].valeur = 15
        self.assertEqual(int(carac["Rêve"]), 15)
        carac["Taille"].valeur = 15
        self.assertEqual(int(carac["Taille"]), 15)
        carac["Force"].exp += 10
        self.assertEqual(int(carac["Force"]), 11)
        carac["Taille"].valeur = 6
        self.assertEqual(int(carac["Taille"]), 6)
        carac["Taille"].valeur = 15
        self.assertEqual(int(carac["Taille"]), 15)
        carac["Force"].exp += 10
        self.assertEqual(int(carac["Force"].exp), 4)
        self.assertEqual(int(carac["Force"]), 11)

    def test_cmp_tron(self):
        cmp1 = model.competance.Competance("t1", -6)
        cmp2 = model.competance.CompetanceTron("t2", cmp1)
        cmp3 = model.competance.CompetanceTron("t2", cmp2)
        cmp3 += 1
        self.assertEqual(int(cmp1.valeur), -5)
        self.assertEqual(int(cmp2.valeur), -5)
        self.assertEqual(int(cmp3.valeur), -5)

    def test_voyageur(self):
        voy = model.voyageur.Personnage()
        voy.caracteristiques["Rêve"].valeur = 15
        self.assertEqual(int(voy.caracteristiques["Rêve"]), 15)
        self.assertEqual(voy.points["Rêve"], 15)
        self.assertEqual(int(voy.competances["Bricollage"]), -4)
        voy.competances["Bricollage"] += 1
        self.assertEqual(int(voy.competances["Bricollage"]), -3)
        voy.competances["Hache 1 main"] += 1
        self.assertEqual(int(voy.competances["Hache 2 main"]), -5)
        self.assertEqual(int(voy.competances["Hache 1 main"]), -5)
        voy.competances["Hache 1 main"] += 5
        self.assertEqual(int(voy.competances["Hache 2 main"]), 0)
        self.assertEqual(int(voy.competances["Hache 1 main"]), 0)
        voy.competances["Hache 1 main"] += 1
        self.assertEqual(int(voy.competances["Hache 2 main"]), 0)
        self.assertEqual(int(voy.competances["Hache 1 main"]), 1)
        voy.competances["Epée 1 main"] += 7
        self.assertEqual(int(voy.competances["Epée 1 main"]), 1)
        self.assertEqual(int(voy.competances["Epée 2 main"]), 0)
        voy.competances["Survie en Forêt"] += 1
        self.assertEqual(int(voy.competances["Survie en Forêt"]), -8)
        voy.competances["Survie en Extérieur"] += 1
        voy.competances["Survie en Forêt"] += 1
        self.assertEqual(int(voy.competances["Survie en Forêt"]), -7)

    def test_fatigue_recalculate(self):
        fc = model.voyageur.FatigueCount()
        self.assertEqual(fc.segments[-3].size, 3)
        fc.recalculate_seg(30)
        self.assertEqual(fc.segments[-3].size, 5)
        self.assertEqual(fc.segments[-2].size, 5)
        self.assertEqual(fc.segments[0][0].size, 5)
        self.assertEqual(fc.segments[0][1].size, 5)
        self.assertEqual(fc.segments[-1][0].size, 5)
        self.assertEqual(fc.segments[-1][1].size, 5)
        fc.recalculate_seg(29)
        self.assertEqual(fc.segments[-3].size, 5)
        self.assertEqual(fc.segments[-2].size, 4)
        self.assertEqual(fc.segments[0][0].size, 4)
        self.assertEqual(fc.segments[0][1].size, 5)
        self.assertEqual(fc.segments[-1][0].size, 5)
        self.assertEqual(fc.segments[-1][1].size, 5)
        fc.recalculate_seg(28)
        self.assertEqual(fc.segments[-3].size, 5)
        self.assertEqual(fc.segments[-2].size, 4)
        self.assertEqual(fc.segments[0][0].size, 4)
        self.assertEqual(fc.segments[0][1].size, 5)
        self.assertEqual(fc.segments[-1][0].size, 4)
        self.assertEqual(fc.segments[-1][1].size, 5)
        fc.recalculate_seg(27)
        self.assertEqual(fc.segments[-3].size, 4)
        self.assertEqual(fc.segments[-2].size, 4)
        self.assertEqual(fc.segments[0][0].size, 4)
        self.assertEqual(fc.segments[0][1].size, 4)
        self.assertEqual(fc.segments[-1][0].size, 4)
        self.assertEqual(fc.segments[-1][1].size, 5)
        fc.recalculate_seg(26)
        self.assertEqual(fc.segments[-3].size, 4)
        self.assertEqual(fc.segments[-4].size, 5)
        self.assertEqual(fc.segments[-2].size, 4)
        self.assertEqual(fc.segments[0][0].size, 4)
        self.assertEqual(fc.segments[0][1].size, 4)
        self.assertEqual(fc.segments[-1][0].size, 4)
        self.assertEqual(fc.segments[-1][1].size, 4)


if __name__ == '__main__':
    unittest.main()
