from sqlalchemy import Column, DateTime, String, Integer, create_engine, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import Flask, current_app
import config
import datetime
from db.cs_base import CSBase


Base = declarative_base(cls=CSBase)
db_session = None

def init_db(uri=None, persist=True):
    global db_session
    engine = create_engine(uri, convert_unicode=True)
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    Base.query = db_session.query_property()
    if not persist:
        Base.metadata.drop_all(engine) 
    Base.metadata.create_all(bind=engine)
    return db_session
