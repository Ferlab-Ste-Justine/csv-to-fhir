import oauth
from app import config
from app.fhir import build_bundle, bundle_entry, send_bundle
from app.parse import parse_row
from app.spreadsheet import load
import argparse
import requests

def print_file_params(conf):
    file_params = """
File Parameters:
\tKeycloak Url: %(keycloak_url)s
\tKeycloak Client ID: %(keycloak_client_id)s
\tFhir Url: %(fhir_url)s
\tSpreadsheet ID: %(spreadsheet_id)s
    """ % {
        "keycloak_url": conf['fhir']['oauth']['url'],
        "keycloak_client_id": conf['fhir']['oauth']['client_id'],
        "fhir_url": conf['fhir']['url'],
        "spreadsheet_id": conf['file']['spreadsheetId'],
    }
    print(file_params)

def main(files):
    for file in files:
        print(f'Import {file} started')
        conf = config.load(file)
        config.check(conf)
        print_file_params(conf)
        request_session = requests.Session()
        if 'requests' in conf and 'ca' in conf['requests']:
            request_session.verify = conf['requests']['ca']
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
            access_token = oauth.get_access_token(request_session, conf['fhir']['oauth']['url'], conf['fhir']['oauth']['client_id'],
                                                  conf['fhir']['oauth']['client_secret'],
                                                  conf['fhir']['oauth'].get('uma_audience', None))
        print('Sending bundle')
        send_bundle(request_session, conf['fhir']['url'], bundle, access_token)
        print(f'Import {file} finished')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file',action='append', help='Configuration file')
    args = parser.parse_args()
    main(args.file)
