# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 20:03:25 2022

@author: Test
"""

from PyQt5 import QtCore, QtGui, QtWidgets
     
from morningstarEquityCreatorWidgetUI import Ui_morningstarEquityCreatorWidget
import list_morningstar_funds
import re

eq_dataframe = list_morningstar_funds.load_from_JSON()
names = list(eq_dataframe['LegalName'])
equity_tuples = [(index, name) for index, name in zip(range(0, len(names) + 1), names)]

INDEXROLE = QtCore.Qt.UserRole + 0


class morningstarEquityCreatorWidget(QtWidgets.QWidget, Ui_morningstarEquityCreatorWidget):
    def __init__(self,equity = None, *args, **kwargs):
        super(morningstarEquityCreatorWidget, self).__init__(*args, **kwargs)
            
        self.setupUi(self)
        

        self.searchLineEdit.returnPressed.connect(self.search)
        self.searchButton.clicked.connect(self.search)
        self.resetButton.clicked.connect(self.reset)
        

        self.listView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.match_model = QtGui.QStandardItemModel()
        self.listView.setModel(self.match_model)
        self.listView.clicked.connect(self.listView_item_clicked)
        

            
            
        # equity_tuples = [name for name in names]
        
        self.populate_listView(equity_tuples)
        
    def populate_listView(self, equity_tuples):
        
        self.match_model.clear()
        
        for equity_tuple in equity_tuples:
            item = QtGui.QStandardItem(equity_tuple[1])
            item.setData(equity_tuple[1], QtCore.Qt.ToolTipRole)
            item.setData(equity_tuple[0], INDEXROLE)
            self.match_model.appendRow(item)
            
            #print(match)
        self.informationLabel.setText(str(len(equity_tuples)) + " items")
        
        
    def search(self):
        self.informationLabel.setText("Searching...")
        
        text = self.searchLineEdit.text()
        self.search_terms = text.split(',')
        
        
        #https://blog.finxter.com/python-regex-and-operator-tutorial-video/
        self.search_terms = ["(?=.*" + term.rstrip().lstrip() + ")" for term in self.search_terms]
        self.expression = ""
        for term in self.search_terms:
            self.expression = self.expression+term
        self.expression = self.expression + ".*"
        self.expression = re.compile(self.expression, re.IGNORECASE)
            
        matches = []
        for index, name in zip(range(0, len(names) + 1), names):
            match = re.findall(self.expression, name)
            if len(match) == 0:
                continue
            else:
                matches.append((index,name))
        
        self.populate_listView(matches)
    
        
        
    def listView_item_clicked(self, modelIndex):
        index = self.match_model.data(modelIndex, INDEXROLE)
        name = self.match_model.data(modelIndex, QtCore.Qt.DisplayRole)
      
        equity = list_morningstar_funds.create_equity(eq_dataframe, index)
        self.equityWidget.set_equity(equity)
        
    def reset(self):
        self.searchLineEdit.setText("")
        self.populate_listView(equity_tuples)
        
        

app = QtWidgets.QApplication([])

widget = morningstarEquityCreatorWidget()
widget.show()

app.exec()
    
        
        