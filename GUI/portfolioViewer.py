# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 12:43:33 2021

@author: Test
"""

from portfolioViewerUI import Ui_MainWindow


import sys
from PyQt5 import QtWidgets, QtGui, QtCore

from PyQt5.QtCore import Qt

import analysis_functions
import equity

import data

from collections import abc
import general_functions

from fund import Fund
import datetime
import pandas as pd
from equity import Equity

from equityWidget import equityWidget
from sellPriceWidget import sellPriceWidget

# rightmove = data.rightmove
# tesco = data.tesco
# astrazeneca = data.astrazeneca
# shell = data.shell

# equity_dict = equity.EquityDict()
# fund_launch_date = datetime.datetime(2018,1, 1)
# equity_dict.add([rightmove,tesco])
# proportions = {rightmove.name:1,tesco.name:1}
# fund_1 = Fund('fund 1',equity_dict,proportions,fund_launch_date)


#equity_dict = equity.EquityDict()
#equity_dict.add([data.tesco,data.rightmove, data.baillie_american])
#ed_data = ed.get_data()


# equity_data = data.rightmove.get_data()
# equity_data = analysis_functions.percent_change(equity_data)


# rightmove = data.rightmove
# rightmove_data = rightmove.get_data()

# tesco = data.tesco
# tesco_data = tesco.get_data()

# list1 = [data.tesco,data.rightmove, data.baillie_american, data.funds]
# list2 = [data.jupiter_uk_smaller_companies,list1,equity_dict]

DATA_ROLE = Qt.UserRole + 1

class portfolioViewer(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, data_to_show,*args, **kwargs):
        super(portfolioViewer, self).__init__(*args, **kwargs)
        self.setupUi(self)

        
        self.treeModel = QtGui.QStandardItemModel()
        self.treeModel.setHorizontalHeaderLabels(['','Key','Type','Name'])
        
        self.treeView.setModel(self.treeModel)
        self.treeViewSelectionModel = self.treeView.selectionModel()
        self.treeViewSelectionModel.selectionChanged.connect(self.on_selectionChanged)     
        #self.treeView.setHeaderHidden(True)
        
        self.setupTreeModel(data_to_show)
        
        # self.treeViewWidth = 250
        # self.treeView.setMinimumWidth(self.treeViewWidth)
        # self.treeView.setMaximumWidth(self.treeViewWidth)
        
        #self.treeView.header().setStretchLastSection(True)
        #self.treeView.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        
        self.treeView.header().setSectionResizeMode(0,QtWidgets.QHeaderView.Interactive)
        self.treeView.header().resizeSection(0,40)
        
        self.treeView.header().setSectionResizeMode(1,QtWidgets.QHeaderView.Interactive)
        self.treeView.header().resizeSection(1,40)
        
        self.treeView.header().setSectionResizeMode(2,QtWidgets.QHeaderView.Interactive)
        self.treeView.header().resizeSection(2,60)
        
        self.treeView.header().setSectionResizeMode(3,QtWidgets.QHeaderView.Stretch)
        
        self.treeView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.treeView.activated.connect(self.treeView_item_activated)


        #self.treeView.header().sectionResized.connect(self.section_resized)



        self.expandAllButton.clicked.connect(self.treeView.expandAll)
        self.collapseAllButton.clicked.connect(self.treeView.collapseAll)
        self.addToChartButton.clicked.connect(self.addToChart)
        self.keyColumnCheckBox.stateChanged.connect(self.toggleKeyColumn)
        
        self.actionSell_price_calculator.triggered.connect(self.show_sell_price_calculator)
        
        self.sub_windows = []
        

        
        
        #self.showMaximized()

        
        
    # def section_resized(self, logicalIndex, oldSize,newSize):
    #     print("resize: "+ str(logicalIndex) + ", " + str(newSize))


    
    def toggleKeyColumn(self, state):
        if(state == Qt.Checked):
            #self.treeView.showColumn(1)
            self.treeView.header().showSection(1)
        else:
            #self.treeView.hideColumn(1)
            self.treeView.header().hideSection(1)
    def equity_from_index(self, index):
        row = index.row()
        currentDataIndex = index.sibling(row,3)


        equity = currentDataIndex.data(DATA_ROLE)
        return equity
        
    def addToChart(self):
        index = self.treeView.currentIndex() #current_selected
        equity = self.equity_from_index(index)
        
        #print(str(equity_name) + " : " + str(equity))
        
        self.chartWidget.add_equity(equity)
        

        
    def setupTreeModel(self, data):
        self.treeModel.setRowCount(0)
        self.treeModel.setColumnCount(4)
        
        rootItem = self.treeModel.invisibleRootItem()


        #rootItem.appendRow(self.recursive_add_item(data))

        if(isinstance(data,abc.Sequence) and not isinstance(data, str)):
            #caveat if the top item is a list or tuple
            data_dict = general_functions.get_collection_items(data)
            for key, item in data_dict.items():
                rootItem.appendRow(self.recursive_add_item(item,key))
        else:
            rootItem.appendRow(self.recursive_add_item(data))

        self.treeView.hideColumn(1) #hide key column
        
    def recursive_add_item(self, item, key = ""):
        if(isinstance(item,equity.Equity)): #will catch equities and funds
            #equitytype, add to tree
            #return [QtGui.QStandardItem(str(type(item).__name__)), QtGui.QStandardItem(item.name)]
            
            
            blankItem = QtGui.QStandardItem("")
            keyItem = QtGui.QStandardItem(str(key))
            typeItem = QtGui.QStandardItem(str(type(item).__name__))
            nameItem = QtGui.QStandardItem(item.name)
            
            blankItem.setData(item.name, Qt.ToolTipRole)
            keyItem.setData(item.name, Qt.ToolTipRole)
            typeItem.setData(item.name, Qt.ToolTipRole)
            nameItem.setData(item.name, Qt.ToolTipRole)
            
            nameItem.setData(item,role = DATA_ROLE)
            
            
            return [blankItem, keyItem, typeItem, nameItem]

        elif(isinstance(item, abc.Collection) and not isinstance(item, str)):
            #collection
            

            blankItem = QtGui.QStandardItem("")
            keyItem = QtGui.QStandardItem(str(key))
            typeItem = QtGui.QStandardItem(str(type(item).__name__))
            nameItem = QtGui.QStandardItem("")
            
            nameItem.setData(item,role = DATA_ROLE)

            #childId = 0
            itemDict = general_functions.get_collection_items(item)
            for child_key, child in itemDict.items():
                childItem = self.recursive_add_item(child, child_key)
                if childItem is not None:
                    blankItem.appendRow(childItem)
                    #parentKeyItem.appendRow(childItem)

                else:
                    pass
                    #print("ChildItem is None")
            
            #return [parentItem, QtGui.QStandardItem("")]
            return [blankItem, keyItem, typeItem, nameItem]

        else:
            return None
            # standardItem = QtGui.QStandardItem("***" + str(type(item).__name__) + "*** : " + str(self.uniqueID))
            # self.uniqueID = self.uniqueID + 1
            #return standardItem
    
    
    
    @QtCore.pyqtSlot('QItemSelection', 'QItemSelection')
    def on_selectionChanged(self, selected, deselected):
        #https://stackoverflow.com/questions/52778141/qtableview-selecion-change
        index = selected.indexes()[0]
        selectedItem = self.equity_from_index(index)
        
        if(type(selectedItem) == Equity):
            self.equityWidget.set_equity(selectedItem)
            
    # def moveEvent(self, event):
    #     self.equityWidget.move_chart()
    #     super(portfolioViewer, self).moveEvent(event)
        
    def closeEvent(self, closeEvent):
        super(portfolioViewer, self).closeEvent(closeEvent)
        #close the subwindows
        #del self.sub_windows
        # for sub_window in self.sub_windows:
        #     print(sub_window)
        #     sub_window.close()
        app = QtWidgets.QApplication.instance()
        app.closeAllWindows()
        #self.equityWidget.close_chart()
        
    def treeView_item_activated(self, index):
        selectedItem = self.equity_from_index(index)
        if(type(selectedItem) == Equity):
            widget = equityWidget(selectedItem)
            widget.show()

    def show_sell_price_calculator(self):
        widget = sellPriceWidget()
        self.sub_windows.append(widget)
        widget.show()