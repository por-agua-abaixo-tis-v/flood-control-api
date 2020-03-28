#!/usr/bin/env python
# -*- coding: utf-8 -*


from flood.models import is_database_ok
from flask import Blueprint, jsonify, request

import logging
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)


blueprint = Blueprint('status', __name__)


@blueprint.route('/status', methods=['GET', 'OPTIONS'])
def get_status():
    return '', 200


@blueprint.route('/ready', methods=['GET', 'OPTIONS'])
def get_ready():
    result = {
        "APP": "OK",
        "DATABASE": str(is_database_ok())
    }
    return '', 200


