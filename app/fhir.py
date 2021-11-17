import json

import requests


def bundle_entry(resource):
    return {
        'resource': resource,
        'fullUrl': f'{resource["resourceType"]}/{resource["id"]}',
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


def send_bundle(fhir_url, bundle, access_token=None):
    headers = {}
    if access_token:
        headers['Authorization'] = f'Bearer {access_token}'
    r = requests.post(fhir_url, json=bundle, headers=headers)
    if r.status_code > 201:
        print(json.dumps(r.json(), indent=True))
    r.raise_for_status()
