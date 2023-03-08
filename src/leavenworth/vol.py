import requests
import pandas as pd
from .helpers import configure_api_keys, validate_date
from datetime import datetime, timedelta
now = datetime.now()
today = now.date().strftime('%Y-%m-%d')
last_year =  datetime.now() - timedelta(days=1*365)
ly_date = last_year.date().strftime('%Y-%m-%d')


def bitvol(start_date = ly_date, end_date = today, currency = 'BTC'):
    """
    Typical usage:
        df = bitvol(start_date = '2022-01-01', end_date = '2022-05-31', currency = 'BTC")
        Defaults
            start_date = date from 1 year ago
            end_date = today's date
    """
    if currency.upper() not in ["BTC", "ETH"]:
        raise Exception('Invalid currency. Supported values are BTC and ETH')
    try:
        start_date = validate_date(start_date)
    except:
        raise Exception('start_date is not a valid date. Allowed format is of the type "2022-01-01"')
    try:
        end_date = validate_date(end_date)
    except:
        raise Exception('end_date is not a valid date. Allowed format is of the type "2022-01-01"')
    start_date = start_date.date().strftime('%Y-%m-%d-%H-%M-%S')
    end_date = end_date.date().strftime('%Y-%m-%d-%H-%M-%S')
    key = configure_api_keys('bitvol')
    url = "https://crypto-volatility-index.p.rapidapi.com/history/%s/day/"%currency.upper()
    headers = {
    'x-rapidapi-host': "crypto-volatility-index.p.rapidapi.com",
    'x-rapidapi-key': key
    }
    url = url+start_date+'/'+end_date
    response = requests.request("GET", url, headers = headers)
    s = response.json()
    df = pd.DataFrame.from_dict(s[0])
    df['datetime'] = pd.to_datetime(df.datetime)
    df = df.set_index('datetime')
    return df
