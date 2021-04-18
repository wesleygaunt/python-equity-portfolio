# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'portfolioViewerUI.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
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
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.expandAllButton = QtWidgets.QPushButton(self.frame)
        self.expandAllButton.setObjectName("expandAllButton")
        self.gridLayout_2.addWidget(self.expandAllButton, 0, 0, 1, 1)
        self.collapseAllButton = QtWidgets.QPushButton(self.frame)
        self.collapseAllButton.setObjectName("collapseAllButton")
        self.gridLayout_2.addWidget(self.collapseAllButton, 0, 1, 1, 1)
        self.addToChartButton = QtWidgets.QPushButton(self.frame)
        self.addToChartButton.setObjectName("addToChartButton")
        self.gridLayout_2.addWidget(self.addToChartButton, 4, 0, 1, 1)
        self.keyColumnCheckBox = QtWidgets.QCheckBox(self.frame)
        self.keyColumnCheckBox.setObjectName("keyColumnCheckBox")
        self.gridLayout_2.addWidget(self.keyColumnCheckBox, 0, 2, 1, 1)
        self.treeView = QtWidgets.QTreeView(self.frame)
        self.treeView.setObjectName("treeView")
        self.treeView.header().setDefaultSectionSize(40)
        self.gridLayout_2.addWidget(self.treeView, 1, 0, 2, 3)
        self.gridLayout.addWidget(self.frame, 0, 0, 3, 1)
        self.chartWidget = chartWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chartWidget.sizePolicy().hasHeightForWidth())
        self.chartWidget.setSizePolicy(sizePolicy)
        self.chartWidget.setObjectName("chartWidget")
        self.gridLayout.addWidget(self.chartWidget, 0, 2, 3, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1400, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Portfolio Viewer"))
        self.expandAllButton.setText(_translate("MainWindow", "Expand All"))
        self.collapseAllButton.setText(_translate("MainWindow", "Collapse All"))
        self.addToChartButton.setText(_translate("MainWindow", "Add to chart"))
        self.keyColumnCheckBox.setText(_translate("MainWindow", "Key column"))
from chartWidget import chartWidget
