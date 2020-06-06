#!/usr/bin/env python
# -*- coding: utf-8 -*

from flood.endpoints import endpoints_exception

request_cache = {}
cache_size = 500

def add_to_cache_processing(request_id):
    if len(request_cache) >= cache_size:
        request_cache.pop(list(request_cache.keys())[0])
    request_cache[request_id] = 'processing'


def check_processing_or_complete(request_id):
    if request_id:
        if request_id not in request_cache.keys():
            add_to_cache_processing(request_id)
            return True
        elif request_cache[request_id] == 'failed':
            request_cache[request_id] = 'processing'
            return True
        elif request_cache[request_id] == 'processing' or request_cache[request_id] == 'complete':
            raise endpoints_exception(400, f"BAD REQUEST: Request {request_cache[request_id]}")


def complete_request(request_id):
    if request_id:
        request_cache[request_id] = 'complete'

def fail_request(request_id):
    if request_id:
        request_cache[request_id] = 'complete'
