''' Ã©lÃ©ment pour la crÃ©ation et la gestion de personnage.

    :platform: Unix, Windows
    :synopsis: crÃ©ation et gestion de personnage

.. moduleauthor:: GaÃ«l PICOT <gael.picot@free.fr>
'''


class Experience(object):
    """ reprÃ©sente l'expÃ©rience gagnÃ© dans une caractÃ©ristique ou une
    compÃ©tance.
    """
    def __init__(self, element, xp_tab):
        """ initialization

        :param element: Ã©lÃ©ment Ã  augmentÃ© (caractÃ©ristique ou compÃ©tance)
        """
        self._element = element
        self._xp_tab = xp_tab
        self._valeur = 0

    def __iadd__(self, valeur):
        """ incrÃ©mente la valeur
        """
        self._valeur += valeur
        while (self._valeur >= self._xp_tab[int(self._element)+1]):
            self._valeur -= self._xp_tab[int(self._element)+1]
            self._element.valeur = self._element.valeur + 1
        return self

    def __int__(self):
        """ retourn la valeur
        """
        return self._valeur

    @property
    def valeur(self):
        self._valeur


class XpTab():
    """ list de valeur pour l'augmentation par l'expÃ©rience
    """
    def __init__(self, base_list, evolution_func):
        """ initialization

        :param base_list: list d'Ã©volution basique
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
                16: 20}

    evolution_func = lambda x: (x - 14) * 10

    xp_tab = XpTab(base_tab, evolution_func)

    def __init__(self, valeur=10, physique=False, experience=None):
        #: valeur de la caractéristique
        self._valeur = valeur
        #: expérinece dans la caractéristique
        if experience is None:
            self._exp = Experience(self, Caracteristique.xp_tab)
        else:
            self._exp = experience
        #: si la caractéristique et physique (limité à 20)
        self._physique = physique

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
        if self._physique:
            if valeur < 20:
                self._valeur = valeur
        else:
            self._valeur = valeur

    @property
    def exp(self):
        return self._exp

    @exp.setter
    def exp(self, exp):
        self._exp = exp


class Caracteristiques(object):
    """ classe gÃ©rant l'ensemble des caractÃ©ristiques d'un personnage (*le
    controller et la vue doivent gÃ©rÃ© les XP dans les dÃ©river.
    """
    class TailleForce(Caracteristique):
        class ExperianceForce(Experience):
            def __init__(self, element, xp_tab):
                Experience.__init__(self, element, xp_tab)
                self._taille = 10

            def __iadd__(self, valeur):
                if int(self._element) > (self._taille + 4):
                    self._valeur += valeur
                    while (self._valeur >= self._xp_tab[int(self._element)+1]
                           and int(self._element) > self._taille + 4):
                        self._valeur -= self._xp_tab[int(self._element)+1]
                        self._element += 1
                return self

            @property
            def taille(self):
                return self._taille

            @taille.setter
            def taille(self, valeur):
                self._taille = valeur

        class Taille(object):
            def __init__(self, farce_exp):
                self._valeur = 10
                self._farce_exp = farce_exp

            def __int__(self):
                """ retourn la valeur
                """
                return self._valeur

            @property
            def valeur(self):
                return self._valeur

            @valeur.setter
            def valeur(self, valeur):
                self._valeur = valeur
                self._farce_exp.taille = valeur

        def __init__(self, valeur=10):
            self._exp = self.ExperianceForce(self, Caracteristique.xp_tab)
            Caracteristique.__init__(self, 10, False, self._exp)
            self._taille = self.Taille(self._exp)

        @property
        def taille(self):
            return self._taille

    def __init__(self):
        """ initialization
        """
        force = Caracteristiques.TailleForce()
        self._tab = {"Taille": force.taille,
                     "Apparence": Caracteristique(),
                     "Constitution": Caracteristique(True),
                     "Force": force,
                     "Agilité": Caracteristique(True),
                     "Dextérité": Caracteristique(True),
                     "Perception": Caracteristique(True),
                     "Vue": Caracteristique(True),
                     "Ouïe": Caracteristique(True),
                     "Odorat-Gout": Caracteristique(True),
                     "Volonté": Caracteristique(),
                     "Itellect": Caracteristique(),
                     "Empathie": Caracteristique(), "Rêve": Caracteristique(),
                     "Chance": Caracteristique()}

    def __getitem__(self, key):
        return self._tab[key]
