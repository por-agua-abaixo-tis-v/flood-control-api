#!/usr/bin/env python
# -*- coding: utf-8 -*


import uuid
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import MetaData
from datetime import datetime

import warnings

import logging
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)


Base = declarative_base()
_session = None
_engine = None
_config = None


db_user = os.environ.get("DB_USER", "").replace("\n", "")
password = os.environ.get("DB_PASS", "").replace("\n", "")
host = os.environ.get("DB_IP", "").replace("\n", "")
database = os.environ.get("DB", "").replace("\n", "")


def _get_session_class():
    global _engine
    _engine = create_engine(
        'mysql+pymysql://{db_user}:{password}@{host_ip}:{port}/{database}'.format(
            db_user=db_user.strip('\n').strip(' '),
            password=password.strip('\n').strip(' '),
            host_ip=host,
            port=3306,
            database=database
        )
    )
    return sessionmaker(bind=_engine)


class ExpectedError(RuntimeError):
    pass


def db_session(f):
    """Decorator for functions that use the database."""
    def wrapper(*arg, **kwargs):
        session = _session()
        try:
            res = f(session, *arg, **kwargs)
            res = res
            with warnings.catch_warnings():
                session.commit()
            return res
        except ExpectedError as e:
            _logger.exception("EXPECTED_DATABASE_ERROR {}".format(str(e)))
            session.rollback()
            raise e
        except Exception as e:
            _logger.exception("UNEXPECTED_DATABASE_ERROR")
            session.rollback()
        finally:
            session.close()
    return wrapper


def to_dict(row):
    """Translates an SQLAlchemy row into a dictionary"""
    if row is None:
        return None
    data = row.__dict__.copy()
    if '_sa_instance_state' in data:
        data.pop('_sa_instance_state')
    for key in data:
        if type(data[key]) == datetime:
            data[key] = data[key].isoformat()
    return data


def from_tuple_to_dict(row):
    data = row._asdict()
    for key in data:
        if type(data[key]) == datetime:
            data[key] = data[key].isoformat()
    return data


def create_tables():
    global _engine
    Base.metadata.drop_all(_engine)
    Base.metadata.create_all(_engine)


def config():
    """
    Configure module
    """
    global _session
    _session = _get_session_class()

    global user
    if user is None:
        user = os.environ.get("DB_USER", None)
    global password
    if password is None:
        password = os.environ.get("DB_PASS", None)
    global host
    if host is None:
        host = os.environ.get("DB_IP", None)
    global database
    if database is None:
        database = os.environ.get("DB", None)


def get_id():
    return str(uuid.uuid4())


def is_database_ok():
    try:
        meta = MetaData()
        meta.reflect(bind=_engine)
        tables = meta.tables
        if tables.__len__() >= 0:
            return True
    except:
        _logger.exception('DATABASE_READY_CHECK')

    return False
