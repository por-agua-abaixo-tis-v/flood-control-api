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
from flood.models.user import User

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)

dateformat = '%Y-%m-%dT%H:%M:%S'


class Message(Base):
    __tablename__ = 'messages'

    id = Column(
        mysql.VARCHAR(length=64), default=get_id, primary_key=True
    )
    group_id = Column(
        mysql.VARCHAR(length=64), ForeignKey(Group.id, ondelete='CASCADE'), nullable=False, index=True
    )
    user_id = Column(
        mysql.VARCHAR(length=64), ForeignKey(User.id, ondelete='CASCADE'), nullable=False, index=True
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
            "user_id": self.user_id,
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
        user_id=row.get("user_id", None),
        text=row.get("text", None),

    )
    if "created_at" in row.keys():
        message.created_at = datetime.strptime(row["created_at"], dateformat)

    return message


@db_session
def create(session, text, user, group):
    _logger.info(
        "CREATING_MESSAGE_MODEL:  {}".format({'text': text, 'user': user, 'group': group.id}),
    )
    result = Message(
        group_id=group.id,
        user=user.name,
        user_id=user.id,
        text=text,
    )
    session.add(result)
    session.flush()
    r = to_dict(result)
    session.commit()
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
def list_group(session, group):
    _logger.info(
        "LISNTING_MESSAGE_MODEL",
    )
    data = []
    result = session.query(Message).filter(Message.group_id == group.id).order_by(Message.created_at)
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
def delete(session, message):
    _logger.info(
        "DELETING_MESSAGE_MODEL: {}".format(message.to_dict()),
    )
    x = session.query(Message).get(message.id)
    session.delete(x)
    session.commit()

@db_session
def get_user_messages(session, user, start_date):
    _logger.info(
        f"LISNTING_USER_MESSAGES: {user.id}",
    )
    data = []
    if start_date:
        result = session.query(Message).filter(Message.user_id == user.id).filter(Message.created_at > start_date).all()
    else:
        result = session.query(Message).filter(Message.user_id == user.id).all()

    if result is None:
        return data
    else:
        for row in result:
            r = to_dict(row)
            data.append(buid_object_from_row(r))
        return data
