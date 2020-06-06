#!/usr/bin/env python
# -*- coding: utf-8 -*

from flood.endpoints import endpoints_exception

from flood.utils import request_cache_utils

def validate_group(body):
    required_keys = ['name']
    for key in required_keys:
        if key not in body.keys():
            raise endpoints_exception(400, f"BAD REQUEST: Missing {key} on body")
        if body[key] is None:
            raise endpoints_exception(400, f"BAD REQUEST: Missing {key} value on body")

    if 'severity' in body.keys():
        if body['severity'] not in ['low', 'medium', 'high', 'extreme']:
            raise endpoints_exception(400, f"BAD REQUEST: Invalid value for severity. Use low, medium, high or extreme")

    request_cache_utils.check_processing_or_complete(body.get('request_id', None))


def validate_message(body):
    required_keys = ['text']
    for key in required_keys:
        if key not in body.keys():
            raise endpoints_exception(400, f"BAD REQUEST: Missing {key} on body")
        if body[key] is None:
            raise endpoints_exception(400, f"BAD REQUEST: Missing {key} value on body")

    request_cache_utils.check_processing_or_complete(body.get('request_id', None))


def validate_user(body):
    required_keys = ['email', 'pswd', 'name']
    for key in required_keys:
        if key not in body.keys():
            raise endpoints_exception(400, f"BAD REQUEST: Missing {key} on body")
        if body[key] is None:
            raise endpoints_exception(400, f"BAD REQUEST: Missing {key} value on body")

    request_cache_utils.check_processing_or_complete(body.get('request_id', None))

def validate_geolocation(body):
    required_keys = ['latitude', 'longitude']
    for key in required_keys:
        if key not in body.keys():
            raise endpoints_exception(400, f"BAD REQUEST: Missing {key} on body")
        if body[key] is None:
            raise endpoints_exception(400, f"BAD REQUEST: Missing {key} value on body")
    request_cache_utils.check_processing_or_complete(body.get('request_id', None))


def validate_auth(body):
    required_keys = ['email', 'pswd']
    for key in required_keys:
        if key not in body.keys():
            raise endpoints_exception(400, f"BAD REQUEST: Missing {key} on body")
        if body[key] is None:
            raise endpoints_exception(400, f"BAD REQUEST: Missing {key} value on body")

    request_cache_utils.check_processing_or_complete(body.get('request_id', None))
