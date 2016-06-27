# -*- coding: utf-8 -*-
import datetime
import re
import json
import pytz
import requests

BOM = '\xef\xbb\xbf'

def collect(options):
    data = {}
    resp = requests.get(options['api_endpoint'], params={
        'action': 'query',
        'list': 'recentchanges',
        'rclimit': 100,
        'meta': 'siteinfo',
        'siprop': 'statistics',
        'format': 'json'
    }, timeout=20).content
    if resp.startswith(BOM):
        resp = resp[len(BOM):]
    resp = json.loads(resp)
    data['page_count'] = resp['query']['statistics']['pages']
    changes = []
    for change in resp['query']['recentchanges']:
        changes.append(pytz.utc.localize(datetime.datetime.strptime(change['timestamp'], '%Y-%m-%dT%H:%M:%SZ')))
    data['changes'] = changes
    return data
