import os
import pathlib

from app import config


def test_load():
    os.environ['config.fhir.auth.client_id'] = 'myclientid'
    os.environ['config.fhir.auth.client_secret'] = 'myclientsecret'
    current_path = pathlib.Path(__file__).parent.resolve()
    assert config.load(f'{current_path}/test_config.yml') == {
        'fhir': {
            'url': 'http://localhost:8080',
            'auth': {
                'client_id': 'myclientid',
                'client_secret': 'myclientsecret'
            }
        }
    }
