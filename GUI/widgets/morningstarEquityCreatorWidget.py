# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 20:03:25 2022

@author: Test
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, QThread, pyqtSignal
     
from morningstarEquityCreatorWidgetUI import Ui_morningstarEquityCreatorWidget
import list_morningstar_funds
import re
from time import process_time




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
        
        
        
        self.eq_dataframe = list_morningstar_funds.load_from_JSON()
        self.names = list(self.eq_dataframe['LegalName'])

        equity_tuples = [(index, name) for index, name in zip(range(0, len(self.names) + 1), self.names)]
            
        t1 = process_time()
        self.populate_listView(equity_tuples)
        #self.populate_listView_task()
        t2 = process_time()
        print(t2 - t1)
        #print("end")

        
        
    def populate_listView(self, equity_tuples):
        self.setDisabled(True)
     
        number_of_items = str(len(equity_tuples))
        self.match_model.clear()

        for equity_tuple in equity_tuples:
            item = QtGui.QStandardItem(equity_tuple[1])
            item.setData(equity_tuple[1], QtCore.Qt.ToolTipRole)
            item.setData(equity_tuple[0], INDEXROLE)
            
            self.match_model.appendRow(item)


        self.informationLabel.setText(number_of_items + " items")
        self.setDisabled(False)

        
    def populate_listView_task(self):
        self.informationLabel.setText("Preparing")
        self.thread = QThread()
        self.worker = listViewPopulateWorker()
        self.worker.moveToThread(self.thread)
        
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.finished.connect(self.worker_finished)
        
        self.worker.number_of_items_signal.connect(self.update_number_of_items)
        #self.worker.item_available.connect(self.add_item_to_listView)
        #self.worker.match_model_signal.connect(self.set_model)
        
        self.thread.start()
    
    def update_number_of_items(self, number_of_items):
        #self.informationLabel.setText(str(number_of_items) + " items")
        pass
        
        
        
    def worker_finished(self,signal_tuple):
        names = signal_tuple[0]
        eq_dataframe = signal_tuple[1]
        equity_tuples = signal_tuple[2]

        model = signal_tuple[3]
        
        self.names = names
        self.eq_dataframe = eq_dataframe
        self.equity_tuples = equity_tuples
        self.match_model = model
        
        self.listView.setModel(self.match_model)
        self.informationLabel.setText("Done")
        
    def search(self):
        self.informationLabel.setText("Searching...")
        
        text = self.searchLineEdit.text()
        self.search_terms = text.split(' ')
        
        
        #https://blog.finxter.com/python-regex-and-operator-tutorial-video/
        self.search_terms = ["(?=.*" + term.rstrip().lstrip() + ")" for term in self.search_terms]
        self.expression = ""
        for term in self.search_terms:
            self.expression = self.expression+term
        self.expression = self.expression + ".*"
        self.expression = re.compile(self.expression, re.IGNORECASE)
            
        matches = []
        for index, name in zip(range(0, len(self.names) + 1), self.names):
            match = re.findall(self.expression, name)
            if len(match) == 0:
                continue
            else:
                matches.append((index,name))
        
        self.populate_listView(matches)
                
    def listView_item_clicked(self, modelIndex):
        index = self.match_model.data(modelIndex, INDEXROLE)
        #name = self.match_model.data(modelIndex, QtCore.Qt.DisplayRole)
      
        equity = list_morningstar_funds.create_equity(self.eq_dataframe, index)
        self.equityWidget.set_equity(equity)
        
    def reset(self):
        self.searchLineEdit.setText("")
        self.populate_listView(self.equity_tuples)
#https://realpython.com/python-pyqt-qthread/

class listViewPopulateWorker(QObject):
    finished = pyqtSignal(tuple)
    number_of_items_signal = pyqtSignal(int)
    match_model_signal = pyqtSignal(list)
    
    
    def run(self):
        model = QtGui.QStandardItemModel()

        eq_dataframe = list_morningstar_funds.load_from_JSON()
        names = list(eq_dataframe['LegalName'])
        equity_tuples = [(index, name) for index, name in zip(range(0, len(names) + 1), names)]
        number_of_items = len(equity_tuples)
        self.number_of_items_signal.emit(number_of_items)
        
        for equity_tuple in equity_tuples:
            item = QtGui.QStandardItem(equity_tuple[1])
            item.setData(equity_tuple[1], QtCore.Qt.ToolTipRole)
            item.setData(equity_tuple[0], INDEXROLE)
            model.appendRow(item)
            
            #self.item_available.emit(equity_tuple)
        #self.match_model_signal.emit([model])
        #sleep(5)
        signal_tuple = (names,eq_dataframe,equity_tuples, model)
        self.finished.emit(signal_tuple)
    

# app = QtWidgets.QApplication([])

# widget = morningstarEquityCreatorWidget()
# widget.show()

# app.exec()
    
        
        