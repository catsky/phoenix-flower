
from datetime import datetime, timedelta
# from pytz import timezone


def timeadjust(dt):
    hours = timedelta(hours=9) # yohoo date is 9 hours faster than AU SYD
    return dt-hours

def timeformat(timestamp):
    #tz = timezone("Australia/Sydney")
    return datetime.fromtimestamp(timestamp).isoformat()