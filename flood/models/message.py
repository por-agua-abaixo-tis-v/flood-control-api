#!/usr/bin/env python
# -*- coding: utf-8 -*

from datetime import datetime

from sqlalchemy import between, func, ForeignKey
from sqlalchemy.schema import Column
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.dialects import mysql
from sqlalchemy.sql import text
from sqlalchemy import and_
from flood.models.group import Group
from flood.models import db_session, Base, get_id, to_dict

import logging
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)

dateformat = '%Y-%m-%dT%H:%M:%S'

class Message(Base):
    __tablename__ = 'messages'

    id = Column(
        mysql.VARCHAR(length=64), default=get_id, primary_key=True
    )
    group_id = Column(
        mysql.VARCHAR(length=64), ForeignKey(Group.id), nullable=False, index=True
    )
    user = Column(
        mysql.VARCHAR(length=64), nullable=False
    )
    created_at = Column(
        TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=False, index=True
    )
    text = Column(
        mysql.VARCHAR(length=512), nullable=False
    )

    def __repr__(self):
        return f"<Message(id={self.id}, user={self.user}, group )>"

    def to_dict(self):
        result = {
            "id": self.id,
            "group_id": self.group_id,
            "user": self.user,
            "text": self.text,
            "created_at": None
        }
        if self.created_at is not None:
            result['created_at'] = self.created_at.isoformat()

        return result

def buid_object_from_row(row):
    message = Message(
        id=row.get("id", None),
        group_id=row.get("group_id", None),
        user=row.get("user", None),
        text=row.get("text", None),

    )
    if "created_at" in row.keys():
        message.created_at = datetime.strptime(row["created_at"], dateformat)

    return message

@db_session
def create(session, message):
    _logger.info(
        "CREATING_MESSAGE_MODEL: {}".format(message),
    )
    result = Message(
        group_id=message.get("group_id", None),
        user=message.get("user", None),
        text=message.get("text", None),
    )
    session.add(result)
    session.flush()
    r = to_dict(result)
    return buid_object_from_row(r)

@db_session
def list(session):
    _logger.info(
        "LISNTING_MESSAGE_MODEL",
    )

    data = []

    result = session.query(Message).all()

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
        "GETTING_MESSAGE_MODEL: {}".format(id),
    )
    result = session.query(Message).get(id)
    if result is None:
        return None
    else:
        r = to_dict(result)
        return buid_object_from_row(r)


@db_session
def delete(session, group):
    _logger.info(
        "DELETING_MESSAGE_MODEL: {}".format(group.to_dict()),
    )
    x = session.query(Group).get(group.id)
    session.delete(x)