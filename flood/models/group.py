#!/usr/bin/env python
# -*- coding: utf-8 -*

from datetime import datetime

from sqlalchemy import between, func
from sqlalchemy.schema import Column
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.dialects import mysql
from sqlalchemy.sql import text
from sqlalchemy import and_

from flood.models import db_session, Base, get_id

import logging
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)



class Group(Base):
    __tablename__ = 'groups'

    id = Column(
        mysql.VARCHAR(length=64), default=get_id, primary_key=True
    )
    name = Column(
        mysql.VARCHAR(length=128), nullable=False
    )

    def __repr__(self):
        return "<_Job(id='%s', name=%s)>Be" % (self.id, self.name)

    def to_dict(self):
        result = {
            "id": self.id,
            "name": self.name
        }


@db_session
def create(session, group):
    _logger.info(
        "CREATING_GROUP_MODEL: {}".format(group),
    )

    result = Group(
        name=group.get("name"),
    )

    session.add(result)
    session.flush()

    return result

