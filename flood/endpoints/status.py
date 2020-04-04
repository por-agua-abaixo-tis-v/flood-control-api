#!/usr/bin/env python
# -*- coding: utf-8 -*


import logging

from flask import Blueprint, jsonify

from flood.models import is_database_ok

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
    return jsonify(result), 200


