#!/usr/bin/env python
# -*- coding: utf-8 -*
import jwt
import datetime
import os
from flask import jsonify


def jwt_token(user_id, email, pswd):
    exp_time = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    token = jwt.encode({'user_id': user_id, 'email': email, 'pswd': pswd, 'exp': exp_time}, os.getenv('TOKEN_SECRET'))
    return token.decode('UTF-8')



