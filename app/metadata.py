import argparse
import json
from datetime import datetime

from app import config
from app.parse import parse_row
from app.spreadsheet import load


def translateStatus(status:str):
    if status == 'POS':
        return 'AFF'
    elif status == 'NEG':
        return 'UNF'
    else:
        return 'UNK'

def formatBirthDate(d:str):
    return datetime.strptime(d, '%Y-%m-%d').strftime('%d/%m/%Y')

def main(file, output):
    print(f'Import {file} started')
    conf = config.load(file)
    patients = load_tab(conf, 'Patient')
    persons = load_tab(conf, 'Person')
    observations = load_tab(conf, 'Obs_codeabableConcept')
    analysis_sr = load_tab(conf, 'SR_analysis')
    sequencing_sr = load_tab(conf, 'SR_sequencing')
    lab_additional = load_tab(conf, 'Lab_additionnal')
    # print(analysis_sr)
    # print(sequencing_sr)
    # print(lab_additional)
    diseases_status_by_patient = {
        o['subject']['reference'].replace("Patient/", ""): o['interpretation'][0]['coding'][0]['code'] for o in
        observations if 'code' in o and 'code' in o['code']['coding'][0] and o['code']['coding'][0]['code'] == 'DSTA'}
    mrn_ep_by_patient = {
        p['id'].replace("Patient/", ""): {'mrn': p['identifier'][0]['value'],
                                          'ep': p['identifier'][0]['assigner']['reference'].replace('Organization/',
                                                                                                    '')} for p
        in patients}
    person_by_patient = {p['link'][0]['target']['reference'].replace("Patient/", ""): {'birthDate': p['birthDate'],
                                                                                       'firstName':
                                                                                           p['name'][0]['given'][0],
                                                                                       'lastName':
                                                                                           p['name'][0]['family'],
                                                                                       'sex': p['gender'],
                                                                                       'ramq': p['identifier'][0][
                                                                                           'value']} for
                         p in persons}
    panel_code_by_patient = {sr['subject']['reference'].replace("Patient/", ""): sr['code']['coding'][0]['code'] for sr
                            in sequencing_sr}

    analysis = []
    for l in lab_additional:
        pid = l['patient_id']
        aliquot_id = l['labAliquotId']
        ep = mrn_ep_by_patient[pid]['ep']
        e = {
            'patient': {
                'firstName': person_by_patient[pid]['firstName'],
                'lastName': person_by_patient[pid]['lastName'],
                'sex': person_by_patient[pid]['sex'],
                'birthDate': formatBirthDate(person_by_patient[pid]['birthDate']),
                'ep': ep,
                'designFamily': l['designFamily'],
                'status': translateStatus(diseases_status_by_patient[pid]),
                'ramq': person_by_patient[pid]['ramq'],
                'mrn': mrn_ep_by_patient[pid]['mrn']
            },
            'ldm': f'LDM-{ep}',
            'ldmSampleId': l['ldmSampleId'],
            'ldmSpecimenId': l['ldmSpecimenId'],
            'specimenType': 'NBL',
            'sampleType': 'DNA',
            'bodySite': '87612001',
            'ldmServiceRequestId': l['ldmServiceRequestId'],
            'labAliquotId': aliquot_id,
            'panelCode': panel_code_by_patient[pid],
            'files': {
                'cram': f'{aliquot_id}.cram',
                'crai': f'{aliquot_id}.cram.crai',
                'snv_vcf': f'{aliquot_id}.hard-filtered.gvcf.gz',
                'snv_tbi': f'{aliquot_id}.hard-filtered.gvcf.gz.tbi',
                'cnv_vcf': f'{aliquot_id}.cnv.vcf.gz',
                'cnv_tbi': f'{aliquot_id}.cnv.vcf.gz.tbi',
                'supplement': f'{aliquot_id}.QC.tgz'
            }


        }
        if 'familyMember' in l:
            e['patient']['familyMember'] = l['familyMember']
        if 'familyId' in l:
            e['patient']['familyId'] = l['familyId']
        analysis.append(e)

    print(analysis)
    with open("template_metadata/metadata.json", "r") as f:
        metadata_template = f.read()
        metadata_template = metadata_template.replace("$analyses", json.dumps(analysis, indent=4, ensure_ascii=False))
        with open(f"{output}/metadata.json", "w+") as o:
            o.write(metadata_template)


def load_tab(conf, tab_name):
    rows = load(conf['file']['spreadsheetId'], conf['file']['credentialFile'], tab_name)
    headers = rows.pop(0)
    result = []
    for row in rows:
        definition = {header: row[idx] if len(row) >= idx + 1 else None for idx, header in enumerate(headers)}
        result.append(parse_row(definition))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Configuration file')
    parser.add_argument('-o', '--output', help='Output for TF files')
    args = parser.parse_args()
    main(args.file, args.output)
