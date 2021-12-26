from PyQt5 import QtCore, QtGui, QtWidgets
from equityWidget import equityWidget


import data

baillie_american = data.baillie_american
#min_size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)

class equityDialog(QtWidgets.QDialog):
    def __init__(self, parent = None):
        super().__init__(parent = parent)
        
        #self.resize(1400, 800)

        self.gridLayout = QtWidgets.QGridLayout()
        
        self.equityWidget = equityWidget()
        self.equityWidget.setObjectName("chartWidget")
        self.gridLayout.addWidget(self.equityWidget)    
        self.setLayout(self.gridLayout)
        self.layout().setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
    
    def moveEvent(self, moveEvent):
        self.equityWidget.move_chart()
        super(equityDialog, self).moveEvent(moveEvent)
    def closeEvent(self, closeEvent):
        self.equityWidget.close_chart()
        super(equityDialog, self).closeEvent(closeEvent)

        
        
        #self.setSizePolicy(min_size_policy)
        
app = QtWidgets.QApplication([])
        
dialog = equityDialog()
dialog.equityWidget.set_equity(baillie_american)
dialog.show()
app.exec()
