# coding=utf-8
# 数据库连接和MAPPING

import sqlalchemy
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import event, exc, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.pool import QueuePool
from sqlalchemy import distinct
from sqlalchemy import update
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)

pymysql.install_as_MySQLdb()
DBNAME = ''
DBHOST = ''
DBUSER = ''
DBPWD = ''
engine = create_engine('mysql://' + DBUSER + ':' + DBPWD + '@' + DBHOST + '/' + DBNAME + '?charset=utf8', encoding="utf8",
                       poolclass=QueuePool, pool_size=50, pool_recycle=60, echo=False)


@event.listens_for(engine, "engine_connect")
def ping_connection(connection, branch):
    if branch:
        # "branch" refers to a sub-connection of a connection,
        # we don't want to bother pinging on these.
        return

    try:
        # run a SELECT 1. use a core select() so that
        # the SELECT of a scalar value without a table is
        # appropriately formatted for the backend
        connection.scalar(select([1]))
    except exc.DBAPIError as err:
        # catch SQLAlchemy's DBAPIError, which is a wrapper
        # for the DBAPI's exception. It includes a .connection_invalidated
        # attribute which specifies if this connection is a "disconnect"
        # condition, which is based on inspection of the original exception
        # by the dialect in use.
        if err.connection_invalidated:
            # run the same SELECT again - the connection will re-validate
            # itself and establish a new connection. The disconnect detection
            # here also causes the whole connection pool to be invalidated
            # so that all stale connections are discarded.
            connection.scalar(select([1]))
        else:
            raise


# session_factory = sessionmaker(bind=engine)
# Session = scoped_session(session_factory)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Patent(Base):
    __tablename__ = 'patent'
    publicate_number = Column(String, primary_key=True)
    publicate_date = Column(String, nullable=True)
    applicate_number = Column(String)
    applicate_date = Column(String)
    applicate_person = Column(String)
    inventor = Column(String)
    address = Column(String)
    classification = Column(String)
    ipproxy = Column(String)
    proxy_person = Column(String)
    priority = Column(String)
    PCT_in_date = Column(String)
    PCT_applicate = Column(String)
    PCT_publicate = Column(String)

class Page(Base):
    __tablename__ = 'pages'
    strWhere = Column(String, primary_key=True)
    pageSize = Column(String, primary_key=True)
    pageNow = Column(String, primary_key=True)
