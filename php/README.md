# PHP examples for the Nordeas Open Banking API

This repo provides PHP examples for the Nordeas Open Banking API.

These examples show how to make API requests, so it is easier to get the idea how the API is meant to be used.

Note that the examples here are not production grade code so, e.g., error handling is not complete.

## Examples

All of these individual examples generate new access token before they do their thing.

For more thorough information about concepts etc. please refer to the documentation found in developer portal.

Calls are originated from calls.php, which uses basic wrapper: NordeaWrapper from nordeawrapper.php

### Account Details

The $nordeawrapper->getAccountDetails method will fetch the account details from the API.

### Generate access token

The $nordeawrapper->generateAccessToken method implements access token generation process.

### Get payments

The $nordeawrapper->getPayments method gets list of payments.

### Initiate payment

The $nordeawrapper->initiatePayment method initiates payment and confirms it.

### List accounts

The $nordeawrapper->listAccounts method lists the accounts.
