import requests


def get_access_token(url, client_id, client_secret, uma_audience=None):
    response_access_token = requests.post(
        url,
        data={'grant_type': 'client_credentials', 'client_id': client_id, 'client_secret': client_secret}
    )
    response_access_token.raise_for_status()
    if not uma_audience:
        return response_access_token.json()["access_token"]
    else:
        response = requests.post(
            url,
            headers={'Authorization': f"Bearer {response_access_token.json()['access_token']}"},
            data={'grant_type': 'urn:ietf:params:oauth:grant-type:uma-ticket',
                  'audience': uma_audience}
        )

        response.raise_for_status()
        return response.json()["access_token"]

