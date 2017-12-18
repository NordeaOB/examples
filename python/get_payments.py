#!/usr/bin/env python3
import requests
from generate_access_token import generate_access_token

API_URI = 'https://api.nordeaopenbanking.com/'
CLIENT_ID = 'your client id here'
CLIENT_SECRET = 'your client secret here'

if __name__ == '__main__':
    endpoint = 'v2/payments/sepa/'
    access_token = generate_access_token()
    headers = {
        'X-IBM-Client-Id': CLIENT_ID,
        'X-IBM-Client-Secret': CLIENT_SECRET,
        'Authorization': 'Bearer {}'.format(access_token),
        'X-Response-Scenarios': 'AuthorizationSkipAccessControl',
        'content-type': 'application/json'
    }
    r = requests.get(API_URI + endpoint, headers=headers)
    if not r.status_code == requests.codes.ok:
        raise Exception(r.text)
    response = r.json()
    # print the result we got from the API
    print(response)
