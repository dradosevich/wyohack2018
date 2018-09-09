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
import datetime


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
    df1.columns = ["Date","Open","High",'Low',"Close"]

    df1["Date"] = df1["Date"].map(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))

    if isinstance(df1['Date'][0],datetime.datetime):
        print("It's datetime")

    #df2 = df2.reset_index()
    #df2.columns = ["Date","Open","High",'Low',"Close", "MA"]

    ax = df1.plot(x='Date', y='MA')
    df1.plot(ax=ax, x='Date', y='MA')

    ohlc = df1
    ohlc["Date"] = ohlc["Date"].map(mdates.date2num)
    #print(ohlc.head())
    
    #ohlc = ohlc.reset_index()
    #print(ohlc.head()))
    #ohlc.columns = ["Date","Open","High",'Low',"Close", "MA"]
    
    if isinstance(ohlc['Date'][0],datetime.datetime):
        print("It's datetime")
    print(ohlc.head())
    
    """
    if isinstance(ohlc['Date'],str):
        print("It's str")
    else:
        print("It's not")
    """
    print(ohlc.values)
  
    f1, ax = plt.subplots(figsize=(8,5))
    candlestick_ohlc(f1, ohlc.values, width=.6, colorup='b', colordown='r')
    #f1.xaxis_date()
    #f1.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d %H:%M:%S'))

    plt.grid(True)
    ax.xaxis_date()
    ax.autoscale_view()
    #plt.xticks(rotation=45)
    #plt.ylabel('Stock Price')
    #plt.xlabel('Date Hours:Minutes')
    plt.show()
    



def ma(df, n):
    ma_df = ti.moving_average(df, n)
    return ma_df


def format_as_ohlc(df, timeframe):
    df['time'] = pd.to_datetime(df['time'],unit='ms')
    df = df.set_index(pd.DatetimeIndex(df['time']))
    data_ohlc =  df['price'].resample(timeframe).ohlc()

    data_ohlc = data_ohlc.dropna()

    data_ohlc = data_ohlc.rename(index=str, columns = {'time': 'Time', 'open': 'Open', 'low':'Low', 'high': 'High', 'close': 'Close'})

    return data_ohlc

def ma_crossover(ohlc_data):
    slow_lookback = 20
    fast_lookback = 10

    slow_ma = ma(ohlc_data.tail(slow_lookback + 2), 20).tail(2)
    fast_ma = ma(ohlc_data.tail(fast_lookback + 2), 10).tail(2)
    if fast_ma.iloc[0,4] < slow_ma.iloc[0,4] and fast_ma.iloc[1,4] > slow_ma.iloc[1,4]:
        return "buy"
    elif fast_ma.iloc[0,4] > slow_ma.iloc[0,4] and fast_ma.iloc[1,4] < slow_ma.iloc[1,4]:
        return "sell"
    else:
        return "none"

def relative_strength_index(ohlc_data):
    RSI_k = 14
    overbought_val = 70
    oversold_val = 30

    rsi_data = ti.relative_strength_index(ohlc_data, RSI_k).tail(1)

    print(rsi_data)
    if(rsi_data.iloc[0,4] > overbought_val):
        return "sell"
    elif (rsi_data.iloc[0,4] < oversold_val):
        return "buy"
    else:
        return "none"

def macd(ohlc_data):
    slow_ma = 15
    fast_ma = 8

    macd_data = ti.macd(ohlc_data, fast_ma, slow_ma).tail(2)
    print(macd_data)
    if macd_data.iloc[0,6] < 0 and macd_data.iloc[1,6] > 0:
        return "buy"
    elif macd_data.iloc[0,6] > 0 and macd_data.iloc[1,6] < 0:
        return "sell"
    else:
        return "none"

def compare_all():
    all_symbols = get_currency_pairs()
    count = 0
    buy_list = []
    sell_list = []
    fileout = "Market.csv"
    outfile = open(fileout, 'w', newline='')
    crypto_writer = csv.writer(outfile, delimiter=',')

    for symbol in all_symbols:
        crypto_pair = "DAI" + symbol[0]
        try:
            crypto_df = update_history(7,25, 'DAI', symbol[0])
        except:
            count = count + 1
            continue

        ohlc_data = format_as_ohlc(crypto_df, '5Min')
        result = ma_crossover(ohlc_data)
        result2 = macd(ohlc_data)
        if result is "buy" or result is "sell":
            crypto_writer.writerow([crypto_pair, result, ohlc_data.tail(1).iloc[0,3]])
        if count is 10:
            return
        count = count + 1

    for pair in buy_list:
        print(pair + "\t buy")
    for pair in sell_list:
        print(pair + "\t sell")

    outfile.close()


#Load csv files into pandas dataframe
def load_data(filename):
    load_df = pd.read_csv(filename)
    return load_df

def save_data(days):
    url = "http://coincap.io/coins"
    jdata = requests.get(url).json()

    base_url = "http://coincap.io/history"
    url = base_url + str(days) + "day/"

    saved_curr = []
    not_saved_curr = []
    
    #List of filenames saved
    list_files = []
    for curr in jdata:
        try:
            url_curr = url + curr
            jdata1 = requests.get(url_curr).json()
            df_curr = pd.DataFrame(jdata1['price'])
            df_curr.to_csv(curr + str(days) + '.csv', sep='\t')
            saved_curr.append(curr)
            list_files = curr + str(days) + '.csv'
        except:
            not_saved_curr.append(curr)

    global saved
    saved = True

    return saved_curr, not_saved_curr, list_files

if __name__ == '__main__':
    df_rel = update_history(1, 20, "BTC", "DOGE")
    ohlc_df = format_as_ohlc(df_rel, "5Min")
    #ma_df = ma(ohlc_df, 10)
    ma_plot(ohlc_df, df_rel)
    #compare_all()
