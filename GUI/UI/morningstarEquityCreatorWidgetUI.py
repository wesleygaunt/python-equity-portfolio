# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'morningstarEquityCreatorWidgetUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_morningstarEquityCreatorWidget(object):
    def setupUi(self, morningstarEquityCreatorWidget):
        morningstarEquityCreatorWidget.setObjectName("morningstarEquityCreatorWidget")
        morningstarEquityCreatorWidget.resize(774, 305)
        self.gridLayout = QtWidgets.QGridLayout(morningstarEquityCreatorWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.informationLabel = QtWidgets.QLabel(morningstarEquityCreatorWidget)
        self.informationLabel.setText("")
        self.informationLabel.setObjectName("informationLabel")
        self.gridLayout.addWidget(self.informationLabel, 1, 0, 1, 2)
        self.searchButton = QtWidgets.QPushButton(morningstarEquityCreatorWidget)
        self.searchButton.setObjectName("searchButton")
        self.gridLayout.addWidget(self.searchButton, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 3, 1, 1)
        self.searchLineEdit = QtWidgets.QLineEdit(morningstarEquityCreatorWidget)
        self.searchLineEdit.setObjectName("searchLineEdit")
        self.gridLayout.addWidget(self.searchLineEdit, 0, 0, 1, 1)
        self.equityWidget = equityWidget(morningstarEquityCreatorWidget)
        self.equityWidget.setObjectName("equityWidget")
        self.gridLayout.addWidget(self.equityWidget, 2, 3, 1, 1)
        self.listView = QtWidgets.QListView(morningstarEquityCreatorWidget)
        self.listView.setObjectName("listView")
        self.gridLayout.addWidget(self.listView, 2, 0, 1, 3)
        self.resetButton = QtWidgets.QPushButton(morningstarEquityCreatorWidget)
        self.resetButton.setObjectName("resetButton")
        self.gridLayout.addWidget(self.resetButton, 0, 2, 1, 1)

        self.retranslateUi(morningstarEquityCreatorWidget)
        QtCore.QMetaObject.connectSlotsByName(morningstarEquityCreatorWidget)

    def retranslateUi(self, morningstarEquityCreatorWidget):
        _translate = QtCore.QCoreApplication.translate
        morningstarEquityCreatorWidget.setWindowTitle(_translate("morningstarEquityCreatorWidget", "Form"))
        self.searchButton.setText(_translate("morningstarEquityCreatorWidget", "Search"))
        self.resetButton.setText(_translate("morningstarEquityCreatorWidget", "Reset"))

from equityWidget import equityWidget
