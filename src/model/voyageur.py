''' élément pour la création et la gestion de personnage.

    :platform: Unix, Windows
    :synopsis: création et gestion de personnage

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
'''


class Experience(object):
    """ représente l'expérience gagné dans une caractéristique ou une
    compétance.
    """
    def __init__(self, element, xp_tab, taille=None):
        """ initialization

        :param element: élément à augmenté (caractéristique ou compétance)
        """
        self._element = element
        self._xp_tab = xp_tab
        self._valeur = 0
        if taille is not None:
            self._taille = taille
            self.__iadd__ = self.iadd_force

    def iadd_force(self, valeur):
        if self._valeur > self._taille + 4:
            self._valeur += valeur
            while (self._valeur >= self._xp_tab[int(self._element)+1] and
                   self._valeur > self._taille + 4):
                self._valeur -= self._xp_tab[int(self._element)+1]
                self._element += 1
        return self

    def __iadd__(self, valeur):
        """ incrémente la valeur
        """
        self._valeur += valeur
        while (self._valeur >= self._xp_tab[int(self._element)+1]):
            self._valeur -= self._xp_tab[int(self._element)+1]
            self._element += 1
        return self

    def __int__(self):
        """ retourn la valeur
        """
        return self._valeur

    @property
    def valeur(self):
        self._valeur


class XpTab():
    """ list de valeur pour l'augmentation par l'expérience
    """
    def __init__(self, base_list, evolution_func):
        """ initialization

        :param base_list: list d'évolution basique
        :param evolution_fun: fonction pour le calcul des element exterieur
        """
        self._base_list = base_list
        self._evolution_func = evolution_func

    def __getitem__(self, key):
        if key in list(self._base_list.keys()):
            return self._base_list[key]
        else:
            return self._evolution_func(key)


class Caracteristique(object):
    """ représente une caracteristique
    """
    base_tab = {7: 6, 8: 6, 9: 7, 10: 7, 11: 8, 12: 8, 13: 9, 14: 9, 15: 10,
                16: 20, 17: 30}

    evolution_func = lambda x: (x - 15) * 10

    xp_tab = XpTab(base_tab, evolution_func)

    def __init__(self, valeur=10):
        #: valeur de la caractéristique
        self._valeur = valeur
        #: expérinece dans la caractéristique
        self._exp = Experience(self, self.xp_tab)

    def __int__(self):
        return self._valeur

    def __iadd__(self, valeur):
        self._valeur += valeur
        return self

    def __add__(self, valeur):
        return self._valeur + valeur

    @property
    def valeur(self):
        return self._valeur

    @valeur.setter
    def valeur(self, valeur):
        self._valeur = valeur

    @property
    def exp(self):
        return self._exp

    @exp.setter
    def exp(self, exp):
        self._exp = exp


class Caracteristiques(object):
    """ classe gérant l'ensemble des caractéristiques d'un personnage (*le
    controller et la vue doivent géré les XP dans les dériver.
    """
    def __init__(self):
        """ initialization
        """
        taille = Caracteristique()
        taille.exp = None
        force = Caracteristique()
        self._tab = {"Taille": taille, "Apparence": Caracteristique(),
                     "Constitution": Caracteristique(),
                     "Force": force, "Agilité": Caracteristique(),
                     "Dextérité": Caracteristique(),
                     "Perception": Caracteristique(), "Vue": Caracteristique(),
                     "Ouïe": Caracteristique(),
                     "Odorat-Gout": Caracteristique(),
                     "Volonté": Caracteristique(),
                     "Itellect": Caracteristique(),
                     "Empathie": Caracteristique(), "Rêve": Caracteristique(),
                     "Chance": Caracteristique()}
