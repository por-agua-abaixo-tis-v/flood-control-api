#!/usr/bin/env python
# -*- coding: utf-8 -*

from datetime import datetime

from sqlalchemy import between, func
from sqlalchemy.schema import Column
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.dialects import mysql
from sqlalchemy.sql import text
from sqlalchemy import and_

from flood.models import db_session, Base, get_id, to_dict

import logging
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
    created_at = Column(
        TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=False, index=True
    )
    # updated_at = Column(
    #     TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'),
    #     server_onupdate=text('CURRENT_TIMESTAMP'), nullable=False, index=True
    # )

    def __repr__(self):
        return f"<Group(id={self.id}, name={self.name})>"

    def to_dict(self):
        result = {
            "id": self.id,
            "name": self.name,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "created_at": None
            # "updated_at": None
        }
        if self.created_at is not None:
            result['created_at'] = self.created_at.isoformat()
        # if self.updated_at is not None:
        #     result['updated_at'] = self.updated_at.isoformat()

        return result

def buid_object_from_row(row):
    group = Group(
        name=row.get("name", None),
        id=row.get("id", None),
        latitude=row.get("latitude", None),
        longitude=row.get("longitude", None),
    )
    if "created_at" in row.keys():
        group.created_at = datetime.strptime(row["created_at"], dateformat)
    # if "updated_at" in row.keys():
    #     group.updated_at = datetime.strptime(row["updated_at"], dateformat)

    return group

@db_session
def create(session, group):
    _logger.info(
        "CREATING_GROUP_MODEL: {}".format(group),
    )
    result = Group(
        name=group.get("name")
    )
    session.add(result)
    session.flush()
    r = to_dict(result)
    return buid_object_from_row(r)

@db_session
def list(session):
    _logger.info(
        "LISNTING_GROUP_MODEL",
    )

    data = []

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
def delete(session, group):
    _logger.info(
        "DELETING_GROUP_MODEL: {}".format(group.to_dict()),
    )
    x = session.query(Group).get(group.id)
    session.delete(x)