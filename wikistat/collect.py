import datetime
import json
import jinja2
import yaml
from requests.exceptions import Timeout
from wikistat.engines import mediawiki, wikia, rigveda, namu

ENGINES = {
    'mediawiki': mediawiki,
    'wikia': wikia,
    'rigveda': rigveda,
    'namu': namu,
}

def main(site_config_path, output_html_path):
    with open(site_config_path) as fp:
        sites = yaml.load_all(fp.read())
    results = []
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
        assert nchanges >= 2
        period = (data['changes'][0] - data['changes'][-1]).total_seconds()
        assert period >= 0
        period_days = float(period) / 60 / 60 / 24
        site['page_count'] = data['page_count']
        site['freq'] = nchanges / period_days
        results.append(site)

    loader = jinja2.FileSystemLoader('.')
    env = jinja2.Environment(loader=loader)
    html = env.get_template('template.html').render(
        results=results,
        timestamp=datetime.datetime.now(),
    )
    with open(output_html_path, 'w') as fp:
        fp.write(html.encode('utf-8'))

if __name__ == '__main__':
    main('sites.yml', 'index.html')
