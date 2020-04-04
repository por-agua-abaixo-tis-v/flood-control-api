#!/usr/bin/env python
# -*- coding: utf-8 -*

import flood.models.user as user_model

from flask import Blueprint, jsonify, request
from flood.utils import body_validations, password_utils, query_param_validations
from flood.endpoints import endpoints_exception

import logging
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)


blueprint = Blueprint('users', __name__)


@blueprint.route('/users', methods=['GET', 'OPTIONS'])
def get_users():
    result = []
    users = user_model.list()
    if users is not None:
        for user in users:
            result.append(user.to_dict())
    return jsonify(result), 200


@blueprint.route('/users', methods=['POST'])
def post_user():
    body = request.json
    body_validations.validate_user(body)
    body['pswd'] = password_utils.convert_md5(body['pswd'])
    user = user_model.create(body)
    return jsonify(user.to_dict()), 200


@blueprint.route('/users/<user_id>', methods=['GET', 'OPTIONS'])
def get_user(user_id):
    user = user_model.get(user_id)
    if user is None:
        raise endpoints_exception(404, "USER_NOT_FOUND")
    return jsonify(user.to_dict()), 200


@blueprint.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = user_model.get(user_id)
    if user is None:
        raise endpoints_exception(404, "USER_NOT_FOUND")

    user_model.delete(user)
    return jsonify(user.to_dict()), 200


####################################
#               AUTH               #
####################################


@blueprint.route('/users/<user_id>/auth', methods=['GET', 'OPTIONS'])
def auth_user(user_id):
    query_param_validations.validate_auth(request.args)
    user = user_model.get(user_id)

    if user is None:
        raise endpoints_exception(404, "USER_NOT_FOUND")

    if password_utils.convert_md5(request.args['pswd']) != user.pswd:
        raise endpoints_exception(401, "UNAUTHORIZED")
    else:
        return jsonify(user.to_dict()), 200
