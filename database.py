from utils import timeformat

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, Float, String
from sqlalchemy.orm import sessionmaker

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
        moneyminutes = Money_Minutes(tuple_in[0], tuple_in[1], tuple_in[2])
        self.session.add(moneyminutes)
        self.session.commit()
    
    def queryMoneyMinutes(self, count=None):
        #return latest cur of last 30 minutes
        query = self.session.query(Money_Minutes).order_by(Money_Minutes.id.desc()).all()
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
        moneyhours = Money_Hours(tuple_in[0], tuple_in[1], tuple_in[2])
        self.session.add(moneyhours)
        self.session.commit()
        
    def queryMoneyHours(self, count=None):
        query = self.session.query(Money_Hours).order_by(Money_Hours.id.desc()).all()
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

class Money_Minutes(_Base):
    __tablename__ = 'money_minutes'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    timestamp = Column(Float)
    value = Column(Float)
    
    def __init__(self, name, timestamp, value):
        self.name = name
        self.timestamp = timestamp
        self.value = value
        
    def __repr__(self):
        print "<Money_Minutes (%s, %s, %s)>" % (self.id, self.timestamp, self.value)
        
class Money_Hours(_Base):
    __tablename__ = 'money_hours'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    timestamp = Column(Float)
    value = Column(Float)

    def __init__(self, name, timestamp, value):
        self.name = name
        self.timestamp = timestamp
        self.value = value

    def __repr__(self):
        print "<Money_Hours (%s, %s, %s)>" % (self.id, self.timestamp, self.value)

if __name__ == '__main__':
    db = ServiceDB()
    for row in db.queryMoneyMinutes():
        print "%s %s %s %s %s" % (row.name, row.timestamp, row.value, row.timeshow, row.annotation)
    for row in db.queryMoneyHours():
        print "%s %s %s %s %s" % (row.name, row.timestamp, row.value, row.timeshow, row.annotation)
