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

def db_session():
    global db_instance
    load_dotenv()
    persist = False
    if db_instance:
        return db_instance
    print(os.getenv('DB_URI'))
    db_uri = 'postgresql://pybossa:tester@dbdev:5432/cs?sslmode=disable'
    engine = create_engine(db_uri, convert_unicode=True)
    db_session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )
    Base.query = db_session.query_property()
    if not persist:
        Base.metadata.drop_all(engine)
    Base.metadata.create_all(bind=engine)
    db_instance = db_session
    return db_instance
