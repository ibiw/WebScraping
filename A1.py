from pandas_datareader import data
import pandas as pd
import datetime
import time
from functools import wraps

class maAnalysis():

    ten_year = (datetime.datetime.now() - datetime.timedelta(3650)).strftime('%Y, %m, %d')
    # now = datetime.datetime.now().strftime('%Y, %m, %d')
    df = None

    def __str__(self):
        return('MA Analysis.')
    
    def __init__(self):
        # self.df = None
        pass
    
    @classmethod
    def getSymbol(cls, symbol):
        cls.df = data.DataReader(symbol, 'yahoo', cls.ten_year)

    @classmethod
    def ma(cls, *args):
        df = cls.df
        for arg in args:
            column_name = 'ma' + str(arg)
            df[column_name] = pd.Series.rolling(df.Close, window = arg, center = False).mean()
        df = df[['Close', 'ma5', 'ma10', 'ma50', 'ma200']]
        return df

def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwagrs):
        t0 = time.time()
        result = function(*args, **kwagrs)
        t1 = time.time()
        print('Total time running %s: %s seconds' %(function.__name__, str(t1 - t0)))
        return result
    return function_timer

def main():
        maAnalysis.getSymbol('ftnt')
        df = maAnalysis.ma(5, 10, 50, 200)
        df = df.tail(1)
        # print(df.index[0])
        now = str(df.index[0]).split()[0]
        # print(now)
        print(df.T.sort_values(by = now).T)
        random_sort(100)

@fn_timer
def random_sort(n):
    import random
    return sorted([random.random() for i in range(n)])

if __name__ == '__main__':
    main()