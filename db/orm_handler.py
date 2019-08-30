from sqlalchemy import (
    Column,
    DateTime,
    String,
    Integer,
    create_engine,
    JSON,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import Flask, current_app

from flask_sqlalchemy_session import flask_scoped_session

import datetime
from db.cs_base import CSBase
from dotenv import load_dotenv
import os

Base = declarative_base(cls=CSBase)
db_instance = None

def db_session():
    global db_instance
    load_dotenv()
    persist = True
    if db_instance:
        return db_instance
    db_uri = os.getenv('DB_URI')
    engine = create_engine(db_uri, pool_size=25, max_overflow=10)
    # db_session = scoped_session(
    #     sessionmaker(autocommit=False, autoflush=False, bind=engine)
    # )
    
    session_factory = sessionmaker(bind=engine)
    session = flask_scoped_session(session_factory, current_app)
    Base.query = session_factory.query_property()
    if not persist:
        Base.metadata.drop_all(engine)
    Base.metadata.create_all(bind=engine)
    db_instance = session_factory
    return db_instance
