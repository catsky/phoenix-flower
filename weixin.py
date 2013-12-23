#!/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Ken Zheng'

import hashlib
import time
import xml.etree.ElementTree as ET
#from PIL import Image

import urllib2


#generate the thumbnail for an image
def generateThumbnail():
    pass
#     import os
#     file = os.path.abspath(__file__)
#     img = os.path.join(file, '../static/public/img/currency.jpg')
#     im = Image.open(img)
#     #im = Image.open(bucket.get_object_contents(file_name))
#     im.thumbnail((320,200))
#     nailfile = 
#     im.save(file + ".thumbnail", "JPEG")
#all message rec and push need verification
def verification(request):
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')

    token = 'australian1984'  # keep it as the same as it on wechat mp
    tmplist = [token, timestamp, nonce]
    tmplist.sort()
    tmpstr = ''.join(tmplist)
    hashstr = hashlib.sha1(tmpstr).hexdigest()

    if hashstr == signature:
        return True
    return False


#transfer the msg to dict
def parse_msg(rawmsgstr):
    root = ET.fromstring(rawmsgstr)
    msg = {}
    for child in root:
        msg[child.tag] = child.text
    return msg


def is_text_msg(msg):
    return msg['MsgType'] == 'text'


def is_location_msg(msg):
    return msg['MsgType'] == 'location'


def user_subscribe_event(msg):
    return msg['MsgType'] == 'event' and msg['Event'] == 'subscribe'

HELP_INFO = \
u"""
欢迎关注澳洲一刻^_^

我们为您奉上最新鲜的澳洲生活资讯，最前沿的移民信息。
❤回复'm'或者'money' 获取最新澳币汇率 (新版)
❤澳洲一刻社区42bang.com已准备就绪,欢迎访问!
"""


def help_info(msg):
    return response_text_msg(msg, HELP_INFO)


def getAUDCNY():
    API = "http://download.finance.yahoo.com/d/quotes.csv?e=.csv&f=sl1d1t1&s=AUDCNY=x"
    try:
        response = urllib2.urlopen(API)
        content = response.read()
        content = content.split(',')
    except:
        print "Error:getAUDCNY()"
        return None
    return content


def currency_info_AUDCNY(msg):
    cur = getAUDCNY()
    if cur != None:
        return response_text_msg(msg,
                                 u"""Hi, 澳洲一刻的小伙伴：
当前 1 澳币可以兑换  %s 人民币""" % cur[1])
    else:
        return response_text_msg(msg, HELP_INFO)
    

def currency_info_AUDCNY_Pic(msg):
    cur = getAUDCNY()
    if cur != None:
        class Cur(object):
            pass
        cur_obj = Cur()
        cur_obj.title = u"当前 1 澳币可兑换  %s 人民币" % cur[1]
        cur_obj.shorten_content = u"""点击查看最近半小时和24小时汇率趋势图^_^. 
也可以直接登录澳洲一刻小伙伴们的社区
[ http://42bang.com ] 随时查看汇率哦！
社区里还有很多关于澳洲的精彩文章，都很值得收藏！欢迎小伙伴们投稿:)"""

        cur_obj.imgthumbnail = "http://42bang.com/static/public/img/cur1.thumbnail.jpg"
        cur_obj.url = 'http://42bang.com/cur/all'
        curs = list()
        curs.append(cur_obj)
        return response_news_msg(msg, curs)
    else:
        return response_text_msg(msg, HELP_INFO)
    
    

def petrol(msg):
    class Petrol(object):
        pass
    p_obj = Petrol()
    p_obj.title = u"最新的澳洲油价变化周期"
    p_obj.shorten_content = u"""点击查看最近油价的最低点和各大城市的最新油价周期情况。^_^. 
也可以直接登录澳洲一刻小伙伴们的社区
[ http://42bang.com ] 随时查看哦！
社区里还有很多关于澳洲的精彩文章，都很值得收藏！欢迎小伙伴们投稿:)"""

    p_obj.imgthumbnail = "http://42bang.com/static/public/img/cur1.thumbnail.jpg"
    p_obj.url = 'http://42bang.com/petrol'
    pets = list()
    pets.append(p_obj)
    return response_news_msg(msg, pets)

    
    
NEWS_MSG_HEADER_TPL = \
u"""
<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[news]]></MsgType>
<ArticleCount>%d</ArticleCount>
<Articles>
"""
#<Content><![CDATA[]]></Content>

NEWS_MSG_TAIL = \
u"""
</Articles>
</xml>
"""
#<FuncFlag>1</FuncFlag>


#msg reply, news with pictures
def response_news_msg(recvmsg, posts):
    msgHeader = NEWS_MSG_HEADER_TPL % (recvmsg['FromUserName'], recvmsg['ToUserName'],
        str(int(time.time())), len(posts))
    msg = ''
    msg += msgHeader
    msg += make_articles(posts)
    msg += NEWS_MSG_TAIL
    return msg


def make_articles(posts):
    msg = ''
    if len(posts) == 1:
        msg += make_single_item(posts[0])

    return msg

NEWS_MSG_ITEM_TPL = \
u"""
<item>
    <Title><![CDATA[%s]]></Title>
    <Description><![CDATA[%s]]></Description>
    <PicUrl><![CDATA[%s]]></PicUrl>
    <Url><![CDATA[%s]]></Url>
</item>
 """


#if msg with pic only has one, show more desc
def make_single_item(message):
    #filter the sensitive words
    title_r = message.title
    description_r = message.shorten_content
    title = u'%s' % title_r
    description = '%s' % description_r
    picUrl = message.imgthumbnail
    
    item = NEWS_MSG_ITEM_TPL % (title, description, picUrl, message.url)
    #item = NEWS_MSG_ITEM_TPL
    return item

TEXT_MSG_TPL = \
u"""
<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[%s]]></Content>
<FuncFlag>0</FuncFlag>
</xml>
"""


def response_text_msg(msg, content):
    s = TEXT_MSG_TPL % (msg['FromUserName'], msg['ToUserName'],
        str(int(time.time())), content)
    return s
