# -*- coding: utf-8 -*-
import datetime
import re
import pytz
import requests

KST = pytz.timezone('Asia/Seoul')

def http_get(url):
    return requests.get(url, headers={'User-Agent': 'Mozilla/5.0 ()'}, timeout=10, verify=False)

PAGE_COUNT_MACRO = '[[PageCount]]'

def collect(options):
    data = {}
    resp = http_get('https://namu.wiki/raw/FrontPage')
    prefix = None
    for line in resp.text.splitlines():
        if PAGE_COUNT_MACRO in line:
            prefix = line.split(PAGE_COUNT_MACRO, 1)[0]
            break
    assert prefix is not None
    resp = http_get('https://namu.wiki/w/FrontPage')
    match = re.search(re.escape(prefix) + '(\d+)', resp.text)
    data['page_count'] = int(match.group(1))
    resp = http_get('https://namu.wiki/RecentChanges')
    changes = []
    # TODO: 너무 대충 파싱하나?
    for match in re.findall(r"<td>(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})</td>", resp.text):
        changes.append(KST.localize(datetime.datetime.strptime(match, '%Y-%m-%d %H:%M:%S')))
    data['changes'] = changes
    return data
