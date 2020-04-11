#!/usr/bin/env python
# -*- coding: utf-8 -*


import logging
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.dialects import mysql
from sqlalchemy.schema import Column
from sqlalchemy.sql import text
from sqlalchemy.types import TIMESTAMP

from flood.models import db_session, Base, get_id, to_dict
from flood.models.group import Group

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)

dateformat = '%Y-%m-%dT%H:%M:%S'

class User(Base):
    __tablename__ = 'users'

    id = Column(
        mysql.VARCHAR(length=64), default=get_id, primary_key=True
    )
    name = Column(
        mysql.VARCHAR(length=128), nullable=False
    )
    email = Column(
        mysql.VARCHAR(length=128), nullable=False
    )
    pswd = Column(
        mysql.VARCHAR(length=128), nullable=False
    )
    created_at = Column(
        TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=False, index=True
    )

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name})>"

    def to_dict(self):
        result = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": None
        }
        if self.created_at is not None:
            result['created_at'] = self.created_at.isoformat()

        return result


def buid_object_from_row(row):
    user = User(
        name=row.get("name", None),
        id=row.get("id", None),
        email=row.get("email", None),
        pswd=row.get("pswd", None),
    )
    if "created_at" in row.keys():
        user.created_at = datetime.strptime(row["created_at"], dateformat)

    return user


@db_session
def create(session, user):
    _logger.info(
        "CREATING_USER_MODEL: {}".format(user),
    )
    result = User(
        name=user.get("name"),
        email=user.get("email"),
        pswd=user.get("pswd")
    )
    session.add(result)

    session.flush()
    r = to_dict(result)
    session.commit()
    return buid_object_from_row(r)


@db_session
def list(session):
    _logger.info(
        "LISNTING_USER_MODEL",
    )

    data = []

    result = session.query(User).all()

    if result is None:
        return data
    else:
        for row in result:
            r = to_dict(row)
            data.append(buid_object_from_row(r))
        return data


@db_session
def get(session, id):
    _logger.info(
        "GETTING_USER_MODEL: {}".format(id),
    )
    result = session.query(User).get(id)
    if result is None:
        return None
    else:
        r = to_dict(result)
        return buid_object_from_row(r)

@db_session
def get_by_email(session, email):
    _logger.info(
        "GETTING_USER_MODELBY_EMAIL: {}".format(id),
    )
    result = session.query(User).filter(User.email == email).first()
    if result is None:
        return None
    else:
        r = to_dict(result)
        return buid_object_from_row(r)


@db_session
def delete(session, user):
    _logger.info(
        "DELETING_USER_MODEL: {}".format(user.to_dict()),
    )
    x = session.query(Group).get(user.id)
    session.delete(x)
    session.commit()
