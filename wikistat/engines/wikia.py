# -*- coding: utf-8 -*-
import datetime
import re
import pytz
import requests

def collect(options):
    data = {}
    resp = requests.get('http://%s/api/v1/Mercury/WikiVariables' % options['domain']).json()
    wiki_id = resp['data']['id']
    resp = requests.get('http://www.wikia.com/api/v1/Wikis/Details', params={'ids': str(wiki_id)}).json()
    data['page_count'] = resp['items'][str(wiki_id)]['stats']['articles']
    resp = requests.get('http://%s/api/v1/Activity/RecentlyChangedArticles?limit=100' % options['domain']).json()
    changes = []
    for change in resp['items']:
        changes.append(pytz.utc.localize(datetime.datetime.utcfromtimestamp(change['timestamp'])))
    data['changes'] = changes
    return data
