#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 17:10:32 2020

@author: jpgrewal
"""

#Execute from command line with second argument as the location of the json data (Example below)
#Example:  $python GameHiveTest_JPGrewal.py sample_json.txt
#Please Note: not telling you how to execute, lol, but thought I should include
#             this small blurb because I'm over-documenting the hell out of
#             this assignment anyway :)

import pandas as pd
import sys

#===Problem A: Begin===========================================================
# a) Write a script that ingests this JSON data and transforms it into a dataframe that is easy 
#    to use for further analysis.

#json data file location
file_link = sys.argv[1]

#ingest json data into dataframe
df = pd.read_json(file_link)

#establish empty list variable to store series data for each of the two sku's in the file
ls=[]

#loop to append series data for each sku to a list
for index, row in df.iterrows():
    ls.append(row['inappproduct'])

#create data frame for each sku (gamehive_game1_product1 and gamehive_game1_bundle1)
df1 = pd.DataFrame(ls[0])
df2 = pd.DataFrame(ls[1])

#transform individual sku dataframes by expanding out the prices column, and dropping unneeded rows(axis=0) and columns(axis=1)
df_final1 = pd.concat([df1, df1['prices'].apply(pd.Series)], axis = 1).drop('prices', axis = 1).drop('defaultPrice', axis = 1).drop('en-US', axis = 1).drop('status', axis = 1).drop('purchaseType', axis = 1).drop(0, axis=1).drop('currency',axis=0).drop('defaultLanguage',axis=0).drop('listings',axis=0).drop('priceMicros', axis=0)
df_final2 = pd.concat([df2, df2['prices'].apply(pd.Series)], axis = 1).drop('prices', axis = 1).drop('defaultPrice', axis = 1).drop('en-US', axis = 1).drop('status', axis = 1).drop('purchaseType', axis = 1).drop(0, axis=1).drop('currency',axis=0).drop('defaultLanguage',axis=0).drop('listings',axis=0).drop('priceMicros', axis=0)

#assign country code its' own column and reset the index on both individual sku dataframes
df_final1['countryCode'] = df_final1.index
df_final1 = df_final1.reset_index().drop('index',axis=1)
df_final2['countryCode'] = df_final2.index
df_final2 = df_final2.reset_index().drop('index',axis=1)

#updating the secondary sku dataframe indexes so they do not conflict when both dataframes are combined
df_final2.index = df_final2.index + len(df_final1)

#combine both sku dataframes
df_final = df_final1.append(df_final2)

#extract the priceMicros values and store it seperately as a float
df_temp = df_final.priceMicros.astype(float)

#use extracted float values in the previous line to calculate price and add it as a new column in the dataframe
df_final['price'] =  round(df_temp/ 1000000,2)

#format the dataframe to look like the table diagram on the test sheet provided
df_final = df_final[['packageName','sku','countryCode','currency','price']]

#display the dataframe
print('Problem A')
print(df_final)

#===Problem A: End=============================================================

print('\n\n\n') #making some spaces for better viewing in the command window

#===Problem B: Begin===========================================================
# b) Add new column to the dataframe that you created in part a) named “usd_price” which
#    contains the USD equivalent to the values in the “price” column. The USD prices in this column
#    must be rounded to the nearest two decimal places.

#create dictionary of US exchange rates for each currency, include USD with value of 1
fx = {'currency':['DZD','AUD','CAD','EUR','JPY','RUB','SGD','KRW','GBP','USD'],'rate':[119.32,1.40,1.34,0.89,111.93,63.81,1.36,1140.98,0.77,1.00]}

#create data frame from exchange rate dictionary
dfx = pd.DataFrame(fx)

#merge exchange rate data with dataframe from previous question, join on currency
df_final = pd.merge(df_final, dfx, on='currency', how='left')

#calculate new column 'usd_price' based on exchange rate data
df_final['usd_price'] = round(df_final.price / df_final.rate,2)

#format data frame to exclude rate information, and only include newly requested column: usd_price
df_final = df_final[['packageName','sku','countryCode','currency','price','usd_price']]

#display the dataframe
print('Problem B')
print(df_final)
#===Problem B: End=============================================================