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


if __name__ == '__main__':
    unittest.main()
