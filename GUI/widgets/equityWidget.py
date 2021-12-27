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
"""
if using this widget inside a parent the following needs to be implemented:
    
    def moveEvent(self, moveEvent):
        self.equityWidget.move_chart()
        super(equityDialog, self).moveEvent(moveEvent)
    def closeEvent(self, closeEvent):
        self.equityWidget.close_chart()
        super(equityDialog, self).closeEvent(closeEvent)
        
as it handles move event and close events properly
"""

    
class equityWidget(QtWidgets.QWidget, Ui_equityWidget):
    def __init__(self,equity = None, *args, **kwargs):
        super(equityWidget, self).__init__(*args, **kwargs)
            
        self.setupUi(self)
        

        self.chartButton.clicked.connect(self.__toggle_chart)
        self.chartButton.setEnabled(False)
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
        self.chart.setFixedSize(self.chart.size())
        self.chart.legendButton.hide()
        self.chart.setWindowFlags(
            self.chart.windowFlags()
            &~Qt.WindowMinimizeButtonHint 
            &~Qt.WindowMaximizeButtonHint)
        #     self.chart.windowFlags() 
        #     | Qt.FramelessWindowHint)
        
        self.equity = equity
        self.setWindowTitle(self.equity.name + " - Equity")
        
        self.name.setText(self.equity.name)
        self.ISIN.setText(self.equity.ISIN)
        self.type.setText(self.equity.equity_type)
        self.equity_file.setText(self.equity.equity_filename)
        self.unit.setText(self.equity.unit)
        self.symbol.setText(self.equity.symbol)
        self.providerLineEdit.setText(self.equity.provider) 
        self.providerCodeLineEdit.setText(self.equity.provider_code)
        
        if(self.equity.saved_data_available):
            self.dataFileLineEdit.setText(self.equity.historical_data_filename)
            self.saved_data_start_date.setDate(self.equity.saved_data_start_date)                   
            self.saved_data_end_date.setDate(self.equity.saved_data_end_date)    
        else:
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

            self.move_chart()
            
            self.chart.show()

            self.chartButton.setArrowType(Qt.ArrowType.LeftArrow)
            #print("show")
            
        else:
            self.chart.hide()
            self.chartButton.setArrowType(Qt.ArrowType.RightArrow)
        


     
    def move_chart(self):
        # print("geometry: " + str(self.geometry()))
        # print("rect: " + str(self.rect()))
        # print("frameGeometry " + str(self.frameGeometry()))
        topLeft = self.geometry().topLeft()
        # print(self.mapToGlobal(topLeft))
        globalTopLeft = self.mapToGlobal(topLeft)
        #commented out as there is currently a problem
        
        if(self.parent() == None):
            pos = self.pos()
        else:
            pos = self.mapToGlobal(self.pos())
            #not yet working!
        chartpos = QtCore.QPoint(pos.x() + self.width(),pos.y())

        try:
            self.chart.move(chartpos)
        except:
                pass

    def chart_closing(self):
        self.reset_chart_button()
        
    def close_chart(self):
        try:
            self.chart.close()
        except:
            pass
        
    def moveEvent(self, moveEvent):
        self.move_chart()
        super(equityWidget, self).moveEvent(moveEvent)
              
    def closeEvent(self, closeEvent):
        self.close_chart()
        super(equityWidget, self).closeEvent(closeEvent)