# -*- coding: utf-8 -*-
import datetime
import re
import pytz
import requests

def collect(options):
    data = {}
    resp = requests.get(options['api_endpoint'], params={
        'action': 'query',
        'list': 'recentchanges',
        'rclimit': 100,
        'meta': 'siteinfo',
        'siprop': 'statistics',
        'format': 'json'
    }).json()
    data['page_count'] = resp['query']['statistics']['pages']
    changes = []
    for change in resp['query']['recentchanges']:
        changes.append(pytz.utc.localize(datetime.datetime.strptime(change['timestamp'], '%Y-%m-%dT%H:%M:%SZ')))
    data['changes'] = changes
    return data
