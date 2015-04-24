import datetime
import json
import os
import jinja2
import yaml

def read_recent_logs(log_dir, max_days):
    today = datetime.date.today()
    for days in reversed(range(max_days)):
        date = today - datetime.timedelta(days=days)
        log_path = os.path.join(log_dir, 'wikistat.log.' + date.strftime('%Y%m%d'))
        if not os.path.exists(log_path):
            continue
        with open(log_path) as fp:
            for line in fp:
                entry = json.loads(line)
                # Normalize old format
                for k, v in entry['stats'].items():
                    if 't' not in v:
                        v['t'] = entry['t']
                yield entry

def main(site_config_path, output_html_path, log_dir):
    with open(site_config_path) as fp:
        sites = yaml.load_all(fp.read())
    recent_logs = list(read_recent_logs(log_dir, 3))
    last_log_entry = recent_logs[-1]
    results = []
    for site in sites:
        stats = last_log_entry['stats'][site['id']]
        site['page_count'] = stats['page_count']
        site['freq'] = stats['freq']
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
    main('sites.yml', 'index.html', 'logs')
