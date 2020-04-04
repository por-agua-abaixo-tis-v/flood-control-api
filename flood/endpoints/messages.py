#!/usr/bin/env python
# -*- coding: utf-8 -*

import flood.models.message as message_model
import flood.models.group as group_model
import flood.models.user as user_model
from flask import Blueprint, jsonify, request
from flood.utils import body_validations, query_param_validations
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

    message = message_model.create(body['text'], user, group)
    return jsonify(message.to_dict()), 200


@blueprint.route('/messages/<message_id>', methods=['GET', 'OPTIONS'])
def get_message(message_id):
    message = message_model.get(message_id)
    if message is None:
        raise endpoints_exception(404, "GROUP_NOT_FOUND")
    return jsonify(message.to_dict()), 200


@blueprint.route('/messages/<message_id>', methods=['DELETE'])
def delete_message(message_id):
    message = message_model.get(message_id)
    if message is None:
        raise endpoints_exception(404, "GROUP_NOT_FOUND")

    message_model.delete(message)
    return jsonify(message.to_dict()), 200



