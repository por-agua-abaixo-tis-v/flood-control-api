#!/usr/bin/env python
# -*- coding: utf-8 -*

import flood.models.group as group_model

from flask import Blueprint, jsonify, request

import logging
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)


blueprint = Blueprint('groups', __name__)


@blueprint.route('/groups', methods=['GET', 'OPTIONS'])
def get_groups():
    return '', 200


@blueprint.route('/groups', methods=['POST'])
def post_group():
    body = request.json
    name = body['name']
    group_model.create(body)
    return '', 200


