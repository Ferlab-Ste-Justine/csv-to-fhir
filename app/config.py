import yaml
import os

from deepmerge import always_merger

ENV_CONFIG_SEPARATOR = '__'

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

def check(conf):
    for conf_path in _CONFIG_PATHS_CHECKLIST:
        _check_conf_path(conf, conf_path)

def dictionarize_env(env_vars, separator, transform):
    result = {}
    for key, val in env_vars:
        fields = key.split(separator)
        fields = map(transform, fields)
        current_dic = result
        for idx, field in enumerate(fields):
            if idx == (len(fields) - 1):
                current_dic[field] = val
            else:
                if field not in current_dic:
                    current_dic[field] = {}
                current_dic = current_dic[field]
    return result


def load(f):
    env_separator = '__'
    config_start = 'config' + env_separator
    with open(f, "r") as stream:
        from_file = yaml.safe_load(stream)
        from_environ = {k.removeprefix(config_start): v for k, v in os.environ.items() if k.startswith(config_start)}
        from_environ = dictionarize_env(from_environ, env_separator, lambda x: x.lower())
        conf = always_merger.merge(from_file, from_environ)
        return conf
