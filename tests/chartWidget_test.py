# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 11:58:44 2021

@author: Test
"""

#https://stackoverflow.com/questions/40786760/pyqt-qtcharts-designer-plugin



from PyQt5 import QtWidgets, uic, QtGui, QtCore
#from PyQt5.QtCore import Qt, QPointF

import data
import analysis_functions

import equity

from chartDialog import chartDialog
from chartWidget import chartWidget

#set up the equities
#rightmove = data.rightmove
#tesco = data.tesco
#baillie_america
baillie_american = data.baillie_american

ed = equity.EquityDict()
ed.add([data.baillie_american,data.rightmove])

# ed = data.funds

#get data, note as the data on 2020 12 5 is not available, the next available data point is returned.
#rightmove_period = rightmove.get_data(start_date = dt.datetime(2000, 12, 22), end_date = dt.datetime(2020, 12, 5))
rightmove_data = data.rightmove.get_data()
rightmove_data = analysis_functions.percent_change(rightmove_data)

ed_data = ed.get_data()
#dict_data =  analysis_functions.percent_change(dict_data)

#del rightmove
app = QtWidgets.QApplication([])
widget = chartWidget()
widget.add_equity(ed) #provide the objects as arguments to the dialog to see it working

#dialog.chartWidget.add_equity(data.rightmove)
#dialog.chartWidget.add_equity(ed)
#dialog.chartWidget.change_y_axis_scale(chartWidget.Y_AXIS_VALUE)

widget.show()
app.exec()