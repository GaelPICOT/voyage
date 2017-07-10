#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' module de test pour la gestion des actions

    :platform: Unix, Windows
    :synopsis: création et gestion des actions

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
'''
import unittest
from model.rules.rdd.actions import Action


class TestAction(unittest.TestCase):

    def test_action_result(self):
        a1 = Action(lancer=50)
        self.assertEqual(a1.e_part, False)
        self.assertEqual(a1.e_tot, False)
        self.assertEqual(a1.r_part, False)
        self.assertEqual(a1.r_sign, False)
        self.assertEqual(a1.reussite, True)
        self.assertEqual(a1.p_qualite, 0)
        self.assertEqual(a1.p_tache, 1)
        a1 = Action(lancer=60)
        self.assertEqual(a1.e_part, False)
        self.assertEqual(a1.e_tot, False)
        self.assertEqual(a1.r_part, False)
        self.assertEqual(a1.r_sign, False)
        self.assertEqual(a1.reussite, False)
        self.assertEqual(a1.p_qualite, -2)
        self.assertEqual(a1.p_tache, 0)
        a1 = Action(lancer=95)
        self.assertEqual(a1.e_part, True)
        self.assertEqual(a1.e_tot, False)
        self.assertEqual(a1.r_part, False)
        self.assertEqual(a1.r_sign, False)
        self.assertEqual(a1.reussite, False)
        self.assertEqual(a1.p_qualite, -4)
        self.assertEqual(a1.p_tache, -2)
        a1 = Action(lancer=96)
        self.assertEqual(a1.e_part, True)
        self.assertEqual(a1.e_tot, True)
        self.assertEqual(a1.r_part, False)
        self.assertEqual(a1.r_sign, False)
        self.assertEqual(a1.reussite, False)
        self.assertEqual(a1.p_qualite, -6)
        self.assertEqual(a1.p_tache, -4)
        a1 = Action(lancer=25)
        self.assertEqual(a1.e_part, False)
        self.assertEqual(a1.e_tot, False)
        self.assertEqual(a1.r_part, False)
        self.assertEqual(a1.r_sign, True)
        self.assertEqual(a1.reussite, True)
        self.assertEqual(a1.p_qualite, 1)
        self.assertEqual(a1.p_tache, 2)
        a1 = Action(lancer=10)
        self.assertEqual(a1.e_part, False)
        self.assertEqual(a1.e_tot, False)
        self.assertEqual(a1.r_part, True)
        self.assertEqual(a1.r_sign, True)
        self.assertEqual(a1.reussite, True)
        self.assertEqual(a1.p_qualite, 2)
        self.assertEqual(a1.p_tache, 3)

    def test_action_value(self):
        a1 = Action(12, -4, 36)
        self.assertEqual(a1.e_part, False)
        self.assertEqual(a1.e_tot, False)
        self.assertEqual(a1.r_part, False)
        self.assertEqual(a1.r_sign, False)
        self.assertEqual(a1.reussite, True)
        self.assertEqual(a1.p_qualite, 0)
        a1 = Action(12, -3, 42)
        self.assertEqual(a1.e_part, False)
        self.assertEqual(a1.e_tot, False)
        self.assertEqual(a1.r_part, False)
        self.assertEqual(a1.r_sign, False)
        self.assertEqual(a1.reussite, True)
        self.assertEqual(a1.p_qualite, 0)
        a1 = Action(12, -3, 9)
        self.assertEqual(a1.e_part, False)
        self.assertEqual(a1.e_tot, False)
        self.assertEqual(a1.r_part, True)
        self.assertEqual(a1.r_sign, True)
        self.assertEqual(a1.reussite, True)
        self.assertEqual(a1.p_qualite, 2)
        a1 = Action(9, -8, 2)
        self.assertEqual(a1.e_part, False)
        self.assertEqual(a1.e_tot, False)
        self.assertEqual(a1.r_part, True)
        self.assertEqual(a1.r_sign, True)
        self.assertEqual(a1.reussite, True)
        self.assertEqual(a1.p_qualite, 2)
        a1 = Action(8, -10, 92)
        self.assertEqual(a1.e_part, True)
        self.assertEqual(a1.e_tot, True)
        self.assertEqual(a1.r_part, False)
        self.assertEqual(a1.r_sign, False)
        self.assertEqual(a1.reussite, False)
        self.assertEqual(a1.p_qualite, -6)


if __name__ == '__main__':
    unittest.main()
