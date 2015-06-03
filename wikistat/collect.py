import datetime
import json
import os
import time
import pytz
import yaml
from requests.exceptions import Timeout
from wikistat.engines import mediawiki, wikia, moniwiki, namu

ENGINES = {
    'mediawiki': mediawiki,
    'wikia': wikia,
    'moniwiki': moniwiki,
    'namu': namu,
}

def main(site_config_path, log_dir):
    with open(site_config_path) as fp:
        sites = yaml.load_all(fp.read())
    log_entry = {'stats': {}}
    for site in sites:
        site = dict(site) # copy
        engine = ENGINES[site['engine']]
        try:
            data = engine.collect(site.pop('engine_options', {}))
        except Exception as e:
            print site['id'], str(e)
            log_entry['stats'][site['id']] = {'error': 'error'}
            continue
        nchanges = len(data['changes'])
        assert nchanges >= 1
        t = time.time()
        now = pytz.utc.localize(datetime.datetime.utcfromtimestamp(t))
        period = (now - data['changes'][-1]).total_seconds()
        assert period >= 0
        period_days = float(period) / 60 / 60 / 24
        log_entry['stats'][site['id']] = {
            't': t,
            'page_count': data['page_count'],
            'freq': nchanges / period_days,
        }

    log_entry['t'] = time.time()

    try:
        os.mkdir(log_dir, 0700)
    except OSError:
        pass # already exist
    with open(os.path.join(log_dir, 'wikistat.log.' + datetime.date.today().strftime('%Y%m%d')), 'a') as fp:
        fp.write(json.dumps(log_entry) + '\n')

if __name__ == '__main__':
    main('sites.yml', 'logs')
