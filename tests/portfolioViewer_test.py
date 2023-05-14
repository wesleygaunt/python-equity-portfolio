# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 17:14:10 2022

@author: Test
"""
import sys
import data
from PyQt5 import QtWidgets

from portfolioViewer import portfolioViewer



app = QtWidgets.QApplication(sys.argv)
main_window = portfolioViewer(data.all_equities)
main_window.show()
app.exec()