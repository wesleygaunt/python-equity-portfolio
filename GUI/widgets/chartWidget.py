# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 18:32:11 2021

@author: Test
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import pyqtgraph as pg
import pandas as pd
import datetime as dt

import random
import datetime as dt

import pandas as pd

import pyqtgraph as pg

import math
import general_functions

from functools import partial

from chartWidgetUI import Ui_chartWidget 

from bokeh.palettes import Category10_10 as palette 
import itertools  
colors_cycle = itertools.cycle(palette)

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')




plot_data_item_role = Qt.UserRole + 0
data_role = Qt.UserRole + 1

#colors = ['r', 'b','g']

no_pen = pg.mkPen(None)
class chartWidget(QtWidgets.QWidget, Ui_chartWidget):
    def __init__(self, *args, obj=None, **kwargs):
        super(chartWidget, self).__init__(*args, **kwargs)
        self.setupUi(self)
        
        #self.graphWidget.addLegend()
        
        self.graphWidget.setAxisItems({'bottom': pg.DateAxisItem()})
        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget.hideButtons()
        
        self.graphWidget.setMouseEnabled(x=False, y=True) #disable mouse
        
        self.rangeWidget.setAxisItems({'bottom': pg.DateAxisItem()})
        self.rangeWidget.showGrid(x=False, y=False)
        self.rangeWidget.hideAxis('left')
        
        self.rangeWidget.setMouseEnabled(x=False, y=False) #disable mouse
        


        pushButton_width = 40
        
        self._1MPushButton.setMaximumWidth(pushButton_width)
        self._3MPushButton.setMaximumWidth(pushButton_width)
        self._6MPushButton.setMaximumWidth(pushButton_width)
        self._1YPushButton.setMaximumWidth(pushButton_width)
        self._3YPushButton.setMaximumWidth(pushButton_width)
        self._5YPushButton.setMaximumWidth(pushButton_width)
        self._10YPushButton.setMaximumWidth(pushButton_width)
        
        self.item_model = QtGui.QStandardItemModel()
        self.item_model.itemChanged.connect(self.itemChanged)
        
        self.legend.setModel(self.item_model)
        
        self.legendWidth = 250
        self.legend.setMaximumWidth(self.legendWidth)

        
        self.legendCheckBox.stateChanged.connect(self.toggleLegend)
        
        


    def set_data(self, data):
        self.data = data.copy()
        
        #convert to a series`
        if(type(data) == pd.DataFrame or type(data) == pd.Series):
            #first change the dates into correct range
            dates = (pd.Series(data.index) - dt.datetime(1970,1,1)).dt.total_seconds()
            self.data.index = dates
            
            if(type(data) == pd.Series):
                self.data = pd.DataFrame(self.data)
                
            if(len(self.data.columns) == 1):
                #single colum
                #self.legend.setHidden(True)
                pass
            for name, color in zip(data.columns, colors_cycle):
                values = list(self.data[name])
                pen = pg.mkPen(color,width = 2)
                plot_data_item = pg.PlotDataItem(dates, values,name = name, pen = pen)
                
                self.graphWidget.addItem(plot_data_item)
                self.rangeWidget.plot(dates, values,padding = 0)
                
                

                item = QtGui.QStandardItem(name)

                item.setData(QtGui.QColor(color), Qt.DecorationRole)
                item.setData(name, Qt.ToolTipRole)
                #item.setBackground(QtGui.QColor(color))
                item.setCheckable(True)
                item.setCheckState(Qt.CheckState.Checked)
                item.setData(plot_data_item, plot_data_item_role)
                self.item_model.appendRow(item)
                
                #self.legend.setColumnWidth(1,30)

                #self.legend.setColumnWidth(0,self.legendWidth - 30 -2)
                
                #self.lengend.
                
                    

        else:
            #do nothing
            return
        
        x_min = min(self.data.index)
        x_max = max(self.data.index)
        
        #y_min = 0
        #y_max = self.data.max().max()
        

        
        current_range = self.graphWidget.viewRange()
        
        self.graphWidget.setRange(xRange = [x_min, x_max], yRange = [0, current_range[1][1]], padding = 0)
        self.graphWidget.setLimits(xMin = x_min, xMax = x_max,yMin = 0, yMax = current_range[1][1])
       
        
        
        self.region_bounds = [x_min, x_max]
        self.region = [x_min, x_max]
        
        self.linear_region = pg.LinearRegionItem(bounds = self.region_bounds)

        self.rangeWidget.addItem(self.linear_region, ignoreBounds = True)
        
        self.linear_region.setRegion(self.region)
        
        self.linear_region.sigRegionChanged.connect(self.update_region)
        self.linear_region.sigRegionChangeFinished.connect(self.update_region_finished)

        self._1MPushButton.clicked.connect(partial(self.region_back_date_months, months = 1))
        self._3MPushButton.clicked.connect(partial(self.region_back_date_months, months = 3))
        self._6MPushButton.clicked.connect(partial(self.region_back_date_months, months = 6))
        self._1YPushButton.clicked.connect(partial(self.region_back_date_months, months = 12))
        self._3YPushButton.clicked.connect(partial(self.region_back_date_months, months = 36))
        self._5YPushButton.clicked.connect(partial(self.region_back_date_months, months = 60))
        self._10YPushButton.clicked.connect(partial(self.region_back_date_months, months = 120))
        self.maxPushButton.clicked.connect(self.region_max)
       

        
        self.fromDateEdit.setDate(pd.to_datetime(x_min, unit = 's'))
        self.toDateEdit.setDate(pd.to_datetime(x_max, unit = 's'))
        
        self.fromDateEdit.setMinimumDate(pd.to_datetime(x_min, unit = 's'))
        self.toDateEdit.setMinimumDate(pd.to_datetime(x_min, unit = 's'))
        
        self.fromDateEdit.setMaximumDate(pd.to_datetime(x_max, unit = 's'))
        self.toDateEdit.setMaximumDate(pd.to_datetime(x_max, unit = 's'))

        
        self.fromDateEdit.dateChanged.connect(self.range_min_changed)
        self.toDateEdit.dateChanged.connect(self.range_max_changed)

        
    def QDate_to_pydatetime(self,_Qdate):
        date = dt.datetime(year = _Qdate.year(), month = _Qdate.month(), day = _Qdate.day())
        return date
        
    def range_min_changed(self, date):
        date_ts = self.QDate_to_pydatetime(date).timestamp()
        self.region[0] = date_ts
        self.linear_region.setRegion(self.region)
        
    def range_max_changed(self, date):
        date_ts = self.QDate_to_pydatetime(date).timestamp()
        self.region[1] = date_ts
        self.linear_region.setRegion(self.region)
        
    

    
    def update_region(self):
        self.linear_region.setZValue(10)
        x_min, x_max = self.linear_region.getRegion()
        self.graphWidget.setXRange(x_min, x_max, padding=0)  
        
    def update_region_finished(self):
        #self.linear_region.setZValue(10)
        #self.graphWidget.setXRange(x_min, x_max, padding=0)  
        self.fromDateEdit.dateChanged.disconnect(self.range_min_changed)
        self.toDateEdit.dateChanged.disconnect(self.range_max_changed)

        x_min, x_max = self.linear_region.getRegion()

        self.fromDateEdit.setDate(pd.to_datetime(x_min, unit = 's'))
        self.toDateEdit.setDate(pd.to_datetime(x_max, unit = 's'))
        
        self.fromDateEdit.dateChanged.connect(self.range_min_changed)
        self.toDateEdit.dateChanged.connect(self.range_max_changed)
        
    def region_back_date_months(self, months):
        x_max = max(self.data.index)
        x_max_datetime = pd.to_datetime(x_max, unit = 's')
        x_min_datetime = general_functions.add_months(x_max_datetime, -1 * months)
        x_min = x_min_datetime.timestamp()
        
        #set the end region in correct pos
        self.region = [x_min, x_max]
        self.linear_region.setRegion(self.region)
        
    def region_max(self):   
        x_min = min(self.data.index)
        x_max = max(self.data.index)
        
        #set the end region in correct pos
        self.region = [x_min, x_max]
        self.linear_region.setRegion(self.region)
        
    def toggleLegend(self, state):
        if(state == Qt.Checked):
            self.legend.show()
        else:
            self.legend.hide()
        


    def itemChanged(self, item):
        # print(item.text())
        # print(item.data(Qt.UserRole))
        #legend = self.graphWidget.addLegend()
        
        #problem with spacings using old method (below), use this method instead
        #legend.clear()
        for row in range(self.item_model.rowCount()):
            item = self.item_model.item(row)
            if(item.checkState() == Qt.Unchecked):
                item.data(plot_data_item_role).hide()
                #legend.removeItem(item.data(plot_data_item_role))
            else:
                item.data(plot_data_item_role).show()
                #legend.addItem(item.data(plot_data_item_role),item.data(plot_data_item_role).name())
                
              
                
        # if(item.checkState() == Qt.Unchecked):
        #     item.data(plot_data_item_role).hide()
        #     legend.removeItem(item.data(plot_data_item_role))
        # else:
        #     item.data(plot_data_item_role).show()
        #     legend.addItem(item.data(plot_data_item_role),item.data(plot_data_item_role).name())
            
            
        
        
        #self.graphWidget.removeItem(item)
           #self.graphWidget.
        #item.setBackground(grey)