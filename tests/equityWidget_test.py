# -*- coding: utf-8 -*-
"""
Created on Sat Dec 25 12:57:13 2021

@author: Test
"""

from PyQt5 import QtWidgets, uic, QtGui, QtCore

from equityWidget import equityWidget

import data

baillie_american = data.baillie_american
#baillie_american.saved_data_available = False

app = QtWidgets.QApplication([])


widget = equityWidget()
widget.set_equity(baillie_american)
widget.show()

app.exec()

