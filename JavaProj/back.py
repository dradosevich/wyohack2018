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
import sys
import datetime
import os


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


def update_history(days, num_points, curr1, curr2):
    base_url = "http://coincap.io/history/"
    url = base_url + str(days) + "day/"

    print(curr2)
    global dai_down
    if dai_down is False:
        url1 = url + curr1
        jdata1 = requests.get(url1).json()
        df1 = pd.DataFrame(jdata1['price'])#[-num_points:])
        #print(df1.tail())
        global dai_df
        dai_df = df1
        dai_down = True

    url2 = url + curr2
    jdata2 = requests.get(url2).json()
    df2 = pd.DataFrame(jdata2['price'])#[-num_points:])

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


def plot_save(df, curr_pair, days):
    df = df.reset_index()
    df.columns = ["Date","Open","High",'Low',"Close"]

    df["Date"] = df["Date"].map(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))


    ohlc = df.tail(75)
    #print(df1.tail())
    ohlc["Date"] = ohlc["Date"].map(mdates.date2num)


    fig, ax = plt.subplots(figsize=(8,5))
    candlestick_ohlc(ax, zip(ohlc["Date"],
                         ohlc['Open'], ohlc['High'],
                         ohlc['Low'], ohlc['Close']), width=.6, colorup='b', colordown='r')

    plt.xlabel('Dates')
    plt.ylabel('Values')
    plt.legend(['Candlestick Plot ' + curr_pair])
    plt.grid(True)
    ax.xaxis_date()
    ax.autoscale_view()

    plt.savefig('./Charts/' + curr_pair + '.png')
    plt.close()



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

    slow_ma = ti.moving_average(ohlc_data.tail(slow_lookback + 2), 20).tail(2)
    fast_ma = ti.moving_average(ohlc_data.tail(fast_lookback + 2), 10).tail(2)
    if fast_ma.iloc[0,4] < slow_ma.iloc[0,4] and fast_ma.iloc[1,4] > slow_ma.iloc[1,4]:
        return "buy"
    elif fast_ma.iloc[0,4] > slow_ma.iloc[0,4] and fast_ma.iloc[1,4] < slow_ma.iloc[1,4]:
        return "sell"
    else:
        return "none"


def macd(ohlc_data):
    slow_ma = 15
    fast_ma = 8

    macd_data = ti.macd(ohlc_data, fast_ma, slow_ma).tail(2)
    if macd_data.iloc[0,6] < 0 and macd_data.iloc[1,6] > 0:
        return "buy"
    elif macd_data.iloc[0,6] > 0 and macd_data.iloc[1,6] < 0:
        return "sell"
    else:
        return "none"

def compare_all(base_currency, test_type, download, days):
    all_symbols = get_currency_pairs()

    fileout = "Market.csv"
    outfile = open(fileout, 'w', newline='')
    crypto_writer = csv.writer(outfile, delimiter=',')
    crypto_writer.writerow(['Pair','Signal', "Price"])

    if download is 1:
        save_data(days)

    base_df = []
    quote_df = []
    try:
        base_df = load_data(base_currency, days)
        base_df.columns = ['time', 'price']
    except:
        print("could not load base currency")
        exit(1)

    for symbol in all_symbols:
        crypto_pair = base_currency + symbol[0]
        try:
            quote_df = load_data(symbol[0], days)
            quote_df.columns = ['time', 'price']
        except:
            continue

        crypto_df = base_df.copy()
        crypto_df['price'] = base_df['price'] / quote_df['price']
        ohlc_data = format_as_ohlc(crypto_df, '1D')

        if test_type is 1:
            result = ma_crossover(ohlc_data)
        elif test_type is 2:
            result = macd(ohlc_data)
        else:
            r1 = ma_crossover(ohlc_data)
            if r1 is "none":
                continue
            else:
                r2 = macd(ohlc_data)
                if r1 is r2:
                    result = r1
                else:
                    result = "none"

        if result is "buy":
            crypto_writer.writerow([crypto_pair, "buy", ohlc_data.tail(1).iloc[0,3]])
            plot_save(ohlc_data, crypto_pair, days)
        elif result is "sell":
            crypto_writer.writerow([crypto_pair, "sell", ohlc_data.tail(1).iloc[0,3]])
            plot_save(ohlc_data, crypto_pair, days)



    outfile.close()

#Load csv files into pandas dataframe
def load_data(currency, days):
    try:
        file_path = os.path.join("Data", currency)
        file_path = file_path + str(days) + '.csv'
        load_df = pd.read_csv(file_path, sep='\t', index_col= 0)
    except ValueError:
        print("Can't find this file")
    return load_df


def save_data(days):
    url = "http://coincap.io/coins"
    jdata = requests.get(url).json()

    base_url = "http://coincap.io/history/"
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
            df_curr.to_csv('./Data/' + curr + '.csv', sep='\t')
            saved_curr.append(curr)
            list_files = curr + str(days) + '.csv'
            print(curr)
        except:
            not_saved_curr.append(curr)
            print(not_saved_curr)

    global saved
    saved = True

    return saved_curr, not_saved_curr, list_files

if __name__ == '__main__':
    charts = os.listdir("Charts")
    for chart in charts:
        try:
            os.remove(os.path.join("Charts", chart))
        except:
            continue
    days = 90
    test_type = int(sys.argv[1])
    base_currency = sys.argv[2]
    download = int(sys.argv[3])

    compare_all(base_currency, test_type, download, days)
