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
import equity
import analysis_functions
from equity import Equity

from functools import partial
from collections import abc


from chartWidgetUI import Ui_chartWidget 

from bokeh.palettes import Category10_10 as palette 
import itertools  
colors_cycle = itertools.cycle(palette)

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')




plot_data_item_role = Qt.UserRole + 0
equity_data_raw_role = Qt.UserRole + 1
#color_role = Qt.UserRole + 2

Y_AXIS_PERCENT = 0
Y_AXIS_VALUE = 1


no_pen = pg.mkPen(None)

    
    
class chartWidget(QtWidgets.QWidget, Ui_chartWidget):
    def __init__(self, *args, **kwargs):
        super(chartWidget, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.y_axis_scale = Y_AXIS_PERCENT

        
        #self.graphWidget.addLegend()
        self.linear_region = pg.LinearRegionItem()

        
        self.graphWidget.setAxisItems({'bottom': pg.DateAxisItem()})
        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget.hideButtons()
        
        self.graphWidget.setMouseEnabled(x=False, y=True) #disable mouse
        
        self.rangeWidget.setAxisItems({'bottom': pg.DateAxisItem()})
        self.rangeWidget.showGrid(x=False, y=False)
        self.rangeWidget.hideAxis('left')
        
        self.rangeWidget.setMouseEnabled(x=False, y=False) #disable mouse
        self.rangeWidget.addItem(self.linear_region)
        



        pushButton_width = 40
        
        self._1MPushButton.setMaximumWidth(pushButton_width)
        self._3MPushButton.setMaximumWidth(pushButton_width)
        self._6MPushButton.setMaximumWidth(pushButton_width)
        self._1YPushButton.setMaximumWidth(pushButton_width)
        self._3YPushButton.setMaximumWidth(pushButton_width)
        self._5YPushButton.setMaximumWidth(pushButton_width)
        self._10YPushButton.setMaximumWidth(pushButton_width)
        
        self._1MPushButton.clicked.connect(partial(self.region_back_date_months, months = 1))
        self._3MPushButton.clicked.connect(partial(self.region_back_date_months, months = 3))
        self._6MPushButton.clicked.connect(partial(self.region_back_date_months, months = 6))
        self._1YPushButton.clicked.connect(partial(self.region_back_date_months, months = 12))
        self._3YPushButton.clicked.connect(partial(self.region_back_date_months, months = 36))
        self._5YPushButton.clicked.connect(partial(self.region_back_date_months, months = 60))
        self._10YPushButton.clicked.connect(partial(self.region_back_date_months, months = 120))
        self.maxPushButton.clicked.connect(self.region_max)
        
        self.showAllButton.clicked.connect(partial(self.show_hide_all,show_hide = True))
        self.hideAllButton.clicked.connect(partial(self.show_hide_all,False))

        
        self.item_model = QtGui.QStandardItemModel()
        self.item_model.itemChanged.connect(self.item_changed)
        
        self.legend.setModel(self.item_model)
        
        self.legendWidth = 200
        self.legend.setMinimumWidth(self.legendWidth)
        self.legend.setMaximumWidth(self.legendWidth)
        
        #self.legend.header().setStretchLastSection(False)
        self.legend.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        

        self.legendButton.clicked.connect(self.toggleLegend)

        self.y_axisScaleComboBox.currentIndexChanged.connect(self.change_y_axis_scale)

        
        self.x_min = None
        self.x_max = None
        self.y_min = 0
        self.y_max = None
        
        self.linear_region.sigRegionChanged.connect(self.update_region)
        self.linear_region.sigRegionChangeFinished.connect(self.update_region_finished)


        
        self.fromDateEdit.dateChanged.connect(self.range_min_changed)
        self.toDateEdit.dateChanged.connect(self.range_max_changed)
        
    def equity_name_list(self):
        name_list = []
        for row in range(0,self.item_model.rowCount()):
            name = self.item_model.item(row).text()
            name_list.append(name)
        return name_list
    
    
    def add_equity(self, obj):
        
        if(type(obj) == Equity):
            equity = obj
            if equity.name in self.equity_name_list():
                #equity already on chart
                return
            else:
                no_rows = self.item_model.rowCount()
                
                equity_data_raw = equity.get_data().copy()
                
                #first change the dates into correct range
                dates = (pd.Series(equity_data_raw.index) - dt.datetime(1970,1,1)).dt.total_seconds()
                #equity_data_raw.index = dates
                
                equity_data_percent = analysis_functions.percent_change(equity_data_raw)

    
                
                color = palette[no_rows%10] #cycle after 10
                color = QtGui.QColor(color)
                pen = pg.mkPen(color,width = 2)

                values_percent = list(equity_data_percent[equity.name])
                values_raw = list(equity_data_raw[equity.name])

                plot_data_item = pg.PlotDataItem(dates, values_percent,name = equity.name, pen = pen)
                y_max = equity_data_percent.max()[0]

                
                self.graphWidget.addItem(plot_data_item)
                self.rangeWidget.plot(dates, values_percent,padding = 0)
                
                item = QtGui.QStandardItem(equity.name)
                item.setData(color, Qt.DecorationRole)
                item.setData(equity.name, Qt.ToolTipRole)
                #item.setBackground(QtGui.QColor(color))
                item.setCheckable(True)
                item.setCheckState(Qt.CheckState.Checked)
                
                item.setData(plot_data_item, plot_data_item_role)
                item.setData(equity_data_raw, equity_data_raw_role)

                self.item_model.appendRow(item)
                
                x_min = min(dates) #
                x_max = max(dates)
                
                #y_min = 0
                #y_max = current_range[1][1]
                #y_max = self.data.max().max() * 1.1
        
                self.update_range(x_min,x_max,y_max)
                return
        
        
        
        elif(isinstance(obj, abc.Collection) and not isinstance(obj, str)):
            collection_dict = general_functions.get_collection_items(obj)
            for equity in collection_dict.values():
                self.add_equity(equity)
                
            return

        else:
            #not equity or collection
            pass
            return
            
            
    
    def update_range(self,new_x_min = None, new_x_max = None, new_y_max = None):
        if(new_x_min is not None):
            if self.x_min == None:
                self.x_min = new_x_min
            else:
                self.x_min = min([self.x_min, new_x_min])
        if(new_x_max is not None):
            if self.x_max == None:
                self.x_max = new_x_max
            else:
                self.x_max = max([self.x_max, new_x_max])
        if(new_y_max is not None):    
            if self.y_max == None:
                self.y_max = new_y_max
            else:
                self.y_max = max([self.y_max, new_y_max])
            
        #self.y_min = 0
        
        self.graphWidget.setLimits(xMin = self.x_min, xMax = self.x_max,yMin = self.y_min, yMax = self.y_max)

        self.graphWidget.setRange(xRange = [self.x_min, self.x_max], yRange = [self.y_min, self.y_max], padding = 0)
        
        self.region_bounds = [self.x_min, self.x_max] #max it can be extended to.
        self.region = [self.x_min, self.x_max]
        
        self.linear_region.setBounds(self.region_bounds)
        
        self.linear_region.setRegion(self.region)

        
        ##

        self.fromDateEdit.setDate(pd.to_datetime(self.x_min, unit = 's'))
        self.toDateEdit.setDate(pd.to_datetime(self.x_max, unit = 's'))
        
        self.fromDateEdit.setMinimumDate(pd.to_datetime(self.x_min, unit = 's'))
        self.toDateEdit.setMinimumDate(pd.to_datetime(self.x_min, unit = 's'))
        
        self.fromDateEdit.setMaximumDate(pd.to_datetime(self.x_max, unit = 's'))
        self.toDateEdit.setMaximumDate(pd.to_datetime(self.x_max, unit = 's'))
            
            
        
        
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
        #x_max = max(self.data.index)
        x_max_datetime = pd.to_datetime(self.x_max, unit = 's')
        x_min_datetime = general_functions.add_months(x_max_datetime, -1 * months)
        x_min = x_min_datetime.timestamp()
        
        #set the end region in correct pos
        self.region = [x_min, self.x_max]
        self.linear_region.setRegion(self.region)
        
    def region_max(self):   

        #set the end region in correct pos
        self.region = [self.x_min, self.x_max]
        self.linear_region.setRegion(self.region)
        
    def toggleLegend(self, state):
        if(state == Qt.Checked or state == True):
            self.legendGroupBox.show()
            self.legendButton.setArrowType(Qt.ArrowType.UpArrow)
        else:
            self.legendGroupBox.hide()
            self.legendButton.setArrowType(Qt.ArrowType.DownArrow)
            


    def change_y_axis_scale(self,scale):
        self.y_axis_scale = scale
        self.y_max = 0
        current_y_max = 0
     
        self.rangeWidget.clear()

        self.rangeWidget.addItem(self.linear_region)
        
        if(scale == Y_AXIS_VALUE):
            self.normaliseSliderButton.setEnabled(False)
            self.normaliseDateButton.setEnabled(False)
            self.normaliseDateEdit.setEnabled(False)
        elif(scale == Y_AXIS_PERCENT):
            self.normaliseSliderButton.setEnabled(True)
            self.normaliseDateButton.setEnabled(True)
            self.normaliseDateEdit.setEnabled(True)
            

      
            
        for row in range(self.item_model.rowCount()):
            item = self.item_model.item(row)
            equity_name = item.text()
            equity_data_raw = item.data(equity_data_raw_role)      
            dates = (pd.Series(equity_data_raw.index) - dt.datetime(1970,1,1)).dt.total_seconds()
            self.graphWidget.removeItem(item.data(plot_data_item_role))
            color = item.data(Qt.DecorationRole)
            pen = pg.mkPen(color,width = 2)    

            if(self.y_axis_scale == Y_AXIS_PERCENT):
                equity_data_percent = analysis_functions.percent_change(equity_data_raw)
                values_percent = list(equity_data_percent[item.text()])
                plot_data_item = pg.PlotDataItem(dates, values_percent,name = equity_name, pen = pen)
                self.rangeWidget.plot(dates, values_percent,padding = 0)
                y_max = equity_data_percent.max()[0]
                
            elif(self.y_axis_scale == Y_AXIS_VALUE):
                values_raw = list(equity_data_raw[item.text()])
                plot_data_item = pg.PlotDataItem(dates, values_raw,name = equity_name, pen = pen)
                self.rangeWidget.plot(dates, values_raw,padding = 0)
                y_max = equity_data_raw.max()[0]
            
            item.setData(plot_data_item, plot_data_item_role)
            self.graphWidget.addItem(plot_data_item)
            current_y_max = max([y_max, current_y_max])
            
    
        self.update_range(new_y_max = current_y_max)
                
       
        
        


    def item_changed(self, item):
        #print(item.text())
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
                
    def show_hide_all(self,show_hide):
        self.item_model.itemChanged.disconnect(self.item_changed)     
        for row in range(self.item_model.rowCount()):
            item = self.item_model.item(row)
            
            if(show_hide == False):
                item.data(plot_data_item_role).hide()
                item.setCheckState(Qt.Unchecked)
            else:
                item.data(plot_data_item_role).show()
                item.setCheckState(Qt.Checked)       
        self.item_model.itemChanged.connect(self.item_changed)
        
        #self.change_y_axis_scale(Y_AXIS_VALUE)

