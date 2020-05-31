import krakenex
import numpy as np
import pandas as pd
import time

k = krakenex.API()
k.load_key('kraken.key')

trading_pair = input ("Please enter the pair to be traded e.g XBTUSD  ")   #Asking trading pair input
qty = int(input("Please enter the trading quantity  "))                    #Asking trading quantity 

rsi_period = int(input("Please enter the RSI Period  "))
avg_period = int(input("Please enter the Moving Average Period  "))

print(k.query_private('Balance'))  #Printing Account Balance


def rsi(d, p):
    
    '''
    
       This function takes an array of price and period as input and calculates RSI.
       
       Input : 
       first arg = price array
       second arg = RSI period
       
       Output : 
       Returns RSI values for each element in the price array 
    
    '''
    
    temp = []
    rsii = []
    pog = []    
    nog = []
    nav = []
    pav = []
    RS = []
    
    for x in range (1, len(d)):
        temp.append(float(d[x]-d[x-1]))

    for x in range(0, p):
         if temp[x] < 0 :
                nog.append(temp[x])
                pog.append(0)

         else:
                pog.append(temp[x])
                nog.append(0)
                
    nav.append(abs(sum(nog)/p)) 
    pav.append(sum(pog)/p)
    
    for x in range(p+1, len(d)):
        pogx = []    
        nogx = []
        for y in range (x-p, x):
            if temp[y] < 0 :
                nogx.append(temp[y])
                pogx.append(0)

            else:
                pogx.append(temp[y])
                nogx.append(0)
  
        
           
        nav.append(((nav[x-(p+1)]*(p-1))+abs(nogx[p-1]))/p)
        pav.append( ((pav[x-(p+1)]*(p-1))+pogx[(p-1)])/p  ) 

    for x in range(len(nav)):
        RS.append(pav[x]/nav[x])
        rsii.append(100-(100/(1+RS[x])))
       
    return(rsii)



def getList(dict): 
    '''
    This function is used to extract the pair for placing trade as Kraken might be using different convention for pair
    '''
    list = [] 
    for key in dict.keys(): 
        list.append(key) 
          
    return list[0]



def Moving_Avg(dat, prd):
    
    '''
    The function calculates moving average  of a list
    
    Input:
    dat = data list
    prd = moving average period
    
    Output:
    
    (a,b), where a = last moving avg and b = 2nd last moving avg
    '''
    
    temp = np.array(data_rsi)
    temp_dataframe = pd.DataFrame(temp)  
    rolling_mean = temp_dataframe.rolling(prd).mean()
    
    return (rolling_mean[0][len(rolling_mean)-1], rolling_mean[0][len(rolling_mean)-2])





while True:
                                            #Calling Pair Price Data from Kraken
    data = k.query_public('OHLC', {'pair' : f'{trading_pair}', 'type' : 'buy', 'ordertype' : 'market', 'volume' : '10000'})


                                    #Creating an Array of Close prices
    data_rsi = []
    for x in range (len(data['result']['XXBTZUSD'])):
        data_rsi.append(float(data['result']['XXBTZUSD'][x][4]))

                                    #Finding the Krakens Pair naming convention for placing order
    data_trade = k.query_public('Ticker', {'pair' : 'XBTUSD'})
    data_trade_value = getList(data_trade['result'])   #Pair to be put in order



    rsi_values = rsi(data_rsi, rsi_period) #Calculating RSI Values using the RSI function 

    a, b = Moving_Avg(rsi_values, avg_period)

                          #Defining Last and Second Last RSI Values to check crossover condition
    last_rsi = rsi_values[len(rsi_values)-1]
    sec_last_rsi = rsi_values[len(rsi_values)-2]
    
    print ("Just Ran")

                          #Placing Buy Order and Printing the order status if RSI crosses above Moving Average
    if last_rsi > a and sec_last_rsi < b:
        
        print("Crosses above condition has occured, placing a Buy order")

        ord = k.query_private('AddOrder', {'pair' : f'{trading_pair}', 'type' : 'buy', 'ordertype' : 'market', 'volume' : f'{qty}'})
        print(ord)
        

                          #Placing Sell Order and Printing the order status if RSI crosses above Moving Average
    if last_rsi < a and sec_last_rsi > b:
        
        print("Crosses below condition has occured, placing a Sell order")

        ord = k.query_private('AddOrder', {'pair' : f'{trading_pair}', 'type' : 'sell', 'ordertype' : 'market', 'volume' : f'{qty}'})
        print(ord)
        
        
    time.sleep(20)   #Define data refresh and condition checking interval in sec
