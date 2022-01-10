# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'portfolioViewerUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1400, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.chartWidget = chartWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chartWidget.sizePolicy().hasHeightForWidth())
        self.chartWidget.setSizePolicy(sizePolicy)
        self.chartWidget.setObjectName("chartWidget")
        self.gridLayout.addWidget(self.chartWidget, 0, 2, 3, 1)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.keyColumnCheckBox = QtWidgets.QCheckBox(self.frame)
        self.keyColumnCheckBox.setObjectName("keyColumnCheckBox")
        self.gridLayout_2.addWidget(self.keyColumnCheckBox, 0, 2, 1, 1)
        self.equityWidget = equityWidget(self.frame)
        self.equityWidget.setObjectName("equityWidget")
        self.gridLayout_2.addWidget(self.equityWidget, 5, 0, 1, 3)
        self.expandAllButton = QtWidgets.QPushButton(self.frame)
        self.expandAllButton.setObjectName("expandAllButton")
        self.gridLayout_2.addWidget(self.expandAllButton, 0, 0, 1, 1)
        self.collapseAllButton = QtWidgets.QPushButton(self.frame)
        self.collapseAllButton.setObjectName("collapseAllButton")
        self.gridLayout_2.addWidget(self.collapseAllButton, 0, 1, 1, 1)
        self.line = QtWidgets.QFrame(self.frame)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_2.addWidget(self.line, 4, 0, 1, 3)
        self.treeView = QtWidgets.QTreeView(self.frame)
        self.treeView.setObjectName("treeView")
        self.treeView.header().setDefaultSectionSize(40)
        self.gridLayout_2.addWidget(self.treeView, 1, 0, 2, 3)
        self.addToChartButton = QtWidgets.QPushButton(self.frame)
        self.addToChartButton.setObjectName("addToChartButton")
        self.gridLayout_2.addWidget(self.addToChartButton, 6, 2, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 3, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1400, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuCreate_equity = QtWidgets.QMenu(self.menuFile)
        self.menuCreate_equity.setObjectName("menuCreate_equity")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionLoad_data = QtWidgets.QAction(MainWindow)
        self.actionLoad_data.setObjectName("actionLoad_data")
        self.actionCreate_from_morningstar_list = QtWidgets.QAction(MainWindow)
        self.actionCreate_from_morningstar_list.setObjectName("actionCreate_from_morningstar_list")
        self.actionSell_price_calculator = QtWidgets.QAction(MainWindow)
        self.actionSell_price_calculator.setObjectName("actionSell_price_calculator")
        self.menuCreate_equity.addAction(self.actionCreate_from_morningstar_list)
        self.menuFile.addAction(self.actionLoad_data)
        self.menuFile.addAction(self.menuCreate_equity.menuAction())
        self.menuTools.addAction(self.actionSell_price_calculator)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Portfolio Viewer"))
        self.keyColumnCheckBox.setText(_translate("MainWindow", "Key column"))
        self.expandAllButton.setText(_translate("MainWindow", "Expand All"))
        self.collapseAllButton.setText(_translate("MainWindow", "Collapse All"))
        self.addToChartButton.setText(_translate("MainWindow", "Add to chart"))
        self.menuFile.setTitle(_translate("MainWindow", "Data"))
        self.menuCreate_equity.setTitle(_translate("MainWindow", "Create equity"))
        self.menuTools.setTitle(_translate("MainWindow", "Tools"))
        self.actionLoad_data.setText(_translate("MainWindow", "Load data"))
        self.actionCreate_from_morningstar_list.setText(_translate("MainWindow", "Create from morningstar list"))
        self.actionSell_price_calculator.setText(_translate("MainWindow", "Sell price calculator"))

from chartWidget import chartWidget
from equityWidget import equityWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

