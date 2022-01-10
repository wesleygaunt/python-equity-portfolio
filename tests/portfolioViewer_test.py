# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 17:14:10 2022

@author: Test
"""
import sys
import data
from PyQt5 import QtWidgets, QtGui, QtCore

from portfolioViewer import portfolioViewer

from PyQt5.QtCore import Qt


app = QtWidgets.QApplication(sys.argv)
main_window = portfolioViewer(data.all_equities)
main_window.show()
app.exec()