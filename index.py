from flask import Flask, request
from flask import render_template
from crontab import CronTab
import time

from database import ServiceDB


app = Flask(__name__)
app.debug = True
db = ServiceDB()

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



@app.route("/cur/<string:freq>")
def currrency(freq):
    if freq == None or freq == "minutes":
        cur = db.queryMoneyMinutes(30)
        return render_template('currency_minutes.html', currencies=cur)
    elif freq == "hours":
        cur = db.queryMoneyHours(24)
        return render_template('currency_hours.html', currencies=cur)
    else:
        cur1 = db.queryMoneyMinutes(30)
        cur2 = db.queryMoneyHours(24)
        return render_template('currency_all.html', currencies_min=cur1, currencies_hour=cur2)

@app.route("/vote")
def vote():
    user_id = request.args['uid']
    article_id = request.args['aid']
    data = dict(user_id=int(user_id), article_id=int(article_id), timestamp=time.time())
    db.saveFav(**data)
    return render_template('news.html')

@app.route("/hot")
def hot():
    offset_str = request.args.get('offset', False)
    if offset_str != False:
        offset = int(offset_str)
    else:
        offset = 1
    query = db.queryArticlesByHot(count=10, offset=offset)
    return render_template('news.html', articles=query, view="hot")

@app.route("/latest")
def latest():
    offset = 1
    offset_str = request.args.get('offset', False)
    if offset_str != False:
        offset = int(offset_str)
    query = db.queryArticlesByLatest(count=10, offset=offset)
    return render_template('news.html', articles=query, view="latest")

    
if __name__ == "__main__":
    startCron()
    app.run()