from .helpers import get_data, _config

# class glassnode:
#     def __init__(self, **kwargs):
        
def glassnode(metric, currency = 'BTC', debug = False, post_process = True):
    """
    Required arguments:
        metric: not case-sensitive. Get a list of all supported metrics with glassnode_params() method
    Typical usage:
        df = glassnode('PRICE') 
    """
    data = get_data(metric.upper(), currency = currency, source = 'glassnode', debug = debug,  post_process = post_process)
    return(data)

def glassnode_params():
    metrics = _config('', sections = True)
    return metrics