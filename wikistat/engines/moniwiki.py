# -*- coding: utf-8 -*-
import calendar
import datetime
import re
import pytz
import feedparser
import requests

def http_get(url, **kwargs):
    return requests.get(url, headers={'User-Agent': 'Mozilla/5.0 ()'}, timeout=10, **kwargs)

PAGE_COUNT_MACRO = '[[PageCount]]'

def collect(options):
    data = {}
    resp = http_get(options['rc_url'], params={'action': 'raw'})
    prefix = None
    for line in resp.text.splitlines():
        if PAGE_COUNT_MACRO in line:
            prefix = line.split(PAGE_COUNT_MACRO, 1)[0]
            break
    assert prefix is not None
    # remove bullet syntax
    prefix = re.sub(r'^\*', '', prefix.lstrip()).lstrip()
    resp = http_get(options['rc_url'])
    match = re.search(re.escape(prefix) + '(\d+)', resp.text)
    data['page_count'] = int(match.group(1))
    resp = http_get(options['rc_url'], params={'action': 'atom', 'c': '100'})
    d = feedparser.parse(resp.text)
    changes = []
    for entry in d.entries:
        changes.append(pytz.utc.localize(datetime.datetime.utcfromtimestamp(calendar.timegm(entry.updated_parsed))))
    data['changes'] = changes
    return data
