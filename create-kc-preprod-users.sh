# this script generate keycloak configuration based on qa/staging (nanuq) google sheet.
# you must create a creds/credentials.json file with the csv-to-fhir secret in order to work
export PYTHONPATH=.
pip3 install -r requirements.txt
python3 app/users.py -f defaults/nanuq.yml -o . -p Clin2019!