
from datetime import datetime, timedelta
# from pytz import timezone


def timeadjust(dt):
    hours = timedelta(hours=8) # yohoo date is 9 hours faster than AU SYD
    return dt-hours

def timeformat(timestamp):
    #tz = timezone("Australia/Sydney")
    return datetime.fromtimestamp(timestamp).isoformat()

def calculate_score(votes, item_hour_age, gravity=1.8):  
    return (votes - 1) / pow((item_hour_age+2), gravity)