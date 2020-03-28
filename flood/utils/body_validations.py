#!/usr/bin/env python
# -*- coding: utf-8 -*

from flood.endpoints import endpoints_exception

def validate_group(body):
    required_keys = ['namme']
    for key in required_keys:

        if 'name' not in body.keys():
            raise endpoints_exception(400, f"BAD REQUEST: Missing {key}")
