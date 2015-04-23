# -*- coding: utf-8 -*-
import datetime
import re
import pytz
import requests

KST = pytz.timezone('Asia/Seoul')

def http_get(url, **kwargs):
    return requests.get(url, headers={'User-Agent': 'Mozilla/5.0 ()'}, timeout=10, **kwargs)

PAGE_COUNT_MACRO = '[[PageCount]]'

def collect(options):
    # TODO: support generic MoniWiki
    assert options['theme'] == 'rigveda'
    data = {}
    resp = http_get(options['rc_url'], params={'action': 'raw'})
    prefix = None
    for line in resp.text.splitlines():
        if PAGE_COUNT_MACRO in line:
            prefix = line.split(PAGE_COUNT_MACRO, 1)[0]
            break
    assert prefix is not None
    resp = http_get(options['rc_url'])
    match = re.search(re.escape(prefix) + '(\d+)', resp.text)
    data['page_count'] = int(match.group(1))
    changes = []
    cur_year = datetime.datetime.now().year
    for match in re.findall(r"<td class='date'>(\d{2})-(\d{2}) \[(\d{2}):(\d{2})\]</td>", resp.text):
        month, day, hour, minute = map(int, match)
        # 올해로 가정
        changes.append(KST.localize(datetime.datetime(cur_year, month, day, hour, minute)))
    data['changes'] = changes
    return data
