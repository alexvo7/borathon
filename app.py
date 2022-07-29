from crypt import methods
from hashlib import new
from flask import Flask, jsonify, render_template, request, url_for, redirect
# render_template: helper function to render html template
# request: object to access data the user will submit
# url_for(): function to generate urls
# redirect(): function to redirect user back to index page after adding a todo
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.project_database
account_collection = db.account_collection
transactions = db.transactions


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/testing")
def hello_testing():
    return "<p>Hello testing!</p>"


@app.route('/details/<id>', methods=['GET'])
def retrieve_details(id):
    """
    Retrieves customer/account details of an account.

    Outputs balance, status, customer first/last name of account/customer when account number is inputted

    Parameters
    __________
    account_number: str
        The account number in string format

    Examples
    ________
    >>> retrieve_details("1234")
    """
    post = account_collection.find_one({"account_number": id})
    print(post)
    return post


@app.route('/open/', methods=['POST'])
def open_account():
    """
    Open Customer Account.

    Given first and last name, create a new customer and account record with balance = $0.00, account status open.
    return details for this new account.

    Parameters
    __________

    Examples
    ________
    """
    content_type = request.headers.get('Content-Type')
    if content_type == ('application/json'):
        input_json = request.json
        first_name = input_json["first_name"]
        last_name = input_json["last_name"]

        if len(list(account_collection.find())) == 0:
            new_account_id = 1
            new_account_number = 1

        else:
            old_max_account_id = list(account_collection.find().sort("_id", -1).limit(1))
            new_account_id = old_max_account_id[0]["account_number"] + 1
            print(new_account_id)

            old_max_account_number = (list(account_collection.find().sort("account_number", -1).limit(1)))
            new_account_number = old_max_account_number[0]["account_number"] + 1
            print(new_account_number)

        post = {
            "_id": new_account_id,
            "account_number": new_account_number,
            "balance": 0.00,
            "account_status": "open",
            "first_name": first_name,
            "last_name": last_name
        }
        account_collection.insert_one(post)
        print(post)
        return post
    else:
        return 'Content-Type not supported!'


@app.route('/close/', methods=['POST'])
def close_account():
    """
    Close Customer Account

    Given account number, update the account to a closed status

    Parameters
    __________
    account_number: str
        account number

    Examples
    ________
    >>> close_account("123")
    """
    content_type = request.headers.get('Content-Type')
    if content_type == ('application/json'):
        input_json = request.json

        account_number = input_json["account_number"]

        filter = {'account_number': account_number}
        new_values = {"$set": {'account_status': 'closed'}}

        account_collection.update_one(filter, new_values)
        return "Done"
    else:
        return 'Content-Type not supported!'


@app.route('/transaction/', methods=['POST'])
def apply_transaction():
    """
    Apply a Transaction to a Customer Account

    Given account number, transaction amount, and type of transaction ("Debit" or "Credit"),
    create a new transaction record and update account balance accordingly

    Parameters
    __________


    Examples
    ________
    >>>
    """
    content_type = request.headers.get('Content-Type')
    if content_type == ('application/json'):
        input_json = request.json
        account_number = input_json["account_number"]
        transaction_amount = input_json["transaction_amount"]
        transaction_type = input_json["transaction_type"]

        # create new transaction record
        post = {
            "account_number": account_number,
            "transaction_amount": transaction_amount,
            "transaction_type": transaction_type
        }
        transactions.insert_one(post)

        # update account balance
        filter = {'account_number': account_number}
        if transaction_type == "debit":
            transaction_amount *= -1

        current_account = dict(account_collection.find_one({"account_number": account_number}))
        new_account_balance = current_account["balance"] + transaction_amount

        new_values = {"$set": {'balance': new_account_balance}}

        account_collection.update_one(filter, new_values)

        return post


if __name__ == '__main__':
    app.run()