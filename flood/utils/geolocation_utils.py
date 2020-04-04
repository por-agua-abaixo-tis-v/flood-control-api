#!/usr/bin/env python
# -*- coding: utf-8 -*

from geopy.distance import geodesic

def check_range(latitude, longitude, group):
    user_coorditantes = (latitude, longitude)
    group_coorditantes = (group.latitude, group.longitude)
    distance = geodesic(user_coorditantes, group_coorditantes).kilometers
    if distance < group.range:
        return distance
    else:
        return None
