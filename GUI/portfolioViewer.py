# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 12:43:33 2021

@author: Test
"""

from portfolioViewerUI import Ui_MainWindow

import sys
from PyQt5 import QtWidgets, uic, QtGui, QtCore

from PyQt5.QtCore import Qt

import analysis_functions
import equity

import data

from collections import abc
import general_functions

ed = equity.EquityDict()
ed.add([data.tesco,data.rightmove, data.baillie_american])
#ed_data = ed.get_data()


equity_data = data.rightmove.get_data()
equity_data = analysis_functions.percent_change(equity_data)

dataRole = Qt.UserRole

rightmove= data.rightmove
rightmove_data = rightmove.get_data()

tesco = data.tesco
tesco_data = tesco.get_data()

list1 = [data.tesco,data.rightmove, data.baillie_american, data.funds]
list2 = [data.jupiter_uk_smaller_companies,list1,ed]


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, data_to_show,*args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        
        self.treeModel = QtGui.QStandardItemModel()
        self.treeModel.setHorizontalHeaderLabels(['','Key','Type','Name'])
        
        self.treeView.setModel(self.treeModel)
        
        #self.treeView.setHeaderHidden(True)
        
        self.setupTreeModel(data_to_show)
        
        self.treeViewWidth = 250
        self.treeView.setMinimumWidth(self.treeViewWidth)
        self.treeView.setMaximumWidth(self.treeViewWidth)
        
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


        #self.treeView.header().sectionResized.connect(self.section_resized)



        self.expandAllButton.clicked.connect(self.treeView.expandAll)
        self.collapseAllButton.clicked.connect(self.treeView.collapseAll)
        self.addToChartButton.clicked.connect(self.addToChart)
        self.keyColumnCheckBox.stateChanged.connect(self.toggleKeyColumn)
        

        
        
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
    
    def addToChart(self):
        selectedIndex = self.treeView.currentIndex() #current_selected
        row = selectedIndex.row()
        currentEquityIndex = selectedIndex.sibling(row,3)

       
        #currentEquityIndex = selectedIndex.siblingAtColumn(3)
        
        # equity_name = currentEquityIndex.data()
        # if(equity_name == ""):
        #     return

        equity = currentEquityIndex.data(dataRole)
        
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

        self.treeView.hideColumn(1)
        
    def recursive_add_item(self, item, key = ""):
        if(type(item) == equity.Equity):
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
            
            nameItem.setData(item,role = dataRole)
            
            
            return [blankItem, keyItem, typeItem, nameItem]

        elif(isinstance(item, abc.Collection) and not isinstance(item, str)):
            #collection
            

            blankItem = QtGui.QStandardItem("")
            keyItem = QtGui.QStandardItem(str(key))
            typeItem = QtGui.QStandardItem(str(type(item).__name__))
            nameItem = QtGui.QStandardItem("")
            
            nameItem.setData(item,role = dataRole)



            #childId = 0
            itemDict = general_functions.get_collection_items(item)
            for child_key, child in itemDict.items():
                childItem = self.recursive_add_item(child, child_key)
                if childItem is not None:
                    blankItem.appendRow(childItem)
                    #parentKeyItem.appendRow(childItem)

                else:
                    print("ChildItem is None")
            
            #return [parentItem, QtGui.QStandardItem("")]
            return [blankItem,keyItem, typeItem, nameItem]

        else:
            return None
            # standardItem = QtGui.QStandardItem("***" + str(type(item).__name__) + "*** : " + str(self.uniqueID))
            # self.uniqueID = self.uniqueID + 1
            #return standardItem


equities = [data.baillie_american, data.tesco, data.ceres, data.rightmove]
app = QtWidgets.QApplication(sys.argv)
window = MainWindow(data.all_equities)

window.show()
app.exec()

#items = window.recursive_add_item(list1)