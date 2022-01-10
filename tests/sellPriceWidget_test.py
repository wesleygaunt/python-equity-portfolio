# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 19:12:20 2022

@author: Test
"""
from PyQt5 import QtWidgets, QtGui

from sellPriceWidget import sellPriceWidget

app = QtWidgets.QApplication([])
widget = sellPriceWidget()
widget.show()

app.exec()