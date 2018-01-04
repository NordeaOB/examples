from example_app import app
import requests
import json

def generate_access_token():
    """
    First we get the code to generate the access token
    """
    client_id = app.config['CLIENT_ID']
    client_secret = app.config['CLIENT_SECRET']
    api_uri = app.config['API_URI']
    redirect_uri = app.config['REDIRECT_URI']

    endpoint = 'v1/authentication'
    payload = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'state': ''
    }
    r = requests.get(api_uri + endpoint, params=payload)
    if not r.status_code == requests.codes.ok:
        raise Exception(r.text)
    response = r.json()
    code = response['args']['code']

    """
    Next step is to generate the access token
    """
    endpoint = 'v1/authentication/access_token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-IBM-Client-Id': client_id,
        'X-IBM-Client-Secret': client_secret
    }

    payload = {
        'code': code,
        'redirect_uri': redirect_uri
    }
    r = requests.post(api_uri + endpoint, data=payload, headers=headers)
    if not r.status_code == requests.codes.ok:
        raise Exception(r.text)

    response = r.json()
    access_token = response['access_token']
    return access_token

def list_accounts(access_token):

    client_id = app.config['CLIENT_ID']
    client_secret = app.config['CLIENT_SECRET']
    api_uri = app.config['API_URI']

    endpoint = 'v2/accounts'
    headers = {
        'X-IBM-Client-Id': client_id,
        'X-IBM-Client-Secret': client_secret,
        'Authorization': 'Bearer {}'.format(access_token)
    }
    r = requests.get(api_uri + endpoint, headers=headers)
    if not r.status_code == requests.codes.ok:
        raise Exception(r.text)
    response = r.json()
    return response

def get_account_details(access_token, account_id):

    client_id = app.config['CLIENT_ID']
    client_secret = app.config['CLIENT_SECRET']
    api_uri = app.config['API_URI']

    endpoint = 'v2/accounts/{}'.format(account_id)
    headers = {
        'X-IBM-Client-Id': client_id,
        'X-IBM-Client-Secret': client_secret,
        'Authorization': 'Bearer {}'.format(access_token)
    }
    r = requests.get(api_uri + endpoint, headers=headers)
    if not r.status_code == requests.codes.ok:
        raise Exception(r.text)
    response = r.json()

    return response

def get_account_transactions(access_token, account_id):

    client_id = app.config['CLIENT_ID']
    client_secret = app.config['CLIENT_SECRET']
    api_uri = app.config['API_URI']

    endpoint = 'v2/accounts/{}/transactions'.format(account_id)
    headers = {
        'X-IBM-Client-Id': client_id,
        'X-IBM-Client-Secret': client_secret,
        'Authorization': 'Bearer {}'.format(access_token)
    }
    r = requests.get(api_uri + endpoint, headers=headers)
    if not r.status_code == requests.codes.ok:
        raise Exception(r.text)
    response = r.json()

    return response

def get_payments(access_token):

    client_id = app.config['CLIENT_ID']
    client_secret = app.config['CLIENT_SECRET']
    api_uri = app.config['API_URI']

    endpoint = 'v2/payments/sepa/'
    headers = {
        'X-IBM-Client-Id': client_id,
        'X-IBM-Client-Secret': client_secret,
        'Authorization': 'Bearer {}'.format(access_token),
        'content-type': 'application/json'
    }
    r = requests.get(api_uri + endpoint, headers=headers)
    if not r.status_code == requests.codes.ok:
        raise Exception(r.text)
    response = r.json()

    return response

def initiate_payment(access_token, payload):

    client_id = app.config['CLIENT_ID']
    client_secret = app.config['CLIENT_SECRET']
    api_uri = app.config['API_URI']

    endpoint = 'v2/payments/sepa'
    headers = {
        'X-IBM-Client-Id': client_id,
        'X-IBM-Client-Secret': client_secret,
        'Authorization': 'Bearer {}'.format(access_token),
        'content-type': 'application/json'
    }


    r = requests.post(api_uri + endpoint, headers=headers, data=json.dumps(payload))
    if not r.status_code == requests.codes.created:
        raise Exception(r.text)
    response = r.json()

    return response

def confirm_payment(access_token, payment_id):
    client_id = app.config['CLIENT_ID']
    client_secret = app.config['CLIENT_SECRET']
    api_uri = app.config['API_URI']

    endpoint = 'v2/payments/sepa/{}/confirm'.format(payment_id)
    headers = {
        'X-IBM-Client-Id': client_id,
        'X-IBM-Client-Secret': client_secret,
        'Authorization': 'Bearer {}'.format(access_token),
        'content-type': 'application/json'
    }


    r = requests.put(api_uri + endpoint, headers=headers)
    if not r.status_code == requests.codes.ok:
        raise Exception(r.text)
    response = r.json()

    return response
