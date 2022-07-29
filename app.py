from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient(port=27017)
db = client.borathon
accounts = db.account
transactions = db.transactions


@app.route('/')
def hello_world():  # put application's code here
    return jsonify(
        {"hello": "world"}
    )


@app.route('/api/customer/<id>', methods=["GET"])
def get_customer_acc(id):
    return {"hello": id}


@app.route('/api/customer/open', methods=["POST"])
def open_acc():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        json = request.json
        if len(list(accounts.find())) > 0:
            acc_n = accounts.find.sort({"AccountNumber": -1}).limit(1) + 1
        else:   # if db is empty
            acc_n = 0

        post = accounts.insert_one(
            {
                "FirstName": json["FirstName"],
                "LastName": json["LastName"],
                "Status": "open",
                "AccountNumber": acc_n
            }
        )
        return jsonify(
            {"status": f"account #{acc_n} for {json['FirstName']} {json['LastName']} successfully created"}
        )

    return "Content-Type not supported!"


@app.route('/api/customer/close/', methods=["POST"])
def close_acc():
    acc_n = request.args.get("accNumber")
    query = {"AccountNumber": acc_n}
    acc = accounts.find_one(query)
    if acc:
        accounts.update_one(query, {"$set": {"Status": "closed"}})
        return jsonify(
            {"status": f"successfully closed account {acc_n}"}
        )

    return jsonify(
        {"status": "account not found"}
    )


@app.route('/api/customer/apply', methods=["POST"])
def apply_transaction():
    return {"hello": "world"}


# debugging functions

@app.route('/customer/', methods=["GET"])
def customer_table():
    return db.accounts.find()


@app.route('/transaction/', methods=["GET"])
def transaction_table():
    return db.transactions.find()


@app.route('/delete/customer/', methods=["DELETE"])
def delete_customer():
    return db.accounts.deleteMany({})


@app.route('/delete/transaction/', methods=["DELETE"])
def delete_transactions():
    return db.transactions.deleteMany({})


if __name__ == '__main__':
    app.run()
