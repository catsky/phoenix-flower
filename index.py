from flask import Flask, request, redirect, url_for, session
from flask import render_template
from crontab import CronTab
import time

from database import ServiceDB


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
    print "new query"
    cur2 = db.queryMoneyHours(24)
    db.session.commit()
    return render_template('currency_all.html', currencies_min=cur1, 
                           currencies_hour=cur2,  login=haslogin(), 
                           username=session.get('username',''), view="currency")

@app.route("/vote")
def vote():
    user_id = request.args['uid']
    article_id = request.args['aid']
    data = dict(user_id=int(user_id), article_id=int(article_id), timestamp=time.time())
    db.saveFav(**data)
    return render_template('news.html')

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
    query = db.queryArticlesByHot(count=10, offset=offset)
    return render_template('news.html', articles=query, login=haslogin(), 
                           username=session.get('username',''), view="hot")

@app.route("/latest")
def latest():
    offset = 1
    offset_str = request.args.get('offset', False)
    if offset_str != False:
        offset = int(offset_str)
    query = db.queryArticlesByLatest(count=10, offset=offset)
    return render_template('news.html', articles=query,login=haslogin(), 
                           username=session.get('username',''), view="latest")

@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user = dict()
        user['name'] = request.form.get('name', '')
        user['email'] = request.form.get('email', '')
        user['password'] = request.form.get('password', '')
        db.addUser(**user)
        session['username'] =  user['name']
        return redirect(url_for('hot'))
    return render_template('signup.html')

@app.route("/signout")
def signout():
    session.pop('username', None)
    return redirect(url_for('hot'))
    

if __name__ == "__main__":
    startCron()
    app.run('0.0.0.0')