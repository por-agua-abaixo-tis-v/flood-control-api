#!/usr/bin/env python
# -*- coding: utf-8 -*

import logging

from flask import Blueprint, jsonify, request

_logger = logging.getLogger(__name__)


blueprint = Blueprint('groups', __name__)


@blueprint.route('/groups', methods=['GET', 'OPTIONS'])
def get_groups():
    return '', 200


@blueprint.route('/groups', methods=['POST'])
def post_group():
    body = request.json
    name = body['name']

