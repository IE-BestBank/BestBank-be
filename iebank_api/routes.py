from flask import Flask, request
from iebank_api import db, app
from iebank_api.models import Account, User, Transaction

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/skull', methods=['GET'])
def skull():
    text = 'Hi! This is the BACKEND SKULL! 💀 '

    text = text +'<br/>Database URL:' + db.engine.url.database
    if db.engine.url.host:
        text = text +'<br/>Database host:' + db.engine.url.host
    if db.engine.url.port:
        text = text +'<br/>Database port:' + db.engine.url.port
    if db.engine.url.username:
        text = text +'<br/>Database user:' + db.engine.url.username
    if db.engine.url.password:
        text = text +'<br/>Database password:' + db.engine.url.password
    return text


@app.route('/accounts', methods=['POST'])
def create_account():
    name = request.json['name']
    currency = request.json['currency']
    country = request.json['country']
    user_id = request.json['user_id']

    account = Account(name, currency, country, user_id)
    db.session.add(account)
    db.session.commit()
    return format_account(account)

@app.route('/accounts', methods=['GET'])
def get_accounts():
    accounts = Account.query.all()
    return {'accounts': [format_account(account) for account in accounts]}

@app.route('/accounts/<int:id>', methods=['GET'])
def get_account(id):
    account = Account.query.get(id)
    return format_account(account)

@app.route('/accounts/<int:id>', methods=['PUT'])
def update_account(id):
    account = Account.query.get(id)
    account.name = request.json['name']
    db.session.commit()
    return format_account(account)

@app.route('/accounts/<int:id>', methods=['DELETE'])
def delete_account(id):
    account = Account.query.get(id)
    db.session.delete(account)
    db.session.commit()
    return format_account(account)



@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return {'users': [format_user(user) for user in users]}


@app.route('/users/register', methods=['POST'])
def register():
    try:
        username = request.json['username']
        password = request.json['password']
        password2 = request.json['password2']

        # check if all fields are provided
        if not username:
            return {'message': 'Username is required!'}, 400
        if not password:
            return {'message': 'Password is required!'}, 400
        if not password2:
            return {'message': 'Password confirmation is required!'}, 400


        # Check if the passwords match
        if password != password2:
            return {'message': 'Passwords do not match!'}, 400


        # Check if username already exists
        exists = User.query.filter_by(username=username).first()
        if exists:
            return {'message': 'Username already exists!'}, 400


        # Create the user
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        # Create a new account for that user, default is set to USD in Spain
        """
            Since we are committing the user to the database before creating the account,
            if something goes wrong creating the account, we need to delete the user from the database.
            The reason why we need to create and commit the user before creating the account is because
            the user's ID needs to be generated to create the account, which only happens when we commit the user.
        """
        try:
            default_account = user.default_account(user.id)
            db.session.add(default_account)
            db.session.commit()  # Commit the default account

        except Exception as account_error:
            # Rollback changes to avoid partial saves and delete the user if account creation fails
            db.session.rollback()
            db.session.delete(user)  # Remove the user from the database
            db.session.commit()
            return {'message': 'An error occurred while creating the default account', 'error': str(account_error)}, 500

        return format_user(user, [default_account])

    except Exception as e:
        db.session.rollback() # Rollback the session in case of an unexpected error
        return {'message': 'An error occurred while registering the user', 'error': str(e)}, 500


@app.route('/users/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']

    user = User.query.filter_by(username=username).first()

    if not user:
        return {'message': 'User not found!'}, 404

    if not user.check_password(password):
        return {'message': 'Invalid password!'}, 401

    return format_user(user)



@app.route('/users/<int:id>', methods=['GET'])
def get_user_accounts(id):
    user = User.query.get(id)
    if not user:
        return {'message': 'User not found!'}, 404


    return format_user(user)


@app.route('/transactions', methods=['POST'])
def make_transaction():
    sender_account_number = request.json['sender_account_number']
    receiver_account_number = request.json['receiver_account_number']
    amount = request.json['amount']

    sender = Account.query.filter_by(account_number=sender_account_number).first()
    receiver = Account.query.filter_by(account_number=receiver_account_number).first()

    if not sender:
        return {'message': 'Sender account not found!'}, 404

    if not receiver:
        return {'message': 'Receiver account not found!'}, 404

    if sender_account_number == receiver_account_number:
        return {'message': 'Sender and receiver accounts cannot be the same!'}, 400

    if sender.balance < amount:
        return {'message': 'Insufficient funds!'}, 400

    sender.transfer(amount, receiver)

    transaction = Transaction(amount=amount, sender_account_id=sender.id, receiver_account_id=receiver.id)
    db.session.add(transaction)
    db.session.commit()

    return {'message': 'Transaction successful!'}


@app.route('/transactions', methods=['GET'])
def get_transactions():
    transactions = Transaction.query.all()
    return {'transactions': [format_transaction(transaction) for transaction in transactions]}


# we need a way to add money to an account, if not its impossible to test the transactions
@app.route("/deposit", methods=["POST"])
def make_deposit():
    account_number = request.json["account_number"]
    amount = request.json["amount"]

    if not account_number:
        return {"message": "Account ID is required!"}, 400
    if not amount:
        return {"message": "Amount is required!"}, 400

    account = Account.query.filter_by(account_number=account_number).first()

    if not account:
        return {"message": "Account not found!"}, 404

    account.deposit(amount)

    db.session.commit()

    return format_account(account)


def format_account(account):
    return {
        'id': account.id,
        'name': account.name,
        'country': account.country,
        'account_number': account.account_number,
        'balance': account.balance,
        'currency': account.currency,
        'status': account.status,
        'created_at': account.created_at,
        'user_id': account.user_id
    }


def format_user(user, accounts=None):
    if not accounts: # when we register the user, the account does not update in time
        accounts = user.accounts

    return {
        'id': user.id,
        'username': user.username,
        'created_at': user.created_at,
        'accounts': [format_account(account) for account in accounts],
        'is_admin': user.is_admin
    }


def format_transaction(transaction):
    sender_account = Account.query.get(transaction.sender_account_id)
    receiver_account = Account.query.get(transaction.receiver_account_id)

    return {
        'id': transaction.id,
        'amount': transaction.amount,
        'timestamp': transaction.timestamp,
        'sender_account': format_account(sender_account),
        'receiver_account': format_account(receiver_account)
    }

    # List of all routes in this file:
    # 1. GET /
    # 2. GET /skull
    # 3. POST /accounts
    # 4. GET /accounts
    # 5. GET /accounts/<int:id>
    # 6. PUT /accounts/<int:id>
    # 7. DELETE /accounts/<int:id>
    # 8. GET /users
    # 9. POST /users/register
    # 10. POST /users/login
    # 11. GET /users/<int:id>
    # 12. POST /transactions
    # 13. GET /transactions
    # 14. POST /deposit
