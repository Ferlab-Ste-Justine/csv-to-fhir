import os

from app import config


def test_load():
    os.environ['config.fhir.auth.client_id'] = 'myclientid'
    os.environ['config.fhir.auth.client_secret'] = 'myclientsecret'

    assert config.load('test_config.yml') == {
        'fhir': {
            'url': 'http://localhost:8080',
            'auth': {
                'client_id': 'myclientid',
                'client_secret': 'myclientsecret'
            }
        }
    }
