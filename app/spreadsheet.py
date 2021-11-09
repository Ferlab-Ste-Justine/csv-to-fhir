from googleapiclient.discovery import build
from google.oauth2 import service_account
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


def load(spredsheet_id, credentials_file, tab_name, tab_range=None):
    range_name = tab_name
    if tab_range:
        range_name += f'!{tab_range}'

    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    credentials = service_account.Credentials.from_service_account_file(
        credentials_file, scopes=SCOPES)

    service = build('sheets', 'v4', credentials=credentials)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spredsheet_id,
                                range=range_name).execute()
    return result.get('values', [])

