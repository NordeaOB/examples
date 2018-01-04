from example_app import app
from flask import render_template, request, make_response, jsonify, redirect, url_for
import requests
from utils import generate_access_token, list_accounts, get_account_details, get_account_transactions, get_payments, initiate_payment, confirm_payment
from decorators import access_token_required


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/authenticate', methods=['POST', 'GET'])
def credentials():
    if request.method == 'POST':
        access_token = None
        response = 'Access token successfully generated!'
        try:
            access_token = generate_access_token()
        except Exception as e:
            response = "Failed to generate access token: {}".format(e)

        resp = make_response(render_template(
            'authenticate.html', response=response))
        if access_token:
            resp.set_cookie('access_token', access_token)
        return resp
    else:
        access_token = request.cookies.get('access_token')
        if not access_token:
            return render_template('authenticate.html', response='You have not generated access token yet!')
        else:
            return render_template('authenticate.html')


@app.route('/revoke', methods=['POST'])
@access_token_required
def revoke():
    resp = make_response(render_template('revoke.html'))
    resp.set_cookie('access_token', '', expires=0)
    return resp


@app.route('/accounts', methods=['GET'])
@access_token_required
def accounts():
    error = None
    access_token = request.cookies.get('access_token')
    try:
        accounts = list_accounts(access_token)
    except Exception as e:
        error = e

    if error:
        return render_template('accounts.html', error=error)
    else:
        return render_template('accounts.html', accounts=accounts)


@app.route('/account_details', methods=['GET'])
@access_token_required
def account_details():
    account_id = request.args.get('account_id')
    error = None
    access_token = request.cookies.get('access_token')
    try:
        details = get_account_details(access_token, account_id)
    except Exception as e:
        error = e

    if not account_id:
        error = 'Account id url parameter is missing!'

    if error:
        return render_template('account_details.html', error=error)
    else:
        return render_template('account_details.html', details=details)


@app.route('/transactions', methods=['GET'])
@access_token_required
def account_transactions():
    account_id = request.args.get('account_id')
    error = None
    access_token = request.cookies.get('access_token')
    try:
        transactions = get_account_transactions(access_token, account_id)
    except Exception as e:
        error = e

    if not account_id:
        error = 'Account id url parameter is missing!'

    if error:
        return render_template('transactions.html', error=error)
    else:
        return render_template('transactions.html', transactions=transactions)


@app.route('/payments', methods=['GET', 'POST'])
@access_token_required
def payments():
    error = None
    access_token = request.cookies.get('access_token')

    if request.method == 'GET':
        try:
            payments = get_payments(access_token)
            accounts = list_accounts(access_token)
        except Exception as e:
            error = e

        if error:
            return render_template('payments.html', error=error)
        else:
            return render_template('payments.html', payments=payments, accounts=accounts)

    elif request.method == 'POST':
        amount = request.form['amount']
        account_id = request.form['account_id']
        beneficiary = request.form['beneficiary']
        name = request.form['name']
        message = request.form['message']

        if None in [amount, account_id, beneficiary, name, message]:
            error = 'Form data missing!'
        if error:
            return render_template('payments.html', error=error)

        # Geenrate the payload
        payload = {
            "amount": amount,
            "creditor": {
                "account": {
                    "_type": "IBAN",
                    "value": beneficiary
                },
                "message": message,
                "name": name,
                "reference": {
                    "_type": "RF",
                    "value": "RF18539007547034"
                }
            },
            "currency": "EUR",
            "debtor": {
                "_accountId": account_id
            }
        }

        try:
            payment = initiate_payment(access_token, payload)
            accounts = list_accounts(access_token)
            payments = get_payments(access_token)
        except Exception as e:
            error = e

        if error:
            return render_template('payments.html', error=error)
        else:
            return render_template('payments.html', payments=payments, payment=payment, accounts=accounts)


@app.route('/confirm_payment', methods=['POST'])
@access_token_required
def confirm_payments():
    error = None
    access_token = request.cookies.get('access_token')
    try:
        payment_id = request.form['payment_id']
        payment = confirm_payment(access_token, payment_id)
        payments = get_payments(access_token)
        accounts = list_accounts(access_token)
    except Exception as e:
        error = e
    if error:
        return render_template('payments.html', error=error)
    else:
        return redirect(url_for('payments'))
