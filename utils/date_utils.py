
from datetime import datetime, timedelta



def get_now_time(format_str = None):
    _now = datetime.now()
    return _now if format_str is None else _now.strftime(format_str)

def get_now_time_str(format_str="%Y-%m-%d %H:%M:%S,%f"):
    return get_now_time(format_str)


