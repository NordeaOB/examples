#!/usr/bin/env python3
import requests
from generate_access_token import generate_access_token
import json

API_URI = 'https://api.nordeaopenbanking.com/'
CLIENT_ID = 'your client id here'
CLIENT_SECRET = 'your client secret here'

if __name__ == '__main__':
    endpoint = 'v2/payments/sepa'
    access_token = generate_access_token()
    headers = {
        'X-IBM-Client-Id': CLIENT_ID,
        'X-IBM-Client-Secret': CLIENT_SECRET,
        'Authorization': 'Bearer {}'.format(access_token),
        'X-Response-Scenarios': 'AuthorizationSkipAccessControl',
        'content-type': 'application/json'
    }
    payload = {
        "amount": "621000.45",
        "creditor": {
            "account": {
                "_type": "IBAN",
                "value": "FI1350001520000081"
            },
            "message": "This is a message, 123!",
            "name": "Beneficiary name",
            "reference": {
                "_type": "RF",
                "value": "RF18539007547034"
            }
        },
        "currency": "EUR",
        "debtor": {
            "_accountId": "FI6593857450293470-EUR"
        }
    }
    r = requests.post(API_URI + endpoint, headers=headers,
                      data=json.dumps(payload))
    if not r.status_code == requests.codes.created:
        raise Exception(r.text)
    response = r.json()
    payment_id = response['response']['_id']
    # print the payment id
    print(payment_id)

    endpoint = 'v2/payments/sepa/{}/confirm'.format(payment_id)
    r = requests.put(API_URI + endpoint, headers=headers)
    # print the payment response
    response = r.json()
    print(response)
