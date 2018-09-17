'''
Created on 18 sept. 2018

@author: paradoxisme
'''
import unittest
from model.rules.rdd.voyageur import Personnage
from model.rules.rdd.database import Database


class TestDB(unittest.TestCase):

    def test_personnage(self):
        voy = Personnage()
        DB = Database()
        DB.add_personnage(voy, "name")
        DB.save_to_file("file_name")
