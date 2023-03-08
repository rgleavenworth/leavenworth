from fredapi import Fred
from .helpers import configure_api_keys

FRED_API_KEY = configure_api_keys('fred')
fred = Fred(api_key=FRED_API_KEY)

def fred_data(series, **kwargs):
    return fred.get_series(series, **kwargs)
    
def fred_search(series, **kwargs):
    return fred.search(series, **kwargs)

def fred_series_info(series, **kwargs):
    return fred.get_series_info(series, **kwargs)