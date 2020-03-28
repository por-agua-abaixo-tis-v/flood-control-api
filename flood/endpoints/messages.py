#!/usr/bin/env python
# -*- coding: utf-8 -*

import flood.models.message as message_model

from flask import Blueprint, jsonify, request
from flood.utils import body_validations
from flood.endpoints import endpoints_exception

import logging
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)


blueprint = Blueprint('messages', __name__)


@blueprint.route('/messages', methods=['GET', 'OPTIONS'])
def get_groups():
    result = []
    groups = message_model.list()
    for group in groups:
        result.append(group.to_dict())
    return jsonify(result), 200


@blueprint.route('/messages', methods=['POST'])
def post_group():
    body = request.json
    body_validations.validate_group(body)
    group = message_model.create(body)
    return jsonify(group.to_dict()), 200


@blueprint.route('/messages/<message_id>', methods=['GET', 'OPTIONS'])
def get_group(message_id):
    group = message_model.get(message_id)
    if group is None:
        raise endpoints_exception(404, "GROUP_NOT_FOUND")
    return jsonify(group.to_dict()), 200


@blueprint.route('/messages/<message_id>', methods=['DELETE'])
def delete_group(message_id):
    group = message_model.get(message_id)
    if group is None:
        raise endpoints_exception(404, "GROUP_NOT_FOUND")

    message_model.delete(group)
    return jsonify(group.to_dict()), 200



