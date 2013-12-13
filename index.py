# -*- coding: utf-8 -*-

from flask import Flask, request, redirect, url_for, session, flash
from flask import render_template
from crontab import CronTab
import time
from datetime import datetime
import json
import logging
from config import PAGESIZE

from database import ServiceDB
import weixin

app = Flask(__name__)
app.debug = True
app.secret_key = 'iyxi33yk1m12jl4lmyzh2w0zljl0yk2wl3w52l2x'
db = ServiceDB.instance()

def startCron():
    cron = CronTab('catsky')
    cron.remove_all('/usr/bin/python')
    job1 = cron.new(command='/usr/bin/python /home/catsky/Desktop/workspace/phoenix-flower/cron.py')
    job1.every().minute()
    job2 = cron.new(command='/usr/bin/python /home/catsky/Desktop/workspace/phoenix-flower/cron.py --hours')
    job2.every().hour()
    cron.write()
    print 'cron job started as the following'
    print cron.render()



@app.route("/cur/all", methods = ['GET', 'POST'])
def currrency():
    cur1 = db.queryMoneyMinutes(30)
    cur2 = db.queryMoneyHours(24)
    return render_template('currency_all.html', currencies_min=cur1, 
                           currencies_hour=cur2,  login=haslogin(), 
                           username=session.get('username',''), view="currency")

@app.route("/vote")
def vote():
    user_id = request.args.get('uid', '')
    
    if user_id == '':
        return redirect('/signin')
    
    article_id = request.args.get('aid', '') 
    data = dict(user_id=int(user_id), article_id=int(article_id), timestamp=time.time())
    db.saveFav(**data)

def haslogin():
    if session.get('username', False):
        return True
    else:
        return False
@app.route('/')
def index():
    return redirect(url_for('hot'))

@app.route("/hot")
def hot():
    offset_str = request.args.get('offset', False)
    if offset_str != False:
        offset = int(offset_str)
    else:
        offset = 1
    query = db.queryArticlesByHot(count=PAGESIZE, offset=offset, user_id=session.get('user_id',None))
    return render_template('news.html', articles=query, login=haslogin(), 
                           username=session.get('username',''), 
                           user_id=session.get('user_id', ''),
                           view="hot")

@app.route("/latest")
def latest():
    offset = 1
    offset_str = request.args.get('offset', False)
    if offset_str != False:
        offset = int(offset_str)
    query = db.queryArticlesByLatest(count = PAGESIZE, offset = offset, user_id=session.get('user_id',None))
    return render_template('news.html', articles = query,login=haslogin(), 
                           username = session.get('username',''), 
                           user_id=session.get('user_id', ''),
                           view = "latest")

@app.route("/signin", methods = ['GET', 'POST'])
def signin():
    if request.method == 'POST':
        user = dict() 
        user['email'] = request.form.get('email', '')
        user['password'] = request.form.get('password', '')

        islogined, q_user=  db.userLogin(**user)
        if islogined:
            session['username'] = q_user.name
            session['user_id'] = q_user.id
            return redirect(url_for('hot'))
        else:
            return render_template('signin.html', msg = "用户名或者密码不正确！")
    else:
        return render_template('signin.html')
    
    
    
@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user = dict()
        user['name'] = request.form.get('name', '')
        user['email'] = request.form.get('email', '')
        user['password'] = request.form.get('password', '')
        userid = db.addUser(**user)
        session['username'] =  user['name']
        session['user_id'] = userid
        return redirect(url_for('hot'))
    return render_template('signup.html')

@app.route("/emailcheck")
def emailcheck(): 
    email = request.args.get('email', False)
    exist = db.emailcheck(email)
    return json.dumps(exist)  

@app.route("/usercheck")
def usercheck(): 
    name = request.args.get('name', False)
    exist = db.usercheck(name)
    return json.dumps(exist)  

@app.route("/catcheck")
def catcheck(): 
    name = request.args.get('catname', False)
    exist = db.catcheck(name)
    return json.dumps(exist)  

@app.route("/signout")
def signout():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('hot'))
    
@app.route("/submit", methods = ['GET', 'POST'])
def submit():
    cat = db.queryCategory()
    if request.method == 'POST':
        art = dict()
        art['category_id'] = request.form.get('cat_id', '')
        art['title'] = request.form.get('title', '')
        art['URL'] = request.form.get('URL', '')
        art['username'] = session.get('username','')
        art['timestamp'] = time.time()
        db.saveArticle(**art)
        return redirect(url_for('latest'))
    else:
        return render_template('submit.html', categories=cat, login=haslogin(), 
                           username=session.get('username',''))

@app.route("/user/<string:username>")
def user_faved(username):
    query = db.queryFavedArticles(username)
    return render_template("user.html", favs = query, login=haslogin(), 
                           username=session.get('username',''))

