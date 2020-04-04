#!/usr/bin/env python
# -*- coding: utf-8 -*

import hashlib


def convert_md5(passwd):
    m = hashlib.md5()
    m.update(passwd.encode('utf-8'))
    return m.hexdigest()
