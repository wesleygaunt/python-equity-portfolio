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






plot_data_item_role = Qt.UserRole + 0
equity_data_raw_role = Qt.UserRole + 1
#color_role = Qt.UserRole + 2

Y_AXIS_VALUE = 0

Y_AXIS_PERCENT = 1

NORMALISE_START = 2
NORMALISE_DATE = 3
NORMALISE_SLIDER = 4
NORMALISE_SLIDER_AUTO = 5

    
class chartWidget(QtWidgets.QWidget, Ui_chartWidget):
    def __init__(self, *args, **kwargs):
        
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        
        no_pen = pg.mkPen(None)
        
        MIN_DATE = (dt.datetime(dt.MINYEAR,1,1) - dt.datetime(1970,1,1)).total_seconds()
        MAX_DATE = (dt.datetime(dt.MAXYEAR,1,1) - dt.datetime(1970,1,1)).total_seconds()
        infline0 = pg.PlotDataItem([MIN_DATE, MAX_DATE], [0,0])
        infline1 = pg.PlotDataItem([MIN_DATE, MAX_DATE], [1,1])
        LOSS_FILL_ITEM = pg.FillBetweenItem(infline1, infline0, brush=(255,0,0,50))

        
        
        super(chartWidget, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.y_axis_scale = Y_AXIS_PERCENT
        self.y_axis_normalise_type = NORMALISE_START
        self.normalise_date = None

        
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
        
        self._1MPushButton.clicked.connect(partial(self.x_region_back_date_months, months = 1))
        self._3MPushButton.clicked.connect(partial(self.x_region_back_date_months, months = 3))
        self._6MPushButton.clicked.connect(partial(self.x_region_back_date_months, months = 6))
        self._1YPushButton.clicked.connect(partial(self.x_region_back_date_months, months = 12))
        self._3YPushButton.clicked.connect(partial(self.x_region_back_date_months, months = 36))
        self._5YPushButton.clicked.connect(partial(self.x_region_back_date_months, months = 60))
        self._10YPushButton.clicked.connect(partial(self.x_region_back_date_months, months = 120))
        self.maxPushButton.clicked.connect(self.x_region_max)
        
        self.showAllButton.clicked.connect(partial(self.show_hide_all,show_hide = True))
        self.hideAllButton.clicked.connect(partial(self.show_hide_all,False))

        
        self.legend_model = QtGui.QStandardItemModel()
        self.legend_model.itemChanged.connect(self.legend_item_checkstate_changed)
        
        self.legend.setModel(self.legend_model)
        
    
        self.legend.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        

        self.legendButton.clicked.connect(self.toggleLegend)
        self.axisOptionsButton.clicked.connect(self.toggleAxisOptions)


        
        self.percentageRadioButton.toggled.connect(self.y_axis_scale_toggled)
        #self.valueRadioButton.togglde.connect(self.vertical_axis_)
        
        #create an infinite line and plot

        self.graphWidget.addItem(LOSS_FILL_ITEM)

        
        self.x_min = None
        self.x_max = None
        self.y_min = 0
        self.y_max = None
        
        
        self.fromDateEdit.dateChanged.connect(self.x_range_min_changed)
        self.toDateEdit.dateChanged.connect(self.x_range_max_changed)
        
        
        self.linear_region.sigRegionChanged.connect(self.update_x_region)
        self.linear_region.sigRegionChangeFinished.connect(self.update_x_region_finished)


        
        
        self.normaliseStartButton.clicked.connect(self.normalise_to_start_clicked)
        self.normaliseDateButton.clicked.connect(self.normalise_to_date_clicked)
        self.normaliseSliderButton.clicked.connect(self.normalise_to_slider_clicked)
        
        self.autoNormaliseCheckBox.stateChanged.connect(self.autonormalise_toggled)
        
    def equity_name_list(self):
        name_list = []
        for row in range(0,self.legend_model.rowCount()):
            name = self.legend_model.item(row).text()
            name_list.append(name)
        return name_list
    
    
    def add_equity(self, obj):
        if(type(obj) == Equity):
            equity = obj
            if equity.name in self.equity_name_list():
                #equity already on chart, no need to add
                return
            else:
                
                no_rows = self.legend_model.rowCount()
                equity_data_raw = equity.get_data().copy()
                values_raw = list(equity_data_raw[equity.name])
                
                dates = (pd.Series(equity_data_raw.index) - dt.datetime(1970,1,1)).dt.total_seconds()

                equity_data_percent = analysis_functions.percent_change(equity_data_raw)
                values_percent = list(equity_data_percent[equity.name])
                self.rangeWidget.plot(dates, values_percent,padding = 0)

                
                #first change the dates into correct range
                #equity_data_raw.index = dates
                
                color = palette[no_rows%10] #cycle after 10
                color = QtGui.QColor(color)
                pen = pg.mkPen(color,width = 2)
                
                if(self.y_axis_scale == Y_AXIS_PERCENT):
                    if(self.normalise_date != None):
                        #print(normalise_date)
                        equity_data_percent = analysis_functions.percent_change(equity_data_raw,method = analysis_functions.FROM_DATE, date = self.normalise_date)
                        values_percent = list(equity_data_percent[equity.name])

                    plot_data_item = pg.PlotDataItem(dates, values_percent,name = equity.name, pen = pen)
                    y_max = equity_data_percent.max()[0]
                
                elif(self.y_axis_scale == Y_AXIS_VALUE):
                    plot_data_item = pg.PlotDataItem(dates, values_raw,name = equity.name, pen = pen)
                    y_max = equity_data_raw.max()[0]
                

                
                self.graphWidget.addItem(plot_data_item)
                
                
                legend_item = QtGui.QStandardItem(equity.name)
                legend_item.setData(color, Qt.DecorationRole)
                legend_item.setData(equity.name, Qt.ToolTipRole)
                #legend_item.setBackground(QtGui.QColor(color))
                legend_item.setCheckable(True)
                legend_item.setCheckState(Qt.CheckState.Checked)
                
                legend_item.setData(plot_data_item, plot_data_item_role)
                legend_item.setData(equity_data_raw, equity_data_raw_role)

                self.legend_model.appendRow(legend_item)
                
                x_min = min(dates) #
                x_max = max(dates)
                
                #y_min = 0
                #y_max = current_range[1][1]
                #y_max = self.data.max().max() * 1.1
        
                #self.update_range(x_min,x_max,y_max)
                self.update_x_range(x_min,x_max)
                self.update_y_max(y_max)
                
                
                if(self.legend_model.rowCount() == 1):
                    self.x_region_max()
                else:
                    pass
                return
        
        
        
        elif(isinstance(obj, abc.Collection) and not isinstance(obj, str)):
            collection_dict = general_functions.get_collection_items(obj)
            for equity in collection_dict.values():
                self.add_equity(equity)
                
            self.x_region_max() #if adding a lot of equities, set the regio 
            return

        else:
            #not equity or collection
            pass
            return
            
    
    def update_x_range(self,new_x_min = None, new_x_max = None):
        print("update_x_range")
        x_range_changed = False
        if(new_x_min is not None):
            if self.x_min == None:
                self.x_min = new_x_min
                x_range_changed = True
            elif(new_x_min < self.x_min):
                self.x_min = new_x_min
                x_range_changed = True
            
            
        if(new_x_max is not None):
            if self.x_max == None:
                self.x_max = new_x_max
                x_range_changed = True
            elif(new_x_max > self.x_max):
                self.x_max =new_x_max
                x_range_changed = True
                
        
        if(x_range_changed == True):
            
            self.toDateEdit.dateChanged.disconnect(self.x_range_max_changed)
            self.fromDateEdit.dateChanged.disconnect(self.x_range_min_changed)

            self.toDateEdit.setDate(pd.to_datetime(self.x_max, unit = 's'))
            self.toDateEdit.setMaximumDate(pd.to_datetime(self.x_max, unit = 's'))
            self.fromDateEdit.setMaximumDate(pd.to_datetime(self.x_max, unit = 's'))
            
            self.fromDateEdit.setDate(pd.to_datetime(self.x_min, unit = 's'))
            self.fromDateEdit.setMinimumDate(pd.to_datetime(self.x_min, unit = 's'))
            self.toDateEdit.setMinimumDate(pd.to_datetime(self.x_min, unit = 's'))

            self.toDateEdit.dateChanged.connect(self.x_range_max_changed)
            self.fromDateEdit.dateChanged.connect(self.x_range_min_changed)
            
            self.region_bounds = [self.x_min, self.x_max] #max it can be extended to.
            self.linear_region.setBounds(self.region_bounds)
            self.graphWidget.setLimits(xMin = self.x_min, xMax = self.x_max)
            #self.graphWidget.setRange(xRange = [self.x_min, self.x_max], padding = 0)
        
    def update_y_max(self, new_y_max):
        print("update_y_max")
        if(new_y_max is not None):    
            if self.y_max == None:
                self.y_max = new_y_max
            else:
                self.y_max = max([self.y_max, new_y_max])
            
        #The limits/bounds      
        self.graphWidget.setLimits(yMin = self.y_min, yMax = self.y_max)


        #self.region = [self.x_min, self.x_max]
        self.graphWidget.setRange(yRange = [self.y_min, self.y_max], padding = 0)

        #self.set_max_viewable_range()        
        ##
        


        
    def QDate_to_pydatetime(self,_Qdate):
        date = dt.datetime(year = _Qdate.year(), month = _Qdate.month(), day = _Qdate.day())
        return date
        
    def x_range_min_changed(self, date):
        print("x_range_min_changed")
        date_ts = self.QDate_to_pydatetime(date).timestamp()
        self.region[0] = date_ts
        self.linear_region.setRegion(self.region)
        
    def x_range_max_changed(self, date):
        print("x_range_max_changed")
        date_ts = self.QDate_to_pydatetime(date).timestamp()
        self.region[1] = date_ts
        self.linear_region.setRegion(self.region)
        

    
    def y_axis_scale_toggled(self):
        if(self.percentageRadioButton.isChecked() == True):
            self.y_axis_scale = Y_AXIS_PERCENT
            if(self.autoNormaliseCheckBox.isChecked() == True):
                self.y_axis_normalise_type = NORMALISE_SLIDER_AUTO
                self.normalise_to_slider()
            else:
                self.y_axis_normalise_type = NORMALISE_START
                self.change_y_axis_scale()
        else:
            self.y_axis_scale = Y_AXIS_VALUE
            self.autoNormaliseCheckBox.setChecked(False)
            self.change_y_axis_scale()

    
    def normalise_to_start_clicked(self):
        self.y_axis_normalise_type = NORMALISE_START
        self.autoNormaliseCheckBox.setChecked(False)
        self.change_y_axis_scale()
    
        
    def normalise_to_date_clicked(self):
        self.y_axis_normalise_type = NORMALISE_DATE
        self.autoNormaliseCheckBox.setChecked(False)

        _Qdate = self.normaliseDateEdit.date()
        self.normalise_to_date(_Qdate)

        
    def normalise_to_date(self, _Qdate):
        date_dt = self.QDate_to_pydatetime(_Qdate)
        self.change_y_axis_scale(date_dt)
              
    def normalise_to_slider_clicked(self):
        self.y_axis_normalise_type = NORMALISE_SLIDER
        #self.autoNormaliseCheckBox.setChecked(False)
       

        self.normalise_to_slider()
        
    def normalise_to_slider(self):
        print("normalise_to_slider")
        _Qdate = self.fromDateEdit.date()
        self.normalise_to_date(_Qdate)
    
    def autonormalise_toggled(self):
        if(self.autoNormaliseCheckBox.isChecked() == True):
            self.y_axis_normalise_type = NORMALISE_SLIDER_AUTO
            self.normaliseSliderButton.setEnabled(False)
            self.normalise_to_slider()
        else:
            self.y_axis_normalise_type = NORMALISE_SLIDER
            self.normaliseSliderButton.setEnabled(True)

    def change_y_axis_scale(self, normalise_date = None):
        self.normalise_date = normalise_date
        print("change_y_axis_scale")
        self.y_max = 0
        current_y_max = 0
     
        self.rangeWidget.clear()

        self.rangeWidget.addItem(self.linear_region)
        
        if(self.y_axis_scale == Y_AXIS_VALUE):
            self.normaliseSliderButton.setEnabled(False)
            self.normaliseDateButton.setEnabled(False)
            self.normaliseDateEdit.setEnabled(False)
            self.autoNormaliseCheckBox.setEnabled(False)
            self.normaliseStartButton.setEnabled(False)
            LOSS_FILL_ITEM.hide()
            #self.norm
        elif(self.y_axis_scale == Y_AXIS_PERCENT):
            self.normaliseSliderButton.setEnabled(True)
            self.normaliseDateButton.setEnabled(True)
            self.normaliseDateEdit.setEnabled(True)
            self.autoNormaliseCheckBox.setEnabled(True)
            self.normaliseStartButton.setEnabled(True)
            LOSS_FILL_ITEM.show()


            
        for row in range(self.legend_model.rowCount()):
            legend_item = self.legend_model.item(row)
            equity_name = legend_item.text()
            equity_data_raw = legend_item.data(equity_data_raw_role) 
            equity_data_percent = analysis_functions.percent_change(equity_data_raw)
            
            values_raw = list(equity_data_raw[legend_item.text()])
            values_percent = list(equity_data_percent[legend_item.text()])

            
            
            dates = (pd.Series(equity_data_raw.index) - dt.datetime(1970,1,1)).dt.total_seconds()
            self.graphWidget.removeItem(legend_item.data(plot_data_item_role))
            color = legend_item.data(Qt.DecorationRole)
            pen = pg.mkPen(color,width = 2)    
            
            self.rangeWidget.plot(dates, values_percent,padding = 0)


            if(self.y_axis_scale == Y_AXIS_PERCENT):
                if(self.normalise_date != None):
                    #print(normalise_date)
                    equity_data_percent = analysis_functions.percent_change(equity_data_raw,method = analysis_functions.FROM_DATE, date = normalise_date)
                    values_percent = list(equity_data_percent[legend_item.text()])

                plot_data_item = pg.PlotDataItem(dates, values_percent,name = equity_name, pen = pen)
                y_max = equity_data_percent.max()[0]
                
            elif(self.y_axis_scale == Y_AXIS_VALUE):
                plot_data_item = pg.PlotDataItem(dates, values_raw,name = equity_name, pen = pen)
                y_max = equity_data_raw.max()[0]
                

            legend_item.setData(plot_data_item, plot_data_item_role)
            self.graphWidget.addItem(plot_data_item)
            current_y_max = max([y_max, current_y_max])
            
    
        self.update_y_max(new_y_max = current_y_max)
                
      
    def update_x_region(self):
        #print("update_x_region")
        self.linear_region.setZValue(10)
        x_min, x_max = self.linear_region.getRegion()
        self.graphWidget.setXRange(x_min, x_max, padding=0)  
        
    def update_x_region_finished(self):
        #self.linear_region.setZValue(10)
        #self.graphWidget.setXRange(x_min, x_max, padding=0) 
        print("update_x_region_finished")

        self.fromDateEdit.dateChanged.disconnect(self.x_range_min_changed)
        self.toDateEdit.dateChanged.disconnect(self.x_range_max_changed)

        x_min, x_max = self.linear_region.getRegion()

        self.fromDateEdit.setDate(pd.to_datetime(x_min, unit = 's'))
        self.toDateEdit.setDate(pd.to_datetime(x_max, unit = 's'))
        
        self.fromDateEdit.dateChanged.connect(self.x_range_min_changed)
        self.toDateEdit.dateChanged.connect(self.x_range_max_changed)
        
        if(self.autoNormaliseCheckBox.isChecked() == True and self.percentageRadioButton.isChecked() == True):
            self.normalise_to_slider()
        
    def x_region_back_date_months(self, months):
        #x_max = max(self.data.index)
        x_max_datetime = pd.to_datetime(self.x_max, unit = 's')
        x_min_datetime = general_functions.add_months(x_max_datetime, -1 * months)
        x_min = x_min_datetime.timestamp()
        
        #set the end region in correct pos
        self.region = [x_min, self.x_max]
        self.linear_region.setRegion(self.region)
        
    def x_region_max(self):   

        #set the end region in correct pos
        self.region = [self.x_min, self.x_max]
        self.linear_region.setRegion(self.region)
        

            
            
 
    
    def legend_item_checkstate_changed(self, legend_item):
        #print(legend_item.text())
        # print(legend_item.data(Qt.UserRole))
        #legend = self.graphWidget.addLegend()
        
        #problem with spacings using old method (below), use this method instead
        #legend.clear()
        for row in range(self.legend_model.rowCount()):
            legend_item = self.legend_model.item(row)
            if(legend_item.checkState() == Qt.Unchecked):
                legend_item.data(plot_data_item_role).hide()
                #legend.removeItem(legend_item.data(plot_data_item_role))
            else:
                legend_item.data(plot_data_item_role).show()
                #legend.addItem(legend_item.data(plot_data_item_role),legend_item.data(plot_data_item_role).name())
                
    def show_hide_all(self,show_hide):
        self.legend_model.itemChanged.disconnect(self.legend_item_checkstate_changed)     
        for row in range(self.legend_model.rowCount()):
            legend_item = self.legend_model.item(row)
            
            if(show_hide == False):
                legend_item.data(plot_data_item_role).hide()
                legend_item.setCheckState(Qt.Unchecked)
            else:
                legend_item.data(plot_data_item_role).show()
                legend_item.setCheckState(Qt.Checked)       
        self.legend_model.itemChanged.connect(self.legend_item_checkstate_changed)
        

    def toggleLegend(self, state):
        if(state == Qt.Checked or state == True):
            self.legendGroupBox.show()
            self.legendButton.setArrowType(Qt.ArrowType.UpArrow)
        else:
            self.legendGroupBox.hide()
            self.legendButton.setArrowType(Qt.ArrowType.DownArrow)
            
    def toggleAxisOptions(self, state):
        if(state == Qt.Checked or state == True):
            self.verticalAxisOptionsGroupBox.show()
            self.horizontalAxisOptionsGroupBox.show()

            self.axisOptionsButton.setArrowType(Qt.ArrowType.UpArrow)
            self.axisOptionsFrame.show()
        else:
            self.verticalAxisOptionsGroupBox.hide()
            self.horizontalAxisOptionsGroupBox.hide()
            self.axisOptionsFrame.hide()


            self.axisOptionsButton.setArrowType(Qt.ArrowType.DownArrow)
