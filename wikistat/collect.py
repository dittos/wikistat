import datetime
import json
import os
import time
import jinja2
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

def main(site_config_path, output_html_path, log_dir):
    with open(site_config_path) as fp:
        sites = yaml.load_all(fp.read())
    results = []
    log_entry = {'stats': {}}
    for site in sites:
        site = dict(site) # copy
        engine = ENGINES[site['engine']]
        try:
            data = engine.collect(site.pop('engine_options', {}))
        except Timeout:
            site['error'] = 'timeout'
            results.append(site)
            continue
        nchanges = len(data['changes'])
        assert nchanges >= 1
        now = pytz.utc.localize(datetime.datetime.utcnow())
        period = (now - data['changes'][-1]).total_seconds()
        assert period >= 0
        period_days = float(period) / 60 / 60 / 24
        site['page_count'] = data['page_count']
        site['freq'] = nchanges / period_days
        results.append(site)
        log_entry['stats'][site['id']] = {
            'page_count': site['page_count'],
            'freq': site['freq'],
        }

    t = time.time()
    log_entry['t'] = t
    loader = jinja2.FileSystemLoader('.')
    env = jinja2.Environment(loader=loader)
    html = env.get_template('template.html').render(
        results=results,
        timestamp=datetime.datetime.fromtimestamp(t),
    )
    with open(output_html_path, 'w') as fp:
        fp.write(html.encode('utf-8'))

    try:
        os.mkdir(log_dir, 0700)
    except OSError:
        pass # already exist
    with open(os.path.join(log_dir, 'wikistat.log.' + datetime.date.today().strftime('%Y%m%d')), 'a') as fp:
        fp.write(json.dumps(log_entry) + '\n')

if __name__ == '__main__':
    main('sites.yml', 'index.html', 'logs')
