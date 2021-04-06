# -*- coding: utf-8 -*-

#use non overlapping bitmasks
PROFIT = 0b1
PERCENTAGE = 0b10
PROFIT_AND_PERCENTAGE = PROFIT|PERCENTAGE


def calc_buy_due(quantity, price, commission, stamp_duty_percentage = 0):
    """
    Calculates the buy due (the amount paid to the broker from the customer) for a buy transaction.
    """
    buy_consideration = price * quantity #in GBP
    charges = commission
    if stamp_duty_percentage > 0:
        charges = charges + round((stamp_duty_percentage/100)*buy_consideration,2)   
    return buy_consideration + charges

def calc_sell_due(quantity, price, commission):
    """
    Calculates the sell due (the amount paid from the broker to the customer) from a sale.
    """
    sell_consideration = price * quantity
    return sell_consideration - commission
    


def profit(quantity, buy_price, sell_price, commission, stamp_duty_percentage = 0):
    """
    Calculates the profit from a buy/sell or sell/rebuy transaction.
    """
    sell_due = calc_sell_due(quantity, sell_price, commission)
    buy_due = calc_buy_due(quantity, buy_price, commission,stamp_duty_percentage)
    return sell_due - buy_due

def re_buy_percentage_profit(quantity, sell_price, buy_price, commission, stamp_duty_percentage = 0):
    """
    Calculates the percentage from profit from selling and rebuying a stock.
    """
    
    sell_due = calc_sell_due(quantity,sell_price,commission)
    buy_profit = profit(quantity, buy_price, sell_price, commission, stamp_duty_percentage)
    percentage_profit = 100* buy_profit / sell_due   
    return percentage_profit

def sell_percentage_profit(quantity, buy_price, sell_price, commission, stamp_duty_percentage = 0):
    buy_due = calc_buy_due(quantity,buy_price,commission,stamp_duty_percentage)
    buy_profit = profit(quantity, buy_price, sell_price, commission, stamp_duty_percentage)
    percentage_profit = 100* buy_profit / buy_due  
    return percentage_profit

def target_sell_price(quantity, buy_price, commission, target, target_type = PERCENTAGE, stamp_duty_percentage = 0):
    """
    Calculates the target price to sell a stock for a given profit. 
    """
    buy_due = calc_buy_due(quantity, buy_price, commission, stamp_duty_percentage)

    if(target_type == PERCENTAGE):
        target_profit = target*buy_due/100
    elif(target_type == PROFIT):
        target_profit = target
    else:
        return None
    
    target_sell_due = buy_due + target_profit   #money recieved from broker
    target_sell_consideration = target_sell_due + commission #sale value
    target_sell_price = target_sell_consideration/quantity
    return target_sell_price

def target_re_buy_price(quantity, sell_price,commission, target, target_type = PERCENTAGE, stamp_duty_percentage = 0):
    """
    Calculates the target price to rebuy a stock if it has been sold, for a given profit. 
    """
    sell_due = calc_sell_due(quantity, sell_price, commission) #gained from trade
    
    if(target_type == PERCENTAGE):
        target_profit = target*sell_due/100
    elif(target_type == PROFIT):
        target_profit = target
    else:
        return None
    
    target_buy_due = (sell_due - target_profit) #will buy at a lower price than sold
    target_buy_consideration = (target_buy_due - commission)/(1 + (stamp_duty_percentage/100))
    target_buy_price = target_buy_consideration/quantity
    return target_buy_price

class transaction:
    def __init__(self, price, quantity):
        self.price = price
        self.quantity = quantity
 
    
def average_price(transaction_list):
    total_price = 0.0
    total_quantity = 0.0
    for transaction_ in transaction_list:
        price = transaction_.price * transaction_.quantity
        total_price = total_price + price
        total_quantity = total_quantity + transaction_.quantity
    
    average_price = total_price/total_quantity
    return transaction(average_price,total_quantity)        
# stamp_duty_percentage =  0.5
# sell_price = target_sell_price(100,10,11.95,target_type=PROFIT, target =  100,stamp_duty_percentage = stamp_duty_percentage)
# profit_from_sell = profit(100, 10, sell_price, 11.95, stamp_duty_percentage = stamp_duty_percentage)

# rebuy_price = target_re_buy_price(100, sell_price, 11.95,target = 100,target_type=PROFIT, stamp_duty_percentage = stamp_duty_percentage)
# profit_from_rebuy = profit(100, rebuy_price, sell_price, 11.95, stamp_duty_percentage = stamp_duty_percentage)

# for percent in range(-20,25,5):
#     percentage_target_price = target_sell_price(470,13.647,11.95,target_type=PERCENTAGE, target =  percent)
#     print(str(percent) + "%: " + str(percentage_target_price))