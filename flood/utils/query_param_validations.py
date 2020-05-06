#!/usr/bin/env python
# -*- coding: utf-8 -*

from flood.endpoints import endpoints_exception


def validate_message(args):
    required_keys = ['user_id', 'group_id']
    for key in required_keys:
        if key not in args.keys():
            raise endpoints_exception(400, f"BAD REQUEST: Missing query param {key}")


def validate_group_list_filters(args):
    if 'active' not in args.keys():
        return False
    if args['active'] not in ['true', 'false']:
        raise endpoints_exception(400, f"BAD REQUEST: Invalid value for query param active")
    else:
        return True
