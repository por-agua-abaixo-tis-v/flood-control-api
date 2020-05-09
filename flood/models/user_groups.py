#!/usr/bin/env python
# -*- coding: utf-8 -*


import logging
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import Column
from sqlalchemy.sql import text
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.exc import IntegrityError

from flood.models import db_session, Base, get_id, to_dict
from flood.models.group import Group, buid_object_from_row as build_group_from_row
from flood.models.user import User, buid_object_from_row as build_user_from_row

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)

dateformat = '%Y-%m-%dT%H:%M:%S'


class UserGroup(Base):
    __tablename__ = 'users_groups'

    user_id = Column(mysql.VARCHAR(length=64), ForeignKey(User.id, ondelete='CASCADE'), primary_key=True)
    group_id = Column(mysql.VARCHAR(length=64), ForeignKey(Group.id, ondelete='CASCADE'), primary_key=True)

    user = relationship(User, backref=backref("employee_assoc", cascade="all, delete-orphan"))
    group = relationship(Group, backref=backref("department_assoc", cascade="all, delete-orphan"))

    def __repr__(self):
        return f"<UserGrop(user={self.user_id}, group={self.group_id})>"

    def to_dict(self):
        result = {
            "user_id": self.user_id,
            "group_id": self.group_id,
        }
        return result


def buid_object_from_row(row):
    user_grop = UserGroup(
        user_id=row.get("user_id", None),
        group_id=row.get("group_id", None),
    )
    return user_grop


@db_session
def associate(session, group, user):
    _logger.info(
        "ASSOCIATING: group: {} user: {}".format(group.to_dict(), user.to_dict()),
    )
    user_group = session.query(UserGroup).filter(UserGroup.user_id == user.id).filter(UserGroup.group_id == group.id).first()
    if user_group is None:
        result = UserGroup(
            user_id=user.id,
            group_id=group.id
        )
        session.add(result)

        session.flush()
        r = to_dict(result)
        session.commit()
        return buid_object_from_row(r)
    else:
        _logger.info(
            "ASSOCIATION_ALREADY_EXISTS",
        )
        return buid_object_from_row(to_dict(user_group))


@db_session
def get_user_groups(session, user):
    _logger.info(
        "GETTING_USER_GROUPS: ".format(user.to_dict()),
    )
    groups = []

    result = session.query(UserGroup).join(Group).filter(UserGroup.user_id == user.id).all()

    if result is None:
        return groups
    else:
        for row in result:
            r = to_dict(row.group)
            groups.append(build_group_from_row(r))
        return groups
