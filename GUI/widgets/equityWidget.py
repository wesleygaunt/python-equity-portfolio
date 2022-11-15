# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 18:44:13 2021

@author: Test
"""

from equityWidgetUI import Ui_equityWidget 
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from chartWidget import chartWidget
from equity import Equity
import warnings
import subprocess
import webbrowser
import datetime
import os
import general_functions


    
class equityWidget(QtWidgets.QWidget, Ui_equityWidget):
    def __init__(self,equity = None, *args, **kwargs):
        super(equityWidget, self).__init__(*args, **kwargs)
            
        self.setupUi(self)
        
        self.chartButton.setEnabled(False)

        self.chartButton.clicked.connect(self.__toggle_chart)
        self.equityFileButton.clicked.connect(self.open_equity_file)
        self.dataFileButton.clicked.connect(self.open_data_file)
        self.urlButton.clicked.connect(self.open_url)
        #self.layout().setSizeConstraint(QtWidgets.QLayout.SetFixedSize) #fixed size!
        self.setFixedSize(self.size())
        
        
        
        self.setWindowFlags(
            self.windowFlags() 
            &~Qt.WindowMinimizeButtonHint
            &~Qt.WindowMaximizeButtonHint)
        
        
            
        if(type(equity) ==  Equity):
            self.set_equity(equity)
            

        
    def set_equity(self, equity):
        
        #first create a chart
        self.chartButton.setEnabled(True)

        self.chart = chartWidget(owner = self) #new window
        self.chart.toggle_legend(False)
        self.chart.toggle_axis_options(False)
        #self.chart.setFixedSize(self.chart.size())
        self.chart.legendButton.hide()
        
        if(self.parent() == None):
            #if it is a window, make it a popout widget
            self.chart.setWindowFlags(
                # self.chart.windowFlags()
                # &~Qt.WindowMinimizeButtonHint 
                # &~Qt.WindowMaximizeButtonHint)
                self.chart.windowFlags() 
                | Qt.FramelessWindowHint)
        
        self.chart.closed.connect(self.chart_closing)

        
        self.equity = equity
        self.setWindowTitle(self.equity.name + " - Equity")
        
        self.name.setText(self.equity.name)
        self.ISIN.setText(self.equity.ISIN)
        self.type.setText(self.equity.equity_type)
        self.secIdLineEdit.setText(self.equity.secId)
        self.universeLineEdit.setText(self.equity.universe)
        self.urlLineEdit.setText(self.equity.url)
        
        
        
        
        self.equity_file.setText(self.equity.equity_filename)
        self.unit.setText(self.equity.unit)
        self.symbol.setText(self.equity.symbol)
        self.providerLineEdit.setText(self.equity.provider) 
        self.providerCodeLineEdit.setText(self.equity.provider_code)
        
        if(self.equity.saved_data_available):
            self.dataFileLineEdit.setText(self.equity.historical_data_filename)
            self.saved_data_start_date.setDate(self.equity.saved_data_start_date)                   
            self.saved_data_end_date.setDate(self.equity.saved_data_end_date)  
            
            self.dataFileLabel.setEnabled(True) 
            self.dataFileLineEdit.setEnabled(True)
            self.dataFileButton.setEnabled(True)

            self.dataStartLabel.setEnabled(True) 
            self.saved_data_start_date.setEnabled(True)                   
            self.dataEndLabel.setEnabled(True) 
            self.saved_data_end_date.setEnabled(True)
            
            
            
        else:
            
            self.dataFileLineEdit.setText("")
            self.saved_data_start_date.setDate(datetime.datetime(2000,1,1))
            self.saved_data_end_date.setDate(datetime.datetime(2000,1,1))
            
            self.dataFileLabel.setEnabled(False) 
            self.dataFileLineEdit.setEnabled(False)
            self.dataFileButton.setEnabled(False)

            self.dataStartLabel.setEnabled(False) 
            self.saved_data_start_date.setEnabled(False)                   
            self.dataEndLabel.setEnabled(False) 
            self.saved_data_end_date.setEnabled(False)
        self.reset_chart_button()

    def reset_chart_button(self):
        self.chartButton.setArrowType(Qt.ArrowType.RightArrow)
        self.chartButton.setChecked(False)
        
    def __toggle_chart(self, state):
        if(state == Qt.Checked or state == True):
            
                #|Qt.FramelessWindowHint)
                
            self.chart.add_equity(self.equity)
            self.chart.setWindowTitle(self.equity.name + " - Chart")
            
        
            if(self.parent() == None):
                #place the chart to the right of the widget if it is a free floating window
                self.move_chart()
            
            self.chart.show()

            self.chartButton.setArrowType(Qt.ArrowType.LeftArrow)
            
            self.set_equity(self.equity)    #this will enable the saved data buttons if it hsa to retrieve and then save data!
            
            
            #print("show")
            
        else:
            self.chart.hide()
            self.chartButton.setArrowType(Qt.ArrowType.RightArrow)
        


     
    def move_chart(self):
        #will only be run if self.parent == None
        pos = self.pos()
        
        chartpos = QtCore.QPoint(pos.x() + self.width(),pos.y())

        try:
            self.chart.move(chartpos)
        except:
            pass

    
                
        
    def moveEvent(self, event):
        if(self.parent() == None):
            #place the chart to the right of the widget if it is a free floating window
            self.move_chart()        
        super(equityWidget, self).moveEvent(event)
    
    
    def chart_closing(self):
        #https://stackoverflow.com/questions/14017102/how-to-detect-parent-widget-close-in-pyqt
        self.reset_chart_button()
              
    def closeEvent(self, event):
        try:
            self.chart.close()
        except:
            pass
        
        super(equityWidget, self).closeEvent(event)
        
    def open_data_file(self):
        #subprocess.Popen(r'explorer /select,'+ self.equity.historical_data_filename)
        #directory = os.path.dirname(self.equity_historical_data)
        
        
    
        #subprocess.Popen(['xdg-open', self.equity.historical_data_filename])
        
        general_functions.open_directory(self.equity.historical_data_filename)

        #os.system('xdg-open ' + self.equity.historical_data_filename)

    def open_equity_file(self):
        #subprocess.Popen(r'explorer /select,'+ self.equity.equity_filename)
        general_functions.open_directory(self.equity.equity_filename)

        
    def open_url(self):
        if(self.equity.url != ''):
            webbrowser.open(self.equity.url)