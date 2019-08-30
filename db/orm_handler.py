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

import datetime
from db.cs_base import CSBase
from dotenv import load_dotenv
import os

Base = declarative_base(cls=CSBase)
db_instance = None

db_session = None

def db_init():
    global db_instance
    load_dotenv()
    persist = True
    if db_instance:
        return db_instance
    db_uri = os.getenv('DB_URI')
    engine = create_engine(db_uri, pool_size=25, max_overflow=10)
    db_session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )
    Base.query = db_session.query_property()
    if not persist:
        Base.metadata.drop_all(engine)
    Base.metadata.create_all(bind=engine)
    # db_instance = db_session
    # return db_instance
