'''
Created on 17 sept. 2018

@author: paradoxisme
'''
import json
from model.rules.rdd.voyageur import Personnage


class Database(object):
    """ représente une base de données
    """
    def __init__(self):
        """ init
        """
        self._personnages = {}

    def get_personnages(self, name):
        """ listes des personnage
        """
        return self._personnages[name]

    def add_personnage(self, personnage, name=None):
        """ ajout un personnage s'il est de la bonne class
        """
        if isinstance(personnage, Personnage):
            if name is not None:
                self._personnages[name] = personnage
            else:
                self._personnages[personnage.signes_particuliers.nom] = personnage

    def save_to_file(self, file_name):
        """ save database to file
        """
        with open(file_name, 'w') as f:
            json.dump(self.data_dict, f)

    def load_from_file(self, file_name):
        """ load from file
        """
        with open(file_name) as f:
            data = json.load(f)
        self._data = data

    @property
    def data_dict(self):
        """ return a dictionnary representation of datas
        """
        data = {}
        data["personnages"] = {}
        for name, personnage in self._personnages.items():
            data["personnages"][name] = personnage.data_dict

    @data_dict.setter
    def data_dict(self, value):
        for name, personnage in value["personnages"].items():
            new_perso = Personnage()
            new_perso.data_dict = personnage
            self._personnages[name] = new_perso
