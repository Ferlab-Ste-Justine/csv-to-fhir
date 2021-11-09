import oauth
import config
from fhir import build_bundle, bundle_entry, send_bundle
from parse import parse_row
from spreadsheet import load


def main():
    conf = config.load('config.yml')
    bundle_entries = []
    for tab in conf['file']['tabs']:
        rows = load(conf['file']['spreadsheetId'], conf['file']['credentialFile'], tab['name'], tab.get('range'))
        headers = rows.pop(0)
        for row in rows:
            definition = {header: row[idx] if len(row) >= idx + 1 else None for idx, header in enumerate(headers)}
            definition['resourceType'] = tab['resourceType']
            definition['meta'] = {'profile': [tab['profile']]}
            bundle_entries.append(bundle_entry(parse_row(definition)))
    bundle = build_bundle(bundle_entries)
    access_token = None
    if conf['fhir'].get('oauth'):
        access_token = oauth.get_access_token(conf['fhir']['oauth']['url'], conf['fhir']['oauth']['client_id'],
                                              conf['fhir']['oauth']['client_secret'])
    print(access_token)
    send_bundle(conf['fhir']['url'], bundle, access_token)


if __name__ == '__main__':
    main()
