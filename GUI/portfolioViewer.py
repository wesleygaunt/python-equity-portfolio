# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 12:43:33 2021

@author: Test
"""

from portfolioviewerUI import Ui_MainWindow

import sys
from PyQt5 import QtWidgets, uic



class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        #self.chartWidget.set_data(data)


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()