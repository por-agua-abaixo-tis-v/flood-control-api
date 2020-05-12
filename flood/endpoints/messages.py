#!/usr/bin/env python
# -*- coding: utf-8 -*

import flood.models.message as message_model
import flood.models.group as group_model
import flood.models.user as user_model
import flood.models.user_groups as user_group_model
from flask import Blueprint, jsonify, request
from flood.utils import body_validations, query_param_validations, jwt_token
from flood.endpoints import endpoints_exception

import logging
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)


blueprint = Blueprint('messages', __name__)


@blueprint.route('/messages', methods=['GET', 'OPTIONS'])
def get_messages():
    result = []

    group_id = None
    try:
        group_id = request.args['group_id']
    except KeyError:
        pass

    if group_id is not None:
        group = group_model.get(request.args['group_id'])
        if group is None:
            raise endpoints_exception(404, "GROUP_NOT_FOUND")
        messages = message_model.list_group(group)

    else:
        messages = message_model.list()
    if messages is not None:
        for message in messages:
            result.append(message.to_dict())
    return jsonify(result), 200


@blueprint.route('/messages', methods=['POST'])
@jwt_token.token_required
def post_message():
    body = request.json
    query_param_validations.validate_message(request.args)
    body_validations.validate_message(body)

    group = group_model.get(request.args['group_id'])
    if group is None:
        raise endpoints_exception(404, "GROUP_NOT_FOUND")

    user = user_model.get(request.args['user_id'])
    if user is None:
        raise endpoints_exception(404, "USER_NOT_FOUND")

    user_groups = user_group_model.check_user_group(user, group)
    if user_groups is not None:
        message = message_model.create(body['text'], user, group)
        return jsonify(message.to_dict()), 200
    else:
        raise endpoints_exception(404, "USER_NOT_IN_GROUP_FOUND")


@blueprint.route('/messages/<message_id>', methods=['GET', 'OPTIONS'])
def get_message(message_id):
    message = message_model.get(message_id)
    if message is None:
        raise endpoints_exception(404, "GROUP_NOT_FOUND")
    return jsonify(message.to_dict()), 200


@blueprint.route('/messages/<message_id>', methods=['DELETE'])
@jwt_token.token_required
def delete_message(message_id):
    message = message_model.delete(message_id)
    if message is None:
        raise endpoints_exception(404, "GROUP_NOT_FOUND")

    return jsonify(message.to_dict()), 200



