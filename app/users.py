import argparse

from app import config
from app.parse import parse_row
from app.spreadsheet import load


def main(file, password, output):
    print(f'Import {file} started')
    conf = config.load(file)
    organizations = load_tab(conf, 'organisation')
    practioners = load_tab(conf, 'practitioner')
    practioners_roles = load_tab(conf, 'practitionerRole')

    #kc_roles = load_tab(conf, 'roles')
    practioners_email = {}
    pr_kc_roles = {}

    for pr in practioners_roles:
        id = pr['practitioner']['reference'].replace('Practitioner/', '')
        if id not in practioners_email.keys():
            practioners_email[id] = pr['telecom'][1]['value']
        role = pr['code'][0]['coding'][0]['code']
        if role == 'doctor':
            role = 'clin_prescriber'
        elif role == '15941008':
            role = 'clin_genetician'
        elif role == '405277009':
            role = 'clin_prescriber'
        else:
            raise ValueError('No mapping for code[0].coding[0].code: ' + role)
        sanitizedRole = 'keycloak_role.' + role + '.id'
        if id not in pr_kc_roles.keys():
            pr_kc_roles[id] = [sanitizedRole]
        elif sanitizedRole not in pr_kc_roles[id]:
            pr_kc_roles[id].append(sanitizedRole)
    '''
    pr_kc_roles = {}
    for r in kc_roles:
        roles = [f'keycloak_role.{v}.id' for v in r['roles'].split(',')]
        if r['id'] not in pr_kc_roles.keys():
            pr_kc_roles[r['id']] = roles
        else:
            pr_kc_roles[r['id']] += roles
    '''
    # print(pr_kc_roles)
    with open("templates_hcl/user_template.hcl", "r") as f:
        user_template = f.read()

    users = ""

    for p in practioners:
        user = user_template
        user = user.replace("$username", p['id'].lower())
        user = user.replace("$password", password)
        user = user.replace("$practitioner_id", p['id'])
        user = user.replace("$email", practioners_email[p['id']].lower())   # keycloak doesn't like upper case in email
        user = user.replace("$first_name", p['name'][0]['given'][0])
        user = user.replace("$last_name", p['name'][0]['family'])
        user_roles = ['data.keycloak_role.manage_account.id', 'data.keycloak_role.view_profile.id']
        if p['id'] in pr_kc_roles.keys() and pr_kc_roles[p['id']]:
            user_roles += pr_kc_roles[p['id']]
        user = user.replace("$roles", ",".join(user_roles))
        users += user
        users += '\n'
    with open(f"{output}/clin_practitioners.tf", "w+") as f:
        f.write(users)

    groups = {}
    for pr in practioners_roles:
        pr_id = pr['practitioner']['reference'].replace('Practitioner/', '')
        org = pr['organization']['reference'].replace('Organization/', '')
        if org not in groups.keys():
            groups[org] = [f'keycloak_user.{pr_id}.username']
        else:
            groups[org] += [f'keycloak_user.{pr_id}.username']

    with open("templates_hcl/group_template.hcl", "r") as f:
        group_template = f.read()
    group_f = ""
    for group_id, members in groups.items():
        group = group_template
        group = group.replace("$organization_name", group_id)
        group = group.replace("$organization_id", group_id)
        group = group.replace("$members", ",\n    ".join(members))
        group_f +=group
        group_f += '\n'

    with open(f"{output}/clin_organizations.tf", "w+") as f:
        f.write(group_f)

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
    parser.add_argument('-p', '--password', help='Users Password')
    parser.add_argument('-o', '--output', help='Output for TF files')
    args = parser.parse_args()
    main(args.file, args.password, args.output)
