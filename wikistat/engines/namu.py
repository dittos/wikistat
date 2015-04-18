# -*- coding: utf-8 -*-
import datetime
import re
import pytz
import requests

KST = pytz.timezone('Asia/Seoul')

def collect(options):
    data = {}
    resp = requests.get('https://namu.wiki/RecentChanges', headers={'User-Agent': 'Mozilla/5.0 ()'}, timeout=10)
    data['page_count'] = None
    changes = []
    # TODO: 너무 대충 파싱하나?
    for match in re.findall(r"<td>(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})</td>", resp.text):
        changes.append(KST.localize(datetime.datetime.strptime(match, '%Y-%m-%d %H:%M:%S')))
    data['changes'] = changes
    return data
