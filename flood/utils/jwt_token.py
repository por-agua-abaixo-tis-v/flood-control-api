#!/usr/bin/env python
# -*- coding: utf-8 -*
import jwt
import datetime
import os
from flood.endpoints import endpoints_exception
from flood.utils import query_param_validations
import flood.models.user as user_model
from flask import request
from functools import wraps


def jwt_token(user_id, email, pswd):
    exp_time = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    token = jwt.encode({'user_id': user_id, 'email': email, 'pswd': pswd, 'exp': exp_time}, os.getenv('TOKEN_SECRET'))
    return token.decode('UTF-8')


def jwt_decode(token):
    try:
        payload = jwt.decode(token, os.getenv('TOKEN_SECRET'))
    except jwt.exceptions.ExpiredSignatureError:
        raise endpoints_exception(403, "TOKEN HAS EXPIRED")
    except jwt.exceptions.InvalidSignatureError:
        raise endpoints_exception(401, "UNAUTHORIZED")
    except jwt.exceptions.InvalidTokenError:
        raise endpoints_exception(403, "INVALID TOKEN")

    return payload


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = query_param_validations.validate_token(request.args)
        payload = jwt_decode(token)
        user = user_model.get(payload['user_id'])

        if user is None:
            raise endpoints_exception(404, "USER_NOT_FOUND")

        if payload['pswd'] != user.pswd:
            raise endpoints_exception(401, "UNAUTHORIZED")

        return f(*args, **kwargs)

    return decorated

