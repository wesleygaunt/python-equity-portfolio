# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 19:07:17 2022

@author: Test
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 19:22:56 2021

@author: Test
"""
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt

from sellPriceWidgetUI import Ui_sellPriceWidget


import buy_sell_calc_functions

class sellPriceWidget(QtWidgets.QWidget, Ui_sellPriceWidget):
    def __init__(self, *args, obj=None, **kwargs):
        super(sellPriceWidget, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setFixedSize(self.size())
        self.setWindowFlags(
            self.windowFlags() 
            &~Qt.WindowMinimizeButtonHint
            &~Qt.WindowMaximizeButtonHint)
        
        self.setWindowTitle("Sell price calculator")
        
        self.SellUnitsComboBox.currentIndexChanged.connect(self.calculate)
        #Validators
        
        self.BuyPriceEdit.textChanged.connect(self.calculate)
        self.QuantityEdit.textChanged.connect(self.calculate)
        self.StampDutyEdit.textChanged.connect(self.calculate)
        self.CommissionEdit.textChanged.connect(self.calculate)
        self.BuyUnitsComboBox.currentIndexChanged.connect(self.calculate)
        self.StampDutyCheckBox.stateChanged.connect(self.calculate)
        self.CommissionCheckBox.stateChanged.connect(self.calculate)
        
        self.QuantityEdit.returnPressed.connect(self.focus_from_quantity)


        
        self.BuyPriceEdit.setValidator(QtGui.QDoubleValidator())
        self.QuantityEdit.setValidator(QtGui.QDoubleValidator())
        self.StampDutyEdit.setValidator(QtGui.QDoubleValidator())
        self.CommissionEdit.setValidator(QtGui.QDoubleValidator())
        
        self.SellPriceEdit.setValidator(QtGui.QDoubleValidator())
        self.SellPriceEdit.textChanged.connect(self.calculate_from_sell_price)
        
        self.ProfitEdit.setValidator(QtGui.QDoubleValidator())
        self.ProfitEdit.textChanged.connect(self.calculate_from_profit)
        
        
        self.ProfitPercentageEdit.setValidator(QtGui.QDoubleValidator())
        self.ProfitPercentageEdit.textChanged.connect(self.calculate_from_percentage_profit)

        
    def focus_from_quantity(self):
        if(self.StampDutyCheckBox.isChecked() == True):
            self.StampDutyEdit.setFocus()
        elif(self.CommissionCheckBox.isChecked() == True):
            self.CommissionEdit.setFocus()
        else:
            pass
        
    def get_buy_vals(self):
        if(self.BuyPriceEdit.text() != '' and self.QuantityEdit.text() != ''):
        #this 
            self.buy_price = float(self.BuyPriceEdit.text())
            self.quantity = float(self.QuantityEdit.text())
            
            if(self.StampDutyEdit.text() == '' or self.StampDutyCheckBox.isChecked() == False):
                self.stampdutypercentage = 0.0
            else:
                self.stampdutypercentage = float(self.StampDutyEdit.text())
                
            if(self.CommissionEdit.text() == '' or self.CommissionCheckBox.isChecked() == False):
                self.commission = 0.0    
            else:
                self.commission = float(self.CommissionEdit.text())
        
            
            #change to GBP if required
            buy_price_units = self.BuyUnitsComboBox.currentText()
            
            if(buy_price_units == 'GBp'):
                self.buy_price = self.buy_price/100
            else:
                pass #already in GBP
                
            self.buy_due = round(buy_sell_calc_functions.calc_buy_due(self.quantity, self.buy_price, self.commission, self.stampdutypercentage),2)
            self.BuyDue.setText(str(self.buy_due))
            return True
        else:
            return False
            
        
    def calculate_from_sell_price(self):
        buy_vals_valid = self.get_buy_vals()
        if(buy_vals_valid == True and self.SellPriceEdit.text() != '' and self.SellPriceRadioButton.isChecked() == True):
            quantity = self.quantity
            commission = self.commission
            stampdutypercentage = self.stampdutypercentage
            buy_price = self.buy_price
            
            sell_price = float(self.SellPriceEdit.text())

            
            sell_price_units = self.SellUnitsComboBox.currentText()
            
            if(sell_price_units == 'GBp'):
                sell_price = sell_price/100 #'convert to GBP
            
            profit = buy_sell_calc_functions.profit(quantity, buy_price, sell_price, commission,stampdutypercentage)
            profit = round(profit,2)
            self.ProfitEdit.setText(str(profit))
            
            percentage_profit = 100* profit/self.buy_due 
            percentage_profit = round(percentage_profit,2)
            self.ProfitPercentageEdit.setText(str(percentage_profit))
        
    def calculate_from_profit(self):
        buy_vals_valid = self.get_buy_vals()
        if(buy_vals_valid == True and self.ProfitEdit.text() != '' and self.ProfitRadioButton.isChecked() == True):
            quantity = self.quantity
            commission = self.commission
            stampdutypercentage = self.stampdutypercentage
            buy_price = self.buy_price
            
            profit = float(self.ProfitEdit.text())
            
            
            target_sell_price = buy_sell_calc_functions.target_sell_price(quantity,buy_price,commission,target = profit,target_type = buy_sell_calc_functions.PROFIT,stamp_duty_percentage = stampdutypercentage)
            target_sell_price = round(target_sell_price,5)
            sell_price_units = self.SellUnitsComboBox.currentText()
                            

            if(sell_price_units == 'GBp'):
                target_sell_price = target_sell_price*100
                target_sell_price = round(target_sell_price,3)
            self.SellPriceEdit.setText(str(target_sell_price))            

                
            percentage_profit = 100*profit/self.buy_due
            percentage_profit = round(percentage_profit,2)
            self.ProfitPercentageEdit.setText(str(percentage_profit))
            
    def calculate_from_percentage_profit(self):
        buy_vals_valid = self.get_buy_vals()
        if(buy_vals_valid == True and self.ProfitPercentageEdit.text() != '' and self.ProfitPercentageRadioButton.isChecked() == True):
            quantity = self.quantity
            commission = self.commission
            stampdutypercentage = self.stampdutypercentage
            buy_price = self.buy_price
            
            percentage_profit = float(self.ProfitPercentageEdit.text())
            
            
            target_sell_price = buy_sell_calc_functions.target_sell_price(quantity,buy_price,commission,target = percentage_profit,target_type = buy_sell_calc_functions.PERCENTAGE,stamp_duty_percentage = stampdutypercentage)
            target_sell_price = round(target_sell_price,5)
            sell_price_units = self.SellUnitsComboBox.currentText()
                            

            if(sell_price_units == 'GBp'):
                target_sell_price = target_sell_price*100
                target_sell_price = round(target_sell_price,3)
            self.SellPriceEdit.setText(str(target_sell_price))  
            
            profit = (percentage_profit/100)*self.buy_due
            profit = round(profit,2)
            self.ProfitEdit.setText(str(profit))
                  

    def calculate(self):
        buy_vals_valid = self.get_buy_vals()
        if(buy_vals_valid == True):
            quantity = self.quantity
            commission = self.commission
            stampdutypercentage = self.stampdutypercentage
            buy_price = self.buy_price
            
            
            #all in GBP
            pos_0_sell_price = buy_sell_calc_functions.target_sell_price(quantity,buy_price,commission,target = 0,target_type = buy_sell_calc_functions.PERCENTAGE,stamp_duty_percentage = stampdutypercentage)
            pos_5_sell_price = buy_sell_calc_functions.target_sell_price(quantity,buy_price,commission,target = 5,target_type = buy_sell_calc_functions.PERCENTAGE,stamp_duty_percentage = stampdutypercentage)
            pos_10_sell_price = buy_sell_calc_functions.target_sell_price(quantity,buy_price,commission,target = 10,target_type = buy_sell_calc_functions.PERCENTAGE,stamp_duty_percentage = stampdutypercentage)
            pos_15_sell_price = buy_sell_calc_functions.target_sell_price(quantity,buy_price,commission,target = 15,target_type = buy_sell_calc_functions.PERCENTAGE,stamp_duty_percentage = stampdutypercentage)
            pos_20_sell_price = buy_sell_calc_functions.target_sell_price(quantity,buy_price,commission,target = 20,target_type = buy_sell_calc_functions.PERCENTAGE,stamp_duty_percentage = stampdutypercentage)
            pos_25_sell_price = buy_sell_calc_functions.target_sell_price(quantity,buy_price,commission,target = 25,target_type = buy_sell_calc_functions.PERCENTAGE,stamp_duty_percentage = stampdutypercentage)
            
            pos_0_sell_price = round(pos_0_sell_price,5)
            pos_5_sell_price = round(pos_5_sell_price,5)
            pos_10_sell_price = round(pos_10_sell_price,5)
            pos_15_sell_price = round(pos_15_sell_price,5)
            pos_20_sell_price = round(pos_20_sell_price,5)
            pos_25_sell_price = round(pos_25_sell_price,5)
        
        
        
            #calculate profit, all in GBP
            pos_0_profit = buy_sell_calc_functions.profit(quantity,buy_price, pos_0_sell_price,commission,stampdutypercentage)
            pos_5_profit = buy_sell_calc_functions.profit(quantity,buy_price, pos_5_sell_price,commission,stampdutypercentage)
            pos_10_profit = buy_sell_calc_functions.profit(quantity,buy_price, pos_10_sell_price,commission,stampdutypercentage)
            pos_15_profit = buy_sell_calc_functions.profit(quantity,buy_price, pos_15_sell_price,commission,stampdutypercentage)
            pos_20_profit = buy_sell_calc_functions.profit(quantity,buy_price, pos_20_sell_price,commission,stampdutypercentage)
            pos_25_profit = buy_sell_calc_functions.profit(quantity,buy_price, pos_25_sell_price,commission,stampdutypercentage)
            
            pos_0_profit = round(pos_0_profit,2)
            pos_5_profit = round(pos_5_profit,2)
            pos_10_profit = round(pos_10_profit,2)
            pos_15_profit = round(pos_15_profit,2)
            pos_20_profit = round(pos_20_profit,2)
            pos_25_profit = round(pos_25_profit,2)
        
            
            self.pos_0_profit.setText(str(pos_0_profit))
            self.pos_5_profit.setText(str(pos_5_profit))
            self.pos_10_profit.setText(str(pos_10_profit))
            self.pos_15_profit.setText(str(pos_15_profit))
            self.pos_20_profit.setText(str(pos_20_profit))
            self.pos_25_profit.setText(str(pos_25_profit))
        
            
            #change units if need be
            sell_price_units = self.SellUnitsComboBox.currentText()
            if(sell_price_units == 'GBp'):
                pos_0_sell_price = pos_0_sell_price*100
                pos_5_sell_price = pos_5_sell_price*100
                pos_10_sell_price = pos_10_sell_price*100
                pos_15_sell_price = pos_15_sell_price*100
                pos_20_sell_price = pos_20_sell_price*100
                pos_25_sell_price = pos_25_sell_price*100
                
                pos_0_sell_price = round(pos_0_sell_price,3)
                pos_5_sell_price = round(pos_5_sell_price,3)
                pos_10_sell_price = round(pos_10_sell_price,3)
                pos_15_sell_price = round(pos_15_sell_price,3)
                pos_20_sell_price = round(pos_20_sell_price,3)
                pos_25_sell_price = round(pos_25_sell_price,3)
        

            # else:
            #     pass
            #     #already in GBP
            
            
        
            self.pos_0_price.setText(str(pos_0_sell_price))
            self.pos_5_price.setText(str(pos_5_sell_price))
        
            self.pos_10_price.setText(str(pos_10_sell_price))
            self.pos_15_price.setText(str(pos_15_sell_price))
            self.pos_20_price.setText(str(pos_20_sell_price))
            self.pos_25_price.setText(str(pos_25_sell_price))
            
        else:
            pass

      

