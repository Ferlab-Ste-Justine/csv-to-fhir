from parse import parse_row


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
               'extension[0].extension[1].valueBoolean': True
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
                    {'url': 'proband', 'valueBoolean': True}
                ]
            }
        ]

    }
