import json
from spreadsheet import load
from parse import parse_row


def bundle_entry(resource):
    return {
        'resource': resource,
        'request': {
            'method': 'PUT',
            'url': f'{resource["resourceType"]}/{resource["id"]}'
        }
    }


def build_bundle(bundle_entries):
    return {
        "resourceType": "Bundle",
        "type": "transaction",
        "entry": bundle_entries
    }


def main():
    f = open('config.json', )
    config = json.load(f)
    print(config)
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
    print(json.dumps(bundle))


if __name__ == '__main__':
    main()
