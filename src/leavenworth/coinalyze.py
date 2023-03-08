import requests
import pandas as pd
from .helpers import typeassert, configure_api_keys

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
    return data

@typeassert(market_type=str)
def supported_markets(market_type='future'):
    """This routine pulls all supported markets from coinalyze.io"""
    if market_type not in ['future', 'spot']:
        raise Exception('market_type must be either future or spot')
    endpoint = f"/{market_type}"
    data = api_call(endpoint)
    return data

@typeassert(symbols=str)
def current_funding_rate(symbols='BTCUSDT_PERP.A,BTCUSD_PERP.0'):
    """This routine pulls current funding rates from coinalyze.io"""
    endpoint = "/funding-rate"
    params = {'symbols': symbols}
    data = api_call(endpoint, params=params)
    return data

@typeassert(symbols=str)
def predicted_funding_rate(symbols='BTCUSDT_PERP.A,BTCUSD_PERP.0'):
    """This routine pulls predicted funding rates from coinalyze.io"""
    endpoint = "/predicted-funding-rate"
    params = {'symbols': symbols}
    data = api_call(endpoint, params=params)
    return data

@typeassert(symbols=str)
def oi(symbols='BTCUSDT_PERP.A,BTCUSD_PERP.0'):
    """This routine pulls latest open-interest from coinalyze.io"""
    endpoint = "/open-interest"
    params = symbols
    data = api_call(endpoint, params=params)
    return data

@typeassert(symbols=str)
def oi_history(symbols='BTCUSDT_PERP.A,BTCUSD_PERP.0'):
    """This routine pulls historical open-interest from coinalyze.io"""
    endpoint = "/open-interest-history"
    params = {'symbols': symbols}
    data = api_call(endpoint, params=params)
    return data

@typeassert(symbols=str)
def funding_rate_history(symbols='BTCUSDT_PERP.A,BTCUSD_PERP.0'):
    """This routine pulls historical funding rates from coinalyze.io"""
    endpoint = "/funding-rate-history"
    params = {'symbols': symbols}
    data = api_call(endpoint)
    return data

@typeassert(symbols=str)
def predicted_funding_rate_history(symbols='BTCUSDT_PERP.A,BTCUSD_PERP.0'):
    """This routine pulls historical predicted funding rates from coinalyze.io"""
    endpoint = "/predicted-funding-rate-history"
    params = {'symbols': symbols}
    data = api_call(endpoint, params=params)
    return data

@typeassert(symbols=str)
def liquidation_history(symbols='BTCUSDT_PERP.A,BTCUSD_PERP.0'):
    """This routine pulls historical liquidations from coinalyze.io"""
    endpoint = "/liquidation-history"
    params = {'symbols': symbols}
    data = api_call(endpoint, params=params)
    return data

@typeassert(symbols=str)
def long_short_history(symbols='BTCUSDT_PERP.A,BTCUSD_PERP.0'):
    """This routine pulls historical long/short positions from coinalyze.io"""
    endpoint = "/long-short-ratio-history"
    params = {'symbols': symbols}
    data = api_call(endpoint, params=params)
    return data

@typeassert(symbols=str)
def ohlcv_history(symbols='BTCUSDT_PERP.A,BTCUSD_PERP.0'):
    """This routine pulls historical OHLC data from coinalyze.io"""
    endpoint = "/ohlcv-history"
    params = {'symbols': symbols}
    data = api_call(endpoint, params=params)
    return data

def to_df(data):
    """This routine converts the data returned from coinalyze.io to a pandas dataframe"""
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df