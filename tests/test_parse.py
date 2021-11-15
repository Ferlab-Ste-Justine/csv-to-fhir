from app.parse import parse_row, parse_indice


def test_parse_row():
    patient = {'resourceType': 'Patient',
               'name.given[0]': 'John', 'name.given[1]': 'Frank', 'name.last': 'Doe', 'name.display.text': 'hello',
               'name.display.value': 'world',
               'identifier[0].reference': 'ref1',
               'identifier[0].assigner': 'assigner1',
               'identifier[1].reference': 'ref2',
               'identifier[1].assigner': 'assigner2',
               'extension[0].url': 'http://fhir.cqgc.ferlab.bio/StructureDefinition/family',
               'extension[0].extension[0].url': 'subject',
               'extension[0].extension[0].valueReference.reference': 'QA00001',
               'extension[0].extension[1].url': 'proband',
               'extension[0].extension[1].valueBoolean': 'false'
               }
    assert parse_row(patient) == {
        'resourceType': 'Patient',
        'name': {
            'given': ['John', 'Frank'],
            'last': 'Doe',
            'display': {'text': 'hello', 'value': 'world'}
        },
        'identifier': [
            {'reference': 'ref1', 'assigner': 'assigner1'},
            {'reference': 'ref2', 'assigner': 'assigner2'}
        ],
        'extension': [
            {
                'url': 'http://fhir.cqgc.ferlab.bio/StructureDefinition/family',
                'extension': [
                    {
                        'url': 'subject',
                        'valueReference': {'reference': 'QA00001'},
                    },
                    {'url': 'proband', 'valueBoolean': False}
                ]
            }
        ]

    }


def test_parse_row_extension():
    patient = {'extension[0].url': 'http://fhir.cqgc.ferlab.bio/StructureDefinition/is-proband',
               'extension[0].valueBoolean': 'true',
               'extension[1].url': 'http://fhir.cqgc.ferlab.bio/StructureDefinition/family',
               'extension[1].extension[0].url': 'subject',
               'extension[1].extension[0].valueReference.reference': 'Patient/123'
               }
    assert parse_row(patient) == {
        'extension': [
            {
                'url': 'http://fhir.cqgc.ferlab.bio/StructureDefinition/is-proband',
                'valueBoolean': True
            },
            {
                'url': 'http://fhir.cqgc.ferlab.bio/StructureDefinition/family',
                'extension': [
                    {
                        'url': 'subject',
                        'valueReference': {'reference': 'Patient/123'}
                    }
                ]
            }
        ]

    }


def test_parse_row_valueAge():
    patient = {'extension[0].url': 'http://fhir.cqgc.ferlab.bio/StructureDefinition/age',
               'extension[0].valueAge.value': '1'
               }
    assert parse_row(patient) == {
        'extension': [
            {
                'url': 'http://fhir.cqgc.ferlab.bio/StructureDefinition/age',
                'valueAge': {'value': 1}
            }
        ]

    }


def test_parse_indice():
    assert parse_indice('example[0]') == ('example', 0)
    assert parse_indice('example') == (None, None)
