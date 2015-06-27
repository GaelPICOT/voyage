''' module de test pour la gestion de personnage

    :platform: Unix, Windows
    :synopsis: création et gestion de personnage

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
'''
import unittest
import model.voyageur


class TestCaracteristique(unittest.TestCase):

    def test_caracteristique_evolution(self):
        c1 = model.voyageur.Caracteristique()
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
        carac = model.voyageur.Caracteristiques()
        carac["Rêve"].valeur = 15
        self.assertEqual(int(carac["Rêve"]), 15)
        carac["Taille"].valeur = 15
        self.assertEqual(int(carac["Taille"]), 15)
        carac["Force"].exp += 8


if __name__ == '__main__':
    unittest.main()
