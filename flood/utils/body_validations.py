#!/usr/bin/env python
# -*- coding: utf-8 -*

from flood.endpoints import endpoints_exception

def validate_group(body):
    required_keys = ['name']
    for key in required_keys:
        if key not in body.keys():
            raise endpoints_exception(400, f"BAD REQUEST: Missing {key} on body")


def validate_message(body):
    required_keys = ['text']
    for key in required_keys:
        if key not in body.keys():
            raise endpoints_exception(400, f"BAD REQUEST: Missing {key} on body")


def validate_user(body):
    required_keys = ['email', 'pswd', 'name']
    for key in required_keys:
        if key not in body.keys():
            raise endpoints_exception(400, f"BAD REQUEST: Missing {key} on body")