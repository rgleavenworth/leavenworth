import os
import configparser
from pathlib import Path
import json
from .glassnode_api import GlassnodeClient
from datetime import datetime
from pathlib import Path
from inspect import signature
from functools import wraps

# Should only be used on functions/methods that don't have keyword arguments
def typeassert(*ty_args, **ty_kwargs):
    def decorate(func):
        # Map function argument names to supplied types
        sig = signature(func)
        bound_types = sig.bind_partial(*ty_args, **ty_kwargs).arguments

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_values = sig.bind(*args, **kwargs)
            # Enforce type assertions across supplied arguments
            for name, value in bound_values.arguments.items():
                if name in bound_types:
                    if not isinstance(value, bound_types[name]):
                        raise TypeError(
                            'Argument {} must be {}'.format(name, bound_types[name])
                        )
            return func(*args, **kwargs)
        return wrapper
    return decorate

def configure_api_keys(api):
    """This returns API keys and if applicable passwords for APIs used by Leavenworth Capital as set in api.json. Define all location of secrets file in env variable = lc_secrets"""
    secrets_dir = os.getenv('lc_secrets')
    file = Path(secrets_dir, 'api.json')
    if not file.exists():
        print(f"WARNING: {file} file not found, you cannot continue. Can not trigger login to APIs used by Leavenworth Capital")
        raise Exception("api.json file not found, can not authenticate against APIs used by Leavenworth Capital")

    with open(file) as fin:
        settings = json.load(fin)
        api_key = settings.get(api)
    return api_key

GLASSNODE_API_KEY = configure_api_keys('glassnode')
gn = GlassnodeClient()
gn.set_api_key(GLASSNODE_API_KEY)

def _config(param, debug = False, sections = False):
    """Helper function to read config.ini file"""
    config = configparser.ConfigParser()
    configini = str(Path(__file__).resolve().parent/'config.ini')
    # abspath = os.path.dirname(os.path.abspath(__file__))
    try:
        if debug:
            print(f'Param being pulled is {param}')
            print(f'Reading config file in {configini}')
        config.read(configini)
    except:
        raise Exception('config.ini file not found')
    if sections:
        return(config.sections())
    if param not in config:
        raise Exception('Unknown parameter. Not configured in config file')
    # base configs for any connection are server, database, and driver
    global _value
    _value = config[param]['url']
    if debug:
        print('url for param %s is %s'%(param,_value))
    return(None)

def get_data(metric, currency = 'BTC', source = 'glassnode', debug = False, post_process = True):
    _config(metric, debug = debug)
    if source == 'glassnode':
        data = gn.get(_value, a = currency, debug = debug, post_process = post_process)
    return(data)

def validate_date(d, fmt = '%Y-%m-%d'):
    vd = datetime.strptime(d, fmt)
    return vd
    