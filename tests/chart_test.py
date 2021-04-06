# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 11:58:44 2021

@author: Test
"""

#https://stackoverflow.com/questions/40786760/pyqt-qtcharts-designer-plugin



from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtCore import Qt, QPointF

from PyQt5.QtChart import QChart, QChartView, QLineSeries, QBarCategoryAxis, QDateTimeAxis , QValueAxis
import data
import analysis_functions

import equity

import datetime


#set up the equities
rightmove = data.rightmove
tesco = data.tesco
#baillie_america


ed = equity.EquityDict()
ed.add([tesco,rightmove, data.baillie_american])

ed = data.funds

#get data, note as the data on 2020 12 5 is not available, the next available data point is returned.
#rightmove_period = rightmove.get_data(start_date = dt.datetime(2000, 12, 22), end_date = dt.datetime(2020, 12, 5))
rightmove_data = rightmove.get_data()
rightmove_data = analysis_functions.percent_change(rightmove_data)


dict_data = ed.get_data(start_date = datetime.datetime(2000,1,1), end_date=datetime.datetime(2020,1,1))
dict_data = analysis_functions.percent_change(dict_data)

from chartWidget import chartWidget


#del rightmove

class ChartDialog(QtWidgets.QDialog):
    def __init__(self, data, parent = None):
        super().__init__(parent = parent)
        self.resize(800, 500)

        self.gridLayout = QtWidgets.QGridLayout()
        
        self.chartWidget = chartWidget()
        #self.chartWidget.setObjectName("chartWidget")
        self.gridLayout.addWidget(self.chartWidget, 0, 0, 1, 1)
        
        self.setLayout(self.gridLayout)
        
        self.chartWidget.set_data(data)



#old method - do not use.

# from chartdialog import Ui_Dialog
# class ChartDialog(QtWidgets.QDialog, Ui_Dialog):
#     def __init__(self, data, parent=None):
#         super(ChartDialog,self).__init__(parent)
#         self.setupUi(self)
        

#         self.chartWidget.set_data(data)
#         #self.chartWidget.toggle_listview()
#         #self.chartWidget.legend.setColumnWidth(1, 10)
        


        



        
app = QtWidgets.QApplication([])
#provide the objects as arguments to the dialog to see it working
dialog = ChartDialog(rightmove_data)
dialog.exec()