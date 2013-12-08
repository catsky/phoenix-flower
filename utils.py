
from datetime import datetime, timedelta
import re
# from pytz import timezone


def timeadjust(dt):
    hours = timedelta(hours=8) # yohoo date is 9 hours faster than AU SYD
    return dt-hours

def timeformat(timestamp):
    #tz = timezone("Australia/Sydney")
    return datetime.fromtimestamp(timestamp).isoformat()

def calculate_score(votes, item_hour_age, gravity=1.8):  
    return (votes - 1) / pow((item_hour_age+2), gravity)

def formatURL(URL):
    pattern = r"(http://|https://)?([\w|\.]+)/*.*"
    m = re.match(pattern, URL)
    if m:
        return "%s" % m.group(2)
    else:
        return ''


if __name__ == '__main__':
    URL = "http://blog.jobbole.com/52355/"
    print formatURL(URL)