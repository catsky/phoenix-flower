from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import sessionmaker, relationship, backref

from utils import calculate_score, timeformat
from config import DBCHOICE

import os
import time
#Base class for OMR table
_Base = declarative_base()



class ServiceDB():
    engine = None
    Session = None  # Session maker function stub
    dbconn_str = ""

    def __init__(self, sqlite_path='/home/catsky/Desktop/workspace/phoenix-flower/data/db/'):
        self.session = None
        if ServiceDB.engine is None:
            # Valid SQLite URL forms are:
            # sqlite:///:memory: (or, sqlite://)
            # sqlite:///relative/path/to/file.db
            # sqlite:///C:\\path\\to\\database.db
            if DBCHOICE == "sqlite":
                print "DBCHOICE =sqlite"
                if sqlite_path is not None:
                    if not os.path.exists(sqlite_path):
                        os.makedirs(sqlite_path)
                    ServiceDB.dbconn_str = "sqlite:///%s%s" % (
                                               sqlite_path,
                                               "sqlite.data")
                else:
                    print "Error! need db path to create sqlite schema"
                    raise

                print "db path: " + ServiceDB.dbconn_str

                ServiceDB.engine = create_engine(ServiceDB.dbconn_str)

            elif DBCHOICE == "postgresql":
                print "DBCHOICE =postgresql"
#                 ServiceDB.dbconn_str = "postgresql://%s:%s@localhost:%s/%s" % (
#                                                cfg.getUSERNAME(),
#                                                cfg.getPASSWORD(),
#                                                cfg.getDBPORT(),
#                                                cfg.getDBNAME())
#                 ServiceDB.engine = create_engine(ServiceDB.dbconn_str,
#                                                  pool_size=10,
#                                                  pool_recycle=3600)
            else:
                raise
            ServiceDB.Session = sessionmaker(bind=ServiceDB.engine)
            _Base.metadata.create_all(ServiceDB.engine)
        else:
            pass
        self.session = ServiceDB.Session()
   
    def saveMoneyMinute(self, tuple_in):
        moneyminutes = Money_Minute(name=tuple_in[0], timestamp=tuple_in[1], value=tuple_in[2])
        self.session.add(moneyminutes)
        self.session.commit()
        self.session.close() 
    
    def queryMoneyMinutes(self, count=None):
        #return latest cur of last 30 minutes
        query = self.session.query(Money_Minute).order_by(Money_Minute.id.desc()).all()
        for index, row in enumerate(query):
            row.timeshow = timeformat(row.timestamp)
            if index % 3 == 0:
                row.annotation = str(row.value)
            else:
                row.annotation = ''
        if count != None:
            query = query[:count]
        query.reverse()
        return query
    
    def saveMoneyHour(self, tuple_in):
        moneyhours = Money_Hour(name=tuple_in[0], timestamp=tuple_in[1], value=tuple_in[2])
        self.session.add(moneyhours)
        self.session.commit()
        
    def queryMoneyHours(self, count=None):
        query = self.session.query(Money_Hour).order_by(Money_Hour.id.desc()).all()
        for index, row in enumerate(query):
            row.timeshow = timeformat(row.timestamp)
            if index % 3 == 0:
                row.annotation = str(row.value)
            else:
                row.annotation = ''
        if count != None:
            query = query[:count]
        query.reverse()
        return query
    
    def queryArticlesByHot(self, count=32, offset=0):
        query = self.session.query(Article).all()
        now = time.time()
        for row in query:
            if self.isFaved(article_id=row.id, user_id=row.user_id):
                row.faved = True
            else:
                row.faved = False
            delta_hours = int((now-row.timestamp)/3600)
            hot = calculate_score(row.score, delta_hours)
            row.hot = hot
        query = sorted(query, reverse=True)       
        
        for index, row in enumerate(query):
            row.rowid = index + 1
        if len(query) > offset:
            query = query[offset-1:(count+offset+1)]
        else:
            query = query[:count]
        return query
    
    def queryArticlesByLatest(self, count=32, offset=0):
        query = self.session.query(Article).order_by(Article.timestamp.desc()).all()
        for row in query:
            if self.isFaved(article_id=row.id, user_id=row.user_id):
                row.faved = True
            else:
                row.faved = False
        
        for index, row in enumerate(query):
            row.rowid = index + 1
        if len(query) > offset:
            query = query[offset-1:(count+offset+1)]
        else:
            query = query[:count]
        return query
    
    def isFaved(self, article_id, user_id):
        exist = self.session.query(Favorite).filter_by(user_id=user_id, article_id=article_id).count()
        if exist > 0:
            return True
        else:
            return False
        
        
    def saveFav(self, **data):
        timestamp = time.time()
        article_id = data['article_id']
        user_id = data['user_id']
        fav = Favorite(timestamp = timestamp, article_id = article_id, user_id = user_id)
        self.session.add(fav)        
        self.session.flush()
        fav.article.score += 1
        self.session.commit()   


