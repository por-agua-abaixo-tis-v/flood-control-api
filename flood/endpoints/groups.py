#!/usr/bin/env python
# -*- coding: utf-8 -*

import flood.models.group as group_model

from flask import Blueprint, jsonify, request
from flood.utils import body_validations
from flood.endpoints import endpoints_exception

import logging
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)


blueprint = Blueprint('groups', __name__)


@blueprint.route('/groups', methods=['GET', 'OPTIONS'])
def get_groups():
    result = []
    groups = group_model.list()
    if groups is not None:
        for group in groups:
            result.append(group.to_dict())
    return jsonify(result), 200


@blueprint.route('/groups', methods=['POST'])
def post_group():
    body = request.json
    body_validations.validate_group(body)
    group = group_model.create(body)
    return jsonify(group.to_dict()), 200


@blueprint.route('/groups/<group_id>', methods=['GET', 'OPTIONS'])
def get_group(group_id):
    group = group_model.get(group_id)
    if group is None:
        raise endpoints_exception(404, "GROUP_NOT_FOUND")
    return jsonify(group.to_dict()), 200


@blueprint.route('/groups/<group_id>', methods=['DELETE'])
def delete_group(group_id):
    group = group_model.get(group_id)
    if group is None:
        raise endpoints_exception(404, "GROUP_NOT_FOUND")

    group_model.delete(group)
    return jsonify(group.to_dict()), 200



