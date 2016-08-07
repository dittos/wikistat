# -*- coding: utf-8 -*-
import datetime
import re
import pytz
import requests

KST = pytz.timezone('Asia/Seoul')

def http_get(url):
    return requests.get(url, headers={'User-Agent': 'Mozilla/5.0 ()'}, timeout=10, verify=False)

def collect(options):
    data = {}
    resp = http_get('https://namu.wiki/w/%EB%82%98%EB%AC%B4%EC%9C%84%ED%82%A4:%ED%86%B5%EA%B3%84')
    match = re.search(u'<tr>\s*<td.*?>.*?전체 문서.*?</td><td.*?>.*?(\d+).*?</td>\s*</tr>', resp.text.split(u'문서 통계', 1)[1])
    data['page_count'] = int(match.group(1))
    resp = http_get('https://namu.wiki/RecentChanges')
    changes = []
    # TODO: 너무 대충 파싱하나?
    for match in re.findall(r"<td>\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}+0900)\s*</td>", resp.text, re.M):
        changes.append(KST.localize(datetime.datetime.strptime(match, '%Y-%m-%d %H:%M:%S')))
    data['changes'] = changes
    return data
