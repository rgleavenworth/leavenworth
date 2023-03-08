import yfinance as yf
import pandas as pd
import janitor
import numpy as np
from datetime import datetime

now = datetime.now()
start_date = now.date().replace(year=now.year -1,month=1, day=1).strftime('%Y-%m-%d')

def _returns(df, t, period = 'month'):
    if period == 'day':
        s = (df[t].pct_change()).round(4)
    elif period == 'month':
        s = (df.resample('M').last()[t].pct_change()).round(4)
    elif period == 'quarter':
        s = (df.resample('Q').last()[t].pct_change()).round(4)
    elif period == 'year':
        s = (df.resample('Y').last()[t].pct_change()).round(4)
    elif period == 'inception':
        s = (((df[t].pct_change())+1).cumprod()-1).round(4)
    else:
        raise Exception('Invalid period.')
    return s

def _dr(df, t, period = 60, method = 'mean', log = False, percent = True):
    if log:
        s =  np.log(df[t].div(df[t].shift(1)))
    else:
        s =  (df[t].div(df[t].shift(1)))
    if method == 'mean':
        s = s.rolling(period).mean()
    elif method == 'std':
        s = s.rolling(period).std()
    else:
        raise Exception('Unknown method. Allowed methods are mean and std')
    if percent:
        return s*100
    else:
        return s

def daily_returns(df, period = 60, method = 'mean', log = False, percent = True):
    dr = pd.DataFrame()
    tickers = df.columns.tolist()
    for ticker in tickers:
        s = _dr(df, ticker, period = period, method = method, log = log, percent = percent)
        dr[ticker] = s
    return(dr)

def yahoo(tickers, period = '1y', debug = False, pivot = True):
    price = pd.DataFrame()
    for ticker in tickers:
        if debug:
            print('Pulling Ticker %s'%ticker)
        s = yf.Ticker(ticker)
        h = s.history(period = period)
        h['TICKER'] = ticker
        price = price.append(h)
    price = price.reset_index().clean_names(case_type = 'upper')
    if pivot:
        pivot = price.reset_index().pivot_table(index = 'DATE', columns = 'TICKER', values = 'CLOSE', aggfunc = 'mean')
        pivot = pivot.fillna(method = 'pad')
        return pivot
    else:
        return price
   
def prep_returns(df, period = 'month', fix_resample = True):
    """Typical usage:
    >>> prep_returns(data, period = 'inception')
    For daily returns
    >>> prep_returns(data, period = 'day')
    Other supported periods are month (default), year (for YTD), and quarter
    """
    r = pd.DataFrame()
    tickers = df.columns.tolist()
    for ticker in tickers:
        s = _returns(df, ticker, period = period)
        r[ticker] = s
    r = r.reset_index()
    # Fix resample fields
    if fix_resample:
        if period == 'month':
            r['MONTH'] = r.DATE.apply(lambda x: x.strftime("%Y-%b"))
        elif period == 'year':
            r = r.dropna().tail(1)
            r = r.rename_column('DATE', 'YTD')
            r = r.clean_names(case_type = 'upper')
            r.loc[r.index.values[0], 'YTD'] = 'YTD'
            r = r.set_index('YTD')
        elif period == 'inception':
            r = r.dropna().tail(1)
            r = r.rename_column('DATE', 'INCEPTION')
            r = r.clean_names(case_type = 'upper')
            r.loc[r.index.values[0], 'INCEPTION'] = 'INCEPTION'
            r = r.set_index('INCEPTION')            
        elif period == 'quarter':
            pass
        else:
            raise Exception('Incorrect period')
    return(r)

def sp500():
    payload=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    first_table = payload[0]
    df = first_table.clean_names(case_type = 'upper')
    return df