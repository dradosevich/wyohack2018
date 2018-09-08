# -*- coding: utf-8 -*-
"""
Damir Pulatov
Backend for WyoHackathon2018
"""

import requests
import pandas as pd
import json 
import matplotlib.pyplot as plt
import technical_indicators as ti


#Request updated info
def update_front(url):
    jdata = requests.get(url).json()
    df = pd.DataFrame(jdata)
    return df


#Update historical data
def update_history(days, num_points, curr1, curr2):
    base_url = "http://coincap.io/history/"
    url = base_url + str(days) + "day/"
    url1 = url + curr1
    url2 = url + curr2
    
    jdata1 = requests.get(url1).json()
    jdata2 = requests.get(url2).json()
    
    df1 = pd.DataFrame(jdata1['price'][-num_points:])
    df2 = pd.DataFrame(jdata2['price'][-num_points:])
    
    #Get relative value
    relative_value = df1[1] / df2[1]
    
    df_rel = df1
    df_rel[1] = relative_value
    
    df_rel = df_rel.rename(index=str, columns = {0: 'time', 1: 'price'})
    return df_rel
    

def compare(df, curr1, curr2):
    price1 = df.loc[df['long'] == curr1]
    price1 = price1['price'][0]
    
    price2 = df.loc[df['long'] == curr2]
    price2 = price2['price'][1]
    
    #Calculate relative price
    base_price = price1
    rel_price = price2 - base_price
    
    return base_price, rel_price 


def rel_plot(df):
    df.plot(x='time', y='price')


def ma(df, n):
    ma_df = ti.moving_average(df, n)
    return ma_df


def convert_data(df, timeframe):
    df['time'] = pd.to_datetime(df['time'],unit='ms')
    df = df.set_index(pd.DatetimeIndex(df['time']))
    data_ohlc =  df['price'].resample(timeframe).ohlc()
    
    data_ohlc = data_ohlc.dropna()
    
    data_ohlc = data_ohlc.rename(index=str, columns = {'time': 'Time', 'open': 'Open', 'low':'Low', 'high': 'High', 'close': 'Close'})
    
    return data_ohlc

if __name__ == '__main__':
    url = "http://coincap.io/front"
    df = update_front(url)
    base_price, rel_price = compare(df, "Bitcoin", "Ethereum")
    relative_df = update_history(1, 100, 'BTC', 'DOGE')
    rel_plot(relative_df)
    
    converted_data = convert_data(relative_df, '5Min')
    #print(converted_data)
    slow_ma = ma(converted_data, 20)
    fast_ma = ma(converted_data, 10)
    #print(ma_df)
    