import requests


def get_access_token(url, client_id, client_secret):
    response = requests.post(
        url,
        data={'grant_type': 'client_credentials', 'client_id': client_id, 'client_secret': client_secret}
    )
    response.raise_for_status()
    return response.json()["access_token"]
