#!/usr/bin/env python
# -*- coding: utf-8 -*

import flood.models.group as group_model

from flask import Blueprint, jsonify, request
from flood.utils import body_validations

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
    body_validations.validate_group(body)
    group = group_model.create(body)
    return jsonify(group.to_dict()), 200


@blueprint.route('/groups/<group_id>', methods=['GET', 'OPTIONS'])
def get_group(group_id):
    group = group_model.get(group_id)
    return jsonify(group.to_dict()), 200



