import requests
import pandas as pd
from .helpers import typeassert, configure_api_keys
from datetime import datetime, timedelta
from functools import reduce

intervals = ["1min", "5min", "15min", "30min", "1hour", "2hour", "4hour", "6hour", "12hour", "daily"]

# generate a function that retruns a tuple of unix timestamps from a start and end date
def get_unix_timestamps(start_date, end_date):
    """This routine returns a tuple of unix timestamps from a start and end date"""
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    start_date = int(start_date.timestamp())
    end_date = int(end_date.timestamp())
    return (start_date, end_date)

# generate a function that returns a tuple of unix timestamps from a period input
def get_unix_timestamps_from_period(period):
    """"This routine returns a tuple of unix timestamps from a period input"""
    if period == 'default':
        period = '1m'
    now = datetime.now()
    today = now.date().strftime('%Y-%m-%d')
    last_year =  datetime.now() - timedelta(days=1*365)
    ly_date = last_year.date().strftime('%Y-%m-%d')
    if period == '1d':
        start_date = today
        end_date = today
    elif period == '1w':
        start_date = today
        end_date = today
    elif period == '1m':
        start_date = today
        end_date = today
    elif period == '1y':
        start_date = ly_date
        end_date = today
    else:
        raise Exception('Invalid period. Supported values are 1d, 1w, 1m, 1y')
    return get_unix_timestamps(start_date, end_date)


@typeassert(endpoint=str, params=dict)
def api_call(endpoint, params=None):
    """This is the base call routine that pulls latest data from coinalyze.io for the given endpoint"""
    url = "https://api.coinalyze.net/v1/open-interest"
    api_key = configure_api_keys('coinalyze')
    base_url = "https://api.coinalyze.net/v1"
    url = base_url + endpoint
    r = requests.get(url, headers={'api-key': api_key}, params = params)
    if r.status_code != 200:
        raise Exception(f"Error calling coinalyze.io API: Return status code is {r.status_code}")
    else:
        data = r.json()
        return data

def exchanges():
    """This routine pulls all supported exchanges from coinalyze.io"""
    endpoint = "/exchanges"
    data = api_call(endpoint)
    return to_df(data)

@typeassert(market_type=str)
def supported_markets(market_type='future'):
    """This routine pulls all supported markets from coinalyze.io"""
    if market_type not in ['future', 'spot']:
        raise Exception('market_type must be either future or spot')
    endpoint = f"/{market_type}"+"-markets"
    data = api_call(endpoint)
    return to_df(data).drop_duplicates()

@typeassert(symbols=str)
def current_funding_rate(symbols='BTCUSDT_PERP.A,BTCUSD_PERP.0'):
    """This routine pulls current funding rates from coinalyze.io"""
    endpoint = "/funding-rate"
    params = {'symbols': symbols}
    data = api_call(endpoint, params=params)
    return to_df(data)

@typeassert(symbols=str)
def predicted_funding_rate(symbols='BTCUSDT_PERP.A,BTCUSD_PERP.0'):
    """This routine pulls predicted funding rates from coinalyze.io"""
    endpoint = "/predicted-funding-rate"
    params = {'symbols': symbols}
    data = api_call(endpoint, params=params)
    return to_df(data)

@typeassert(symbols=str)
def oi(symbols='BTCUSDT_PERP.A,BTCUSD_PERP.0'):
    """This routine pulls latest open-interest from coinalyze.io"""
    endpoint = "/open-interest"
    params = {'symbols': symbols}
    data = api_call(endpoint, params=params)
    return to_df(data)

@typeassert(symbols=str, interval=str, period=str)
def oi_history(symbols='BTCUSDT_PERP.A,BTCUSD_PERP.0', interval='daily', period=None):
    """This routine pulls historical open-interest from coinalyze.io"""
    endpoint = "/open-interest-history"
    if interval not in intervals:
        raise Exception(f"interval must be one of {intervals}")
    if period is None:
        period=get_unix_timestamps_from_period('default')
    else:
        period=get_unix_timestamps_from_period(period)
    params = {'symbols': symbols, 'interval': interval, 'from': period[0], 'to': period[1]}
    data = api_call(endpoint, params=params)
    return to_df(data, flatten=True)

@typeassert(symbols=str, interval=str, period=str)
def funding_rate_history(symbols='BTCUSDT_PERP.A,BTCUSD_PERP.0', interval='daily', period=None):
    """This routine pulls historical funding rates from coinalyze.io"""
    endpoint = "/funding-rate-history"
    if interval not in intervals:
        raise Exception(f"interval must be one of {intervals}")
    if period is None:
        period=get_unix_timestamps_from_period('default')
    else:
        period=get_unix_timestamps_from_period(period)
    params = {'symbols': symbols, 'interval': interval, 'from': period[0], 'to': period[1]}
    data = api_call(endpoint, params=params)
    return to_df(data, flatten=True)

