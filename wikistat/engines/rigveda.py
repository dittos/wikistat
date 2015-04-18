# -*- coding: utf-8 -*-
import datetime
import re
import pytz
import requests

KST = pytz.timezone('Asia/Seoul')

def collect(options):
    data = {}
    resp = requests.get('http://rigvedawiki.net/r1/wiki.php/RecentChanges/more', headers={'User-Agent': 'Mozilla/5.0 ()'})
    match = re.search(u'리그베다 위키에는 현재 총 (\d+)개의 페이지가 등록되어 있습니다.', resp.text)
    data['page_count'] = int(match.group(1))
    changes = []
    cur_year = datetime.datetime.now().year
    for match in re.findall(r"<td class='date'>(\d{2})-(\d{2}) \[(\d{2}):(\d{2})\]</td>", resp.text):
        month, day, hour, minute = map(int, match)
        # 올해로 가정
        changes.append(KST.localize(datetime.datetime(cur_year, month, day, hour, minute)))
    data['changes'] = changes
    return data
