from utils import timeformat

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, Float, String
from sqlalchemy.orm import sessionmaker, relationship, backref

from config import DBCHOICE
import os
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
   
    def saveMoneyMinutes(self, tuple_in):
        moneyminutes = Money_Minute(name=tuple_in[0], timestamp=tuple_in[1], value=tuple_in[2])
        self.session.add(moneyminutes)
        self.session.commit()
    
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
    
    def saveMoneyHours(self, tuple_in):
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
    
    def queryArticles(self, count=None):
        query = self.session.query(Article).order_by(Article.id.desc()).all()
        if count != None:
            query = query[:count]
        return query

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
    score = Column(Integer)
    hot = Column(Float)
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", backref=backref('articles', order_by=id))
    
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    category = relationship("Category", backref=backref('articles', order_by=id))
    
   
    def __repr__(self):
        print "<Article (%s)>" % (self.title)
        
class Category(_Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        print "<Category (%s)>" % (self.name)
        
if __name__ == '__main__':
    db = ServiceDB()
#     query = db.queryArticles(30)
#     for row in query:
#         print row.title
#         print type(row.user)
#         if row.user is not None:
#             print row.user
    ken = User(name='ken',email='zhdhui@g.com',  password='gjffdd')
    cat = Category(name='life')
    db.session.add(ken)
    db.session.add(cat)
    db.session.flush()
    art = Article(title="title", URL="link", user_id=ken.id, category_id=cat.id)
    db.session.add(art)
    db.session.commit()

    
#     for row in db.queryMoneyMinutes():
#         print "%s %s %s %s %s" % (row.name, row.timestamp, row.value, row.timeshow, row.annotation)
#     for row in db.queryMoneyHours():
#         print "%s %s %s %s %s" % (row.name, row.timestamp, row.value, row.timeshow, row.annotation)
