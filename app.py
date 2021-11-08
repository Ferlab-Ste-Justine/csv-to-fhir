import yaml

import oauth
from fhir import build_bundle, bundle_entry, send_bundle
from parse import parse_row
from spreadsheet import load


def load_config(f):
    with open(f, "r") as stream:
        return yaml.safe_load(stream)


def main():
    config = load_config('config.yml')
    bundle_entries = []
    for tab in config['file']['tabs']:
        rows = load(config['file']['spreadsheetId'], config['file']['credentialFile'], tab['name'], tab.get('range'))
        headers = rows.pop(0)
        for row in rows:
            definition = {header: row[idx] if len(row) >= idx + 1 else None for idx, header in enumerate(headers)}
            definition['resourceType'] = tab['resourceType']
            definition['meta'] = {'profile': [tab['profile']]}
            bundle_entries.append(bundle_entry(parse_row(definition)))
    bundle = build_bundle(bundle_entries)
    access_token = None
    if config['fhir'].get('oauth'):
        access_token = oauth.get_access_token(config['fhir']['oauth']['url'], config['fhir']['oauth']['client_id'],
                                              config['fhir']['oauth']['client_secret'])
    print(access_token)
    send_bundle(config['fhir']['url'], bundle, access_token)


if __name__ == '__main__':
    main()
