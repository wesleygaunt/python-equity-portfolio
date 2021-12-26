from PyQt5 import QtCore, QtGui, QtWidgets
from chartWidget import chartWidget


class chartDialog(QtWidgets.QDialog):
    def __init__(self, parent = None):
        super().__init__(parent = parent)
        
        self.resize(1400, 800)

        self.gridLayout = QtWidgets.QGridLayout()
        
        self.chartWidget = chartWidget()
        self.chartWidget.setObjectName("chartWidget")
        self.gridLayout.addWidget(self.chartWidget)#, 0, 0, 1, 1)       
        self.setLayout(self.gridLayout)