#!/usr/bin/env python
# -*- coding: utf-8 -*

import logging
from datetime import datetime

from sqlalchemy.dialects import mysql
from sqlalchemy.schema import Column
from sqlalchemy.sql import text
from sqlalchemy.types import TIMESTAMP

from flood.endpoints import endpoints_exception
from flood.models import db_session, Base, get_id, to_dict

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)

dateformat = '%Y-%m-%dT%H:%M:%S'


class Group(Base):
    __tablename__ = 'groups'

    id = Column(
        mysql.VARCHAR(length=64), default=get_id, primary_key=True
    )
    name = Column(
        mysql.VARCHAR(length=128), nullable=False
    )
    latitude = Column(
        mysql.DOUBLE(), nullable=True
    )
    longitude = Column(
        mysql.DOUBLE(), nullable=True
    )
    range = Column(
        mysql.INTEGER, nullable=True
    )
    active = Column(
        mysql.BOOLEAN, nullable=True
    )
    severity = Column(
        mysql.VARCHAR(length=64), nullable=True
    )
    created_at = Column(
        TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=False, index=True
    )

    def __repr__(self):
        return f"<Group(id={self.id}, name={self.name})>"

    def to_dict(self):
        result = {
            "id": self.id,
            "name": self.name,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "range": self.range,
            "active": self.active,
            "severity": self.severity,
            "created_at": None
        }
        if self.created_at is not None:
            result['created_at'] = self.created_at.isoformat()

        return result


def buid_object_from_row(row):
    group = Group(
        name=row.get("name", None),
        id=row.get("id", None),
        latitude=row.get("latitude", None),
        longitude=row.get("longitude", None),
        range=row.get("range", None),
        active=row.get("active", None),
        severity=row.get("severity", None)
    )
    if "created_at" in row.keys():
        group.created_at = datetime.strptime(row["created_at"], dateformat)
    if group.latitude:
        group.latitude = float(group.latitude)
    if group.longitude:
        group.longitude = float(group.longitude)

    return group


@db_session
def create(session, group):
    _logger.info(
        "CREATING_GROUP_MODEL: {}".format(group),
    )
    result = Group(
        name=group.get("name"),
        latitude=group.get("latitude", None),
        longitude=group.get("longitude", None),
        range=group.get("range", 2),
        active=group.get("active", False),
        severity=group.get("severity", 'low')
    )
    session.add(result)

    session.flush()
    r = to_dict(result)
    session.commit()
    return buid_object_from_row(r)


@db_session
def list(session, active):
    _logger.info(
        "LISNTING_GROUP_MODEL",
    )

    data = []
    if active is not None:
        result = session.query(Group).filter(Group.active == active)
    else:
        result = session.query(Group).all()

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
        "GETTING_GROUP_MODEL: {}".format(id),
    )
    result = session.query(Group).get(id)
    if result is None:
        return None
    else:
        r = to_dict(result)
        return buid_object_from_row(r)


@db_session
def delete(session, group_id):
    _logger.info(
        "DELETING_GROUP_MODEL: {}".format(group_id),
    )
    x = session.query(Group).get(group_id)
    r = to_dict(x)
    session.delete(x)
    session.commit()
    return buid_object_from_row(r)



@db_session
def update(session, group_id, body):
    _logger.info(
        "UPDATING_GROUP_MODEL: {}".format(group_id),
    )
    group = session.query(Group).get(group_id)
    if group is None:
        return None
    else:
        group.name = body.get("name", group.name)
        group.latitude = body.get("latitude", group.latitude)
        group.longitude = body.get("longitude", group.longitude)
        group.range = body.get("range", group.range)
        group.active = body.get("active", group.active)
        group.severity = body.get("severity", group.severity)
        r = to_dict(group)
        return buid_object_from_row(r)