@app.route("/category/<string:catname>")
def category(catname):
    offset_str = request.args.get('offset', False)
    if offset_str != False:
        offset = int(offset_str)
    else:
        offset = 1
    query = db.queryArticlesByCategory(catname, count=PAGESIZE, offset=offset, user_id=session.get('user_id',None))
    return render_template('category.html', articles=query, login=haslogin(), 
                           username=session.get('username',''), 
                           user_id=session.get('user_id', ''),
                           catename = catname
                           )
    

@app.route("/admin", methods = ['GET', 'POST'])   
def admin():
    if request.method == 'GET':
        if haslogin():
            username = session.get('username', '')
            if db.isadmin(username):
                query = db.queryCategory()
                return render_template('admin.html', categories = query, login=haslogin(), 
                           username=session.get('username',''))
        return redirect(url_for('hot'))
    elif request.method == 'POST':
        if haslogin():
            username = session.get('username', '')
            if db.isadmin(username):
                catname = request.form.get('catname', '') 
                db.addCategory(catname)
                query = db.queryCategory()
                return render_template('admin.html', categories = query, login=haslogin(), 
                           username=session.get('username',''))
        return redirect(url_for('hot'))

#wechat verify
@app.route('/weixin', methods=['GET'])
def weixin_access_verify():
    echostr = request.args.get('echostr')
    if weixin.verification(request) and echostr is not None:
        return echostr
    return 'access verification fail'

#yixin verify
@app.route('/yixin', methods=['GET'])
def yixin_access_verify():
    echostr = request.args.get('echostr')
    if weixin.verification(request) and echostr is not None:
        return echostr
    return 'access verification fail'

#msg from weixin 
@app.route('/weixin', methods=['POST'])
def weixin_msg():
    logging.error("1.weixin: in weixin_msg ")
    if weixin.verification(request):
        logging.error("2.weixin verify done")
        data = request.data
        msg = weixin.parse_msg(data)
        if weixin.user_subscribe_event(msg):
            return weixin.help_info(msg)
        elif weixin.is_text_msg(msg):
            content = msg['Content']
            if content == u'?' or content == u'？':
                return weixin.help_info(msg)
            elif (content == u'n' or content == u'N' 
                 or content == u'new' or content == u'NEW'
                 or content == u'New'):
                posts = operatorDB.get_weixin_articles()
                rmsg = weixin.response_news_msg(msg, posts)
                logging.error("3.weixin get rmsg: %s"%rmsg)
                return rmsg
            elif (content == u'm' or content == u'M' 
                 or content == u'money' or content == u'MONEY'
                 or content == u'Money'):
                return weixin.currency_info_AUDCNY(msg)
#             else:
#                 return weixin.help_info(msg)
        elif weixin.is_location_msg(msg):
            Label = msg['Label'] 
            return weixin.help_info(msg)
    return 'message processing fail'

#msg from yixin server
@app.route('/yixin', methods=['POST'])
def yixin_msg():
    logging.error("1.weixin: in weixin_msg ")
    if weixin.verification(request):
        logging.error("2.weixin verify done")
        data = request.data
        msg = weixin.parse_msg(data)
        if weixin.user_subscribe_event(msg):
            return weixin.help_info(msg)
        elif weixin.is_text_msg(msg):
            content = msg['Content']
            if content == u'?' or content == u'？':
                return weixin.help_info(msg)
            elif (content == u'n' or content == u'N' 
                 or content == u'new' or content == u'NEW'
                 or content == u'New'):
                posts = operatorDB.get_weixin_articles()
                rmsg = weixin.response_news_msg(msg, posts)
                logging.error("3.weixin get rmsg: %s"%rmsg)
                return rmsg
            elif (content == u'm' or content == u'M' 
                 or content == u'money' or content == u'MONEY'
                 or content == u'Money'):
                return weixin.currency_info_AUDCNY(msg)
#             else:
#                 return weixin.help_info(msg)
        elif weixin.is_location_msg(msg):
            Label = msg['Label'] 
            return weixin.help_info(msg)
    return 'message processing fail'

            
@app.template_filter()
def timesince(timestamp, default=u"刚才"):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    """
    dt = datetime.fromtimestamp(timestamp)
    now = datetime.now()
    diff = now - dt
    
    periods = (
        (diff.days / 365, u"年"),
        (diff.days / 30, u"月"),
        (diff.days / 7, u"星期"),
        (diff.days, u"天"),
        (diff.seconds / 3600, u"小时"),
        (diff.seconds / 60, u"分钟"),
        (diff.seconds, u"秒钟"),
    )

    for period, singular in periods:
        if period:
            return u"%d %s之前" % (period, singular)

    return default

if __name__ == "__main__":
    startCron()
    app.run('0.0.0.0')