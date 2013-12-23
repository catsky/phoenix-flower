#!/bin/env python
# -*- coding: utf-8 -*-

import urllib2, lxml.html, os
from datetime import datetime
from utils import timeadjust
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


def petrolCapture(imgstorepath):
    BASEURL = 'http://www.accc.gov.au'
    IMGSTORE = imgstorepath
    
    #fetch the source data of petrol price from accc australia
    accchttp = urllib2.urlopen('http://www.accc.gov.au/consumers/petrol-diesel-and-lpg/recent-city-petrol-prices')
    data = accchttp.read()
    accchttp.close()
    doc = lxml.html.document_fromstring(data)
    
    
    #get the data of cheapest in last week
    t1 = doc.xpath('/html/body/div/div/div[3]/div/div[2]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr/td/text()')
    cheapest = [item for item in t1 if item != '\n']  
    db.savePetrolCheapest(cheapest)
    
    #get the charts of major cities
    xpaths = {'sydney':'/html/body/div/div/div[3]/div/div[2]/div/div/div/div/div/div/div/div/div/div/p[10]/img/@src',
              'melbourne': '/html/body/div/div/div[3]/div/div[2]/div/div/div/div/div/div/div/div/div/div/p[13]/img/@src',
              'brisbane':'/html/body/div/div/div[3]/div/div[2]/div/div/div/div/div/div/div/div/div/div/p[16]/img/@src',
              'adelaide':'/html/body/div/div/div[3]/div/div[2]/div/div/div/div/div/div/div/div/div/div/p[19]/img/@src',
              'perth':'/html/body/div/div/div[3]/div/div[2]/div/div/div/div/div/div/div/div/div/div/p[22]/img/@src'
    }
    
    for city in xpaths:
        img = doc.xpath(xpaths[city])
        img1url = "%s%s" % ( BASEURL, img[0])
        imghttp = urllib2.urlopen(img1url)
        imgdata = imghttp.read()
        imghttp.close()
        imgstorepath = os.path.join(IMGSTORE, '%s.jpg'%city)
        fileimg = open(imgstorepath, "wb")
        fileimg.write(imgdata)
        fileimg.close()


if __name__ == '__main__':
    option = '--minutes'
    if len(sys.argv) > 1:
        if sys.argv[1] == '--hours':
            option = '--hours'
        elif sys.argv[1] == '--days':
            option = '--days'
    
    #db = ServiceDB.instance()
    from index import db
    if option == '--minutes':
        money = getAUDCNY()
        db.saveMoneyMinute(money)
        print "saved minutes!"
    elif option == '--hours':
        money = getAUDCNY()
        db.saveMoneyHour(money)
        print "saved hours!"
    elif option == '--days':
        filepath = os.path.realpath(__file__)
        dirname = os.path.dirname(filepath)
        imgpath = os.path.join(dirname, 'static/public/img/')
        petrolCapture(imgpath)
    db.session.close()
    
   