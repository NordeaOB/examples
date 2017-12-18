# Code examples for the Nordeas Open Banking API

This repo provides code examples for the Nordeas Open Banking API.

These examples show how to make API requests, so it is easier to get the idea how the API is meant to be used.

Note that the examples here are not production grade code so, e.g., error handling is not complete.

## Examples

All of these individual examples generate new access token before they do their thing.

For more thorough information about concepts etc. please refer to the documentation found in developer portal.

### Account Details

The `account_details.py` file will fetch the account details from the API.

### Generate access token

The `generate_access_token.py` file implements access token generation process.

It can be run by issuing `python generate_access_token.py` or the `generate_access_token` function can be imported from this file and used.

### Get payments

The `get_payments,py` gets list of payments.

### Initiate payment

The `initiate_payment.py` initiates payment and confirms it.

### List accounts

The `list_accounts.py` lists the accounts.
