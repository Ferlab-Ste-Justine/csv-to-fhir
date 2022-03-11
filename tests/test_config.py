import os
import pathlib

from app import config


def test_load():
    os.environ['CONFIG__FHIR__AUTH__CLIENT_ID'] = 'myclientid'
    os.environ['CONFIG__FHIR__AUTH__CLIENT_SECRET'] = 'myclientsecret'
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
