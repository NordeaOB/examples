#!/usr/bin/env python3
import requests
from generate_access_token import generate_access_token
import json

API_URI = 'https://api.nordeaopenbanking.com/'
CLIENT_ID = 'your client id here'
CLIENT_SECRET = 'your client secret here'

if __name__ == '__main__':
    endpoint = 'v3/payments/domestic'
    access_token = generate_access_token()
    headers = {
        'X-IBM-Client-Id': CLIENT_ID,
        'X-IBM-Client-Secret': CLIENT_SECRET,
        'Authorization': 'Bearer {}'.format(access_token),
        'X-Response-Scenarios': 'AuthorizationSkipAccessControl',
        'content-type': 'application/json'
    }

    payload = {
        "amount" : "100.12",
  "currency" : "DKK",
  "debtor" : {
    "account" : {
      "value" : "DK6120301544118028",
      "_type" : "IBAN",
      "currency" : "DKK"
    }
  },
  "creditor" : {
    "account" : {
      "currency": "DKK",
      "value" : "DK3420301544117544",
      "_type" : "IBAN"
    },
    "name" : "Creditor name",
    "message" : "wow",
    "reference" : {
      "value" : "RF11223344",
      "_type" : "RF"
    }
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
