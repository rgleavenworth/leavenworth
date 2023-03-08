import requests
import pandas as pd
from datetime import datetime
import janitor

def fng(limit = 30):
    url = "https://api.alternative.me/fng/"
    p = {}
    if limit:
        p['limit'] = limit
        
    r = requests.get(url, params=p)
    if r.status_code != 200:
        raise Exception(f"Error calling Fear and Greed API: Return status code is {r.status_code}")
    else:
        d = r.json()['data']
        df = pd.DataFrame.from_dict(d)
        df['timestamp'] = df.timestamp.astype(int)
        df['timestamp'] = df.timestamp.apply(lambda x: datetime.fromtimestamp(x))
        df['value'] = df.value.astype(int)
        df = df.clean_names(case_type = 'upper')
        return df