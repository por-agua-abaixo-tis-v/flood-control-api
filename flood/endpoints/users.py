#!/usr/bin/env python
# -*- coding: utf-8 -*

import flood.models.user as user_model
import flood.models.group as group_model
import flood.models.message as message_model
import flood.models.user_groups as user_group_model

from flask import Blueprint, jsonify, request
from flood.utils import body_validations, password_utils, geolocation_utils, jwt_token
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
    user = user_model.delete(user_id)
    if user is None:
        raise endpoints_exception(404, "USER_NOT_FOUND")


    return jsonify(user.to_dict()), 200


####################################
#               AUTH               #
####################################


@blueprint.route('/users/auth', methods=['POST'])
def auth_user():
    result = {}
    body = request.json
    body_validations.validate_auth(body)

    user = user_model.get_by_email(body['email'])

    if user is None:
        raise endpoints_exception(404, "USER_NOT_FOUND")

    if password_utils.convert_md5(body['pswd']) != user.pswd:
        raise endpoints_exception(401, "UNAUTHORIZED")
    else:
        result['user'] = user.to_dict()
        result['token'] = jwt_token.jwt_token(user.id, user.email, user.pswd)
        return jsonify(result), 200


####################################
#            GEOLOCATION           #
####################################


@blueprint.route('/users/<user_id>/geolocation', methods=['POST'])
@jwt_token.token_required
def update_user_geolocation(user_id):
    result = []
    body = request.json
    body_validations.validate_geolocation(body)
    user = user_model.get(user_id)

    if user is None:
        raise endpoints_exception(404, "USER_NOT_FOUND")

    latitude = body.get('latitude')
    longitude = body.get('longitude')
    groups = group_model.list(None)
    for group in groups:
        distance = geolocation_utils.check_range(latitude, longitude, group)
        if distance is not None:
            user_group_model.associate(group, user)
            aux = group.to_dict()
            aux['distance'] = round(distance, 2)
            result.append(aux)

    return jsonify(result), 200


@blueprint.route('/users/<user_id>/groups', methods=['GET', 'OPTIONS'])
@jwt_token.token_required
def get_user_groups(user_id):
    result = []

    user = user_model.get(user_id)

    if user is None:
        raise endpoints_exception(404, "USER_NOT_FOUND")

    latitude = request.args.get('latitude', None)
    longitude = request.args.get('longitude', None)
    groups = user_group_model.get_user_groups(user)

    for group in groups:
        aux = group.to_dict()
        if latitude is not None and longitude is not None:
            aux['distance'] = round(geolocation_utils.check_range(latitude,longitude, group), 2)
        result.append(aux)

    return jsonify(result), 200

####################################
#            MESSAGES              #
####################################


@blueprint.route('/users/<user_id>/messages', methods=['GET', 'OPTIONS'])
@jwt_token.token_required
def get_user_messages(user_id):

    result = []

    start_date = request.args.get('start_date', None)

    user = user_model.get(user_id)

    if user is None:
        raise endpoints_exception(404, "USER_NOT_FOUND")

    groups = user_group_model.get_user_groups(user)
    if len(groups) == 0:
        return jsonify(result), 200

    messages = message_model.get_user_messages(user, groups, start_date)

    if messages is not None:
        for message in messages:
            result.append(message.to_dict())

    return jsonify(result), 200
