                                      THIS IS A CRYPTO TRADING BOT FOR KRAKEN 
                                      
Buy Rule : RSI inidcator crosses above RSI moving average 
Sell Rule : RSI indicator crosses below RSI moving average

Note : Pair, Trading Quantity, RSI period and RSI Moving Average period will be asked from the user.


The bot fetches 1 min candles from Kraken every 20 secs. It will then calculate RSI value based on closing price of 1 min candles.
Buy and Sell orders will be placed as per the rules mentioned above. Either of the positions will be taken first depending on 
which condition is meeting fist.

Important Instruction:

API Key and Secret Key must be obtained from your kraken account for authentication. Create a text file, copy API and Secret in
first line and second line of the file respectively and save the file with '.key' extension in the same folder as the .py file.
          
Warnings & Areas of Improvement : 

1) The bot does not verify if the entry trade was completely filled and hence if the exit condition meets before the entry
   quantity is completely filled, an exit order for more than the entry quantity will be placed. This should not be a 
   problem in most cases as the orders are market order.

2) If kraken fails to send data correctly, NaN values can occur and indicator calculation might be affected. NaN values 
   in the price can be replaced by average price.
