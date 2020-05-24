#!/usr/bin/env python
# -*- coding: utf-8 -*

import flood.models.group as group_model

from flask import Blueprint, jsonify, request
from flood.utils import body_validations, query_param_validations, jwt_token
from flood.endpoints import endpoints_exception

import logging
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)


blueprint = Blueprint('groups', __name__)


@blueprint.route('/groups', methods=['GET', 'OPTIONS'])
def get_groups():
    result = []
    if query_param_validations.validate_group_list_filters(request.args):
        if request.args['active'] == 'true':
            groups = group_model.list(True)
        else:
            groups = group_model.list(False)
    else:
        groups = group_model.list(None)

    if groups is not None:
        for group in groups:
            result.append(group.to_dict())
    return jsonify(result), 200


@blueprint.route('/groups', methods=['POST'])
# @jwt_token.token_required
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
# @jwt_token.token_required
def delete_group(group_id):
    group = group_model.delete(group_id)
    if group is None:
        raise endpoints_exception(404, "GROUP_NOT_FOUND")

    return jsonify(group.to_dict()), 200


@blueprint.route('/groups/<group_id>', methods=['PUT'])
# @jwt_token.token_required
def update_group(group_id):
    body = request.json

    group = group_model.update(group_id, body)
    if group is None:
        raise endpoints_exception(404, "GROUP_NOT_FOUND")
    return jsonify(group.to_dict()), 200




