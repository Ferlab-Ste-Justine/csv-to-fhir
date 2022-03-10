import yaml
import os

from deepmerge import always_merger

from app.parse import parse_row

_CONFIG_PATHS_CHECKLIST = [
    ['fhir', 'oauth', 'url'],
    ['fhir', 'oauth', 'client_id'],
    ['file', 'spreadsheetId'],
    ['fhir', 'oauth', 'client_secret'],
    ['fhir', 'url']
]

def _check_conf_path(conf, path_keys):
    elem = conf
    for key in path_keys:
        try:
            elem = elem[key]
        except KeyError:
            print("Config error: %s does not exist" % ".".join(path_keys))
            exit(1)

def _check(conf):
    for conf_path in _CONFIG_PATHS_CHECKLIST:
        _check_conf_path(conf, conf_path)

def load(f):
    with open(f, "r") as stream:
        from_file = yaml.safe_load(stream)
        from_environ = {k.removeprefix('config.'): v for k, v in os.environ.items() if k.startswith('config.')}
        from_environ = parse_row(from_environ)
        conf = always_merger.merge(from_file, from_environ)
        _check(conf)
        return conf
