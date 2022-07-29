from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient(port=27017)
db = client.borathon
accounts = db.accounts
transactions = db.transactions


@app.route('/')
def hello_world():  # put application's code here
    return jsonify(
        {"hello": "world"}
    )


@app.route('/api/customer/<id>', methods=["GET"])
def get_customer_acc(id):
    return {"hello": "world"}


@app.route('/api/customer/open', methods=["POST"])
def open_acc():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        print(type(json), json)
        # post = accounts.insert_one(
        #     {
        #         ""
        #     }
        # )
    return "Content-Type not supported!"


@app.route('/api/customer/close', methods=["POST"])
def close_acc():
    return {"hello": "world"}


@app.route('/api/customer/apply', methods=["POST"])
def apply_transaction():
    return {"hello": "world"}


@app.route('/customer/', methods=["GET"])
def customer_table():
    return {"hello": "world"}


@app.route('/transaction/', methods=["GET"])
def transaction_table():
    return {"hello": "world"}


if __name__ == '__main__':
    app.run()