@typeassert(symbols=str, interval=str, period=str)
def predicted_funding_rate_history(symbols='BTCUSDT_PERP.A,BTCUSD_PERP.0', interval='daily', period=None):
    """This routine pulls historical predicted funding rates from coinalyze.io"""
    endpoint = "/predicted-funding-rate-history"
    if interval not in intervals:
        raise Exception(f"interval must be one of {intervals}")
    if period is None:
        period=get_unix_timestamps_from_period('default')
    else:
        period=get_unix_timestamps_from_period(period)
    params = {'symbols': symbols, 'interval': interval, 'from': period[0], 'to': period[1]}
    data = api_call(endpoint, params=params)
    return to_df(data, flatten=True)

@typeassert(symbols=str, interval=str, period=str)
def liquidation_history(symbols='BTCUSDT_PERP.A,BTCUSD_PERP.0', interval='daily', period=None):
    """This routine pulls historical liquidations from coinalyze.io"""
    endpoint = "/liquidation-history"
    if interval not in intervals:
        raise Exception(f"interval must be one of {intervals}")
    if period is None:
        period=get_unix_timestamps_from_period('default')
    else:
        period=get_unix_timestamps_from_period(period)
    params = {'symbols': symbols, 'interval': interval, 'from': period[0], 'to': period[1]}
    data = api_call(endpoint, params=params)
    return to_df(data, flatten=True)

@typeassert(symbols=str, interval=str, period=str)
def long_short_history(symbols='BTCUSDT_PERP.A,BTCUSD_PERP.0', interval='daily', period=None):
    """This routine pulls historical long/short positions from coinalyze.io"""
    endpoint = "/long-short-ratio-history"
    if interval not in intervals:
        raise Exception(f"interval must be one of {intervals}")
    if period is None:
        period=get_unix_timestamps_from_period('default')
    else:
        period=get_unix_timestamps_from_period(period)
    params = {'symbols': symbols, 'interval': interval, 'from': period[0], 'to': period[1]}
    data = api_call(endpoint, params=params)
    return to_df(data, flatten=True)

@typeassert(symbols=str, interval=str, period=str)
def ohlcv_history(symbols='BTCUSDT_PERP.A,BTCUSD_PERP.0', interval='daily', period=None):
    """This routine pulls historical OHLC data from coinalyze.io"""
    endpoint = "/ohlcv-history"
    if interval not in intervals:
        raise Exception(f"interval must be one of {intervals}")
    if period is None:
        period=get_unix_timestamps_from_period('default')
    else:
        period=get_unix_timestamps_from_period(period)
    params = {'symbols': symbols, 'interval': interval, 'from': period[0], 'to': period[1]}
    data = api_call(endpoint, params=params)
    return to_df(data, flatten=True)

def time_unit(s):
    x=s.astype(str).apply(lambda x: len(x)).max()
    if x==10:
        return 's'
    elif x==13:
        return 'ms'
    else:
        raise ValueError('Invalid time unit')

def to_df(data, flatten=False):
    """This routine converts the data returned from coinalyze.io to a pandas dataframe"""
    if flatten:
        df = pd.json_normalize(data, meta=['symbol'], record_path =['history']).set_index('symbol')
        unit=time_unit(df['t'])
        df['t'] = pd.to_datetime(df['t'], unit=unit)
    else:
        df = pd.DataFrame(data)
    if 'update' in df.columns.tolist():
        unit=time_unit(df['update'])
        df['update'] = pd.to_datetime(df['update'], unit=unit)
    return df


def filter_markets(df, base_asset=["BTC"], quote_asset=["USD","USDT","BUSD","USDC"]):
    """This routine filters the markets based on the base and quote assets"""
    return df.query(f'base_asset=={base_asset} and quote_asset=={quote_asset} and is_perpetual==True')

def filter_exchanges(df, exchanges=["Binance", "BitMEX", "Bybit", "Deribit", "Bitfinex", "OKX", "HuobiDM", "Kraken"]):
    """This routine filters the markets based on the exchanges"""
    return df.query(f'name=={exchanges}')

def merge_exchange(df, ex):
    """This routine merges the exchange data with the market data"""
    return pd.merge(df, ex, left_on='exchange', right_on='code').set_index('name').reset_index()

def merge_markets(df, sm):
    """This routine merges data metrics with supported markets meta data"""
    return pd.merge(df, sm, on='symbol')

def merge_meta(df):
    """This routine merges the exchange and market meta data with the data metrics"""
    exchanges=exchanges()
    exchanges=filter_exchanges(exchanges)
    sm=supported_markets()
    sm=filter_markets(sm)
    if 'symbol' in df.columns.tolist():
        df=merge_markets(df, sm)
    if 'exchange' in df.columns.tolist():
        df=merge_exchange(df, exchanges)
    return df

def gen_symbols(df):
    symbols=list(df.symbol.unique())
    return ','.join(symbols)