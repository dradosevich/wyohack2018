"""
Damir Pulatov
Backend for WyoHackathon2018
"""

import requests
import pandas as pd
import json
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
from mpl_finance import candlestick_ohlc
import technical_indicators as ti
import csv


#Indicate whether dai is in memory
dai_down = False

#Store dai history in memory
dai_df = []

#Indicate whether historic data is saved into csv
saved = False

#Request updated info
def update_front(url):
    jdata = requests.get(url).json()
    df = pd.DataFrame(jdata)
    return df


#Update historical data
def update_history(days, num_points, curr1, curr2):
    base_url = "http://coincap.io/history/"
    url = base_url + str(days) + "day/"

    print(curr2)
    global dai_down
    if dai_down is False:
        url1 = url + curr1
        jdata1 = requests.get(url1).json()
        df1 = pd.DataFrame(jdata1['price'][-num_points:])
        global dai_df
        dai_df = df1
        dai_down = True

    url2 = url + curr2
    jdata2 = requests.get(url2).json()
    df2 = pd.DataFrame(jdata2['price'][-num_points:])

    df1 = dai_df

    #Get relative value
    relative_value = df1[1] / df2[1]

    df_rel = df1
    df_rel[1] = relative_value

    df_rel = df_rel.rename(index=str, columns = {0: 'time', 1: 'price'})
    return df_rel

def get_currency_pairs():
    url = "http://coincap.io/coins"
    jdata = requests.get(url).json()
    currency_list = csv.reader(jdata)
    return list(currency_list)

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


def ma_plot(df1, df2):
    df1 = df1.reset_index()
    df1.columns = ["Date","Open","High",'Low',"Close", "MA"]

    df2 = df2.reset_index()
    df2.columns = ["Date","Open","High",'Low',"Close", "MA"]

    #ax = df1.plot(x='Date', y='MA')
    #df2.plot(ax=ax, x='Date', y='MA')

    ohlc = df1
    ohlc['Date'] = ohlc['Date'].map(mdates.date2num)

    f1 = plt.subplot2grid((6, 4), (1, 0), rowspan=6, colspan=4, axisbg='#07000d')
    candlestick_ohlc(f1, df.values, width=.6, colorup='#53c156', colordown='#ff1717')
    f1.xaxis_date()
    f1.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d %H:%M:%S'))

    plt.xticks(rotation=45)
    plt.ylabel('Stock Price')
    plt.xlabel('Date Hours:Minutes')
    plt.show()



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

def ma_crossover(slow_ma, fast_ma):
    if fast_ma.iloc[0,4] < slow_ma.iloc[0,4] and fast_ma.iloc[1,4] > slow_ma.iloc[1,4]:
        #upward ma_crossover, buy signal
        return "buy"
    elif fast_ma.iloc[0,4] > slow_ma.iloc[0,4] and fast_ma.iloc[1,4] < slow_ma.iloc[1,4]:
        #downward ma_crossover, sell signal
        return "sell"
    else:
        return "none"


def compare_all():
    all_symbols = get_currency_pairs()
    count = 0
    signal_list = []
    for symbol in all_symbols:
        crypto_pair = "DAI/" + symbol[0]
        try:
            relative_df = update_history(1,25, 'DAI', symbol[0])
        except:
            continue
        # print(crypto_pair)
        converted_data = convert_data(relative_df, '5Min')
        slow_ma = ma(converted_data, 20)
        fast_ma = ma(converted_data, 10)

        result = ma_crossover(slow_ma.tail(2), fast_ma.tail(2))
        # print(result)
        if result is "buy" or "sell":
            signal_list.append(crypto_pair)
        else:
            continue
        # if count is 10:
        #     return
        # count = count + 1

    for pair in signal_list:
        print(pair)


#Download and save data into csv file
def save_data(filename, days):
    url = "http://coincap.io/coins"
    jdata = requests.get(url).json()

    base_url = "http://coincap.io/history/"
    url = base_url + str(days) + "day/"
    
    saved_curr = []
    not_saved_curr = []
    for curr in jdata:
        try:
            url_curr = url + curr
            jdata1 = requests.get(url_curr).json()
            df_curr = pd.DataFrame(jdata1['price'])
            df_curr.to_csv(filename + '_' + curr + str(days) + '.csv', sep='\t')
            saved_curr.append(curr)
        except:
            not_saved_curr.append(curr)


    global saved
    saved = True

if __name__ == '__main__':
    
    print('working')
    
    #list_not_saved = save_data('price', 1)
    #print(list_not_saved)
    #url = "http://coincap.io/front"
    #df = update_front(url)
    #base_price, rel_price = compare(df, "Bitcoin", "Ethereum")
    #relative_df = update_history(1, 100, 'BTC', 'DOGE')
    #rel_plot(relative_df)


    #converted_data = convert_data(relative_df, '15Min')
    #print(converted_data)
    #slow_ma = ma(converted_data, 20)
    #fast_ma = ma(converted_data, 10)
    #print(ma_df)

    #ma_plot(slow_ma, fast_ma)

    #compare_all()