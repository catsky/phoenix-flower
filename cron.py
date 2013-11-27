from database import ServiceDB

import urllib2
from datetime import datetime
from utils import timeformat, timeadjust
import time
import sys


def getAUDCNY():
    API = "http://download.finance.yahoo.com/d/quotes.csv?e=.csv&f=sl1d1t1&s=AUDCNY=x"
    try:
        response = urllib2.urlopen(API)
        content = response.read()
        content = content.split(',')
        print content
        name = content[0].split('=')[0].strip('"')
        report_t = "%s %s" % (content[2].strip('"'), content[3].replace('\r\n','').strip('"'))
        dt = datetime.strptime(report_t, "%m/%d/%Y %I:%M%p")
        t = time.mktime(timeadjust(dt).timetuple())
        value = content[1]
                
    except:
        print "Error:getAUDCNY()"
        return None
    print "name: %s, time:%s, value:%s" % (name, t, value)
    return (name, t, value)


if __name__ == '__main__':
    option = '--minutes'
    if len(sys.argv) > 1 and sys.argv[1] == '--hours':
        option = '--hours'
    money = getAUDCNY()
    db = ServiceDB()
    if option == '--minutes':
        db.saveMoneyMinutes(money)
        print "saved minutes!"
    elif option == '--hours':
        db.saveMoneyHours(money)
        print "saved hours!"
    
   