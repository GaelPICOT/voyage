'''
Created on 17 sept. 2018

@author: paradoxisme
'''
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi
import os


class Cueillette(QWidget):
    """ fenetre principale
    """
    def __init__(self, parent=None, mdi_area=None):
        """ init
        """
        QWidget.__init__(self, parent)
        current_rep = os.path.abspath(os.path.split(__file__)[0])
        loadUi(os.path.join(current_rep, "cueillette.ui"), self)
        self._mdi_area = mdi_area