class Money_Minute(_Base):
    __tablename__ = 'money_minutes'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    timestamp = Column(Float, nullable=False)
    value = Column(Float, nullable=False)
        
    def __repr__(self):
        print "<Money_Minute (%s, %s, %s)>" % (self.id, self.timestamp, self.value)
        
class Money_Hour(_Base):
    __tablename__ = 'money_hours'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    timestamp = Column(Float, nullable=False)
    value = Column(Float, nullable=False)

    def __repr__(self):
        print "<Money_Hour (%s, %s, %s)>" % (self.id, self.timestamp, self.value)

class User(_Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
       
    def __repr__(self):
        print "<User (%s, %s, %s)>" % (self.name, self.email, self.password)
    
        
class Article(_Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    URL = Column(String, nullable=False, unique=True)
    score = Column(Integer, default=0)
    hot = Column(Float, default=0.0)
    timestamp = Column(Float, nullable=False)
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", backref=backref('articles', order_by=id))
    
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    category = relationship("Category", backref=backref('articles', order_by=id))
    
    def __cmp__(self, other):
        if self.hot > other.hot:
            return 1
        else:
            return -1
   
    def __repr__(self):
        print "<Article (%s)>" % (self.title)
        
class Category(_Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
        
    def __repr__(self):
        print "<Category (%s)>" % (self.name)
        
        
class Favorite(_Base):
    __tablename__ = 'favorites'
    id = Column(Integer, primary_key=True)
    timestamp = Column(Float, nullable=False)
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", backref=backref('favorites', order_by=id))
    
    article_id = Column(Integer, ForeignKey('articles.id'), nullable=False)
    article = relationship("Article", backref=backref('favorites', order_by=id))
    
    def __repr__(self):
        print "<Favorite (%s, %s)>" % (self.user.name, self.article.title)
     
if __name__ == '__main__':
    db = ServiceDB()
    import time
#     query = db.queryArticles(30)
#     for row in query:
#         print row.title
#         print type(row.user)
#         if row.user is not None:
#             print row.user
    import random
    rstr = str(random.randint(0,100000))
    
    ken = User(name='ken'+rstr,email='zhdhui@g.com'+rstr,  password='gjffdd')
    cat = Category(name='life'+rstr)
    db.session.add(ken)
    db.session.add(cat)
    db.session.flush()
    art = Article(title="title", URL="http://www.baidu.com/q="+rstr, 
                  user_id=ken.id, category_id=cat.id,
                  timestamp=time.time())
    db.session.add(art)
    db.session.flush()
    #fav = Favorite(timestamp=time.time(), user_id=ken.id, article_id=art.id)
    data = dict(timestamp=time.time(), user_id=ken.id, article_id=art.id)
    db.saveFav(**data)
    db.session.close()
    import sys
    sys.exit()
#     for row in db.queryMoneyMinutes():
#         print "%s %s %s %s %s" % (row.name, row.timestamp, row.value, row.timeshow, row.annotation)
#     for row in db.queryMoneyHours():
#         print "%s %s %s %s %s" % (row.name, row.timestamp, row.value, row.timeshow, row.annotation)
