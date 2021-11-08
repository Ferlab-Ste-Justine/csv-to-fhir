import yaml

from fhir import build_bundle, bundle_entry, send_bundle
from parse import parse_row
from spreadsheet import load


def load_config(f):
    with open(f, "r") as stream:
        return yaml.safe_load(stream)


def main():
    config = load_config('config.yml')
    bundle_entries = []
    for t in config['file']['tabs']:
        rows = load(config['file']['spreadsheetId'], config['file']['credentialFile'], t['name'], t.get('range'))
        headers = rows.pop(0)
        for row in rows:
            d = {header: row[idx] for idx, header in enumerate(headers)}
            d['resourceType'] = t['resourceType']
            d['meta'] = {'profile': [t['profile']]}
            bundle_entries.append(bundle_entry(parse_row(d)))
    bundle = build_bundle(bundle_entries)
    send_bundle(config['fhir']['url'], bundle)


if __name__ == '__main__':
    main()
