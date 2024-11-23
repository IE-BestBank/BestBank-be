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


@app.route('/users/register', methods=['POST'])
def register():
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

    if len(username.split(" ")) > 1:
        return {'message': 'Username cannot have spaces!'}, 400

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

    default_account = user.default_account()
    user.add_acount(default_account)
    db.session.add(default_account)
    db.session.commit()  # Commit the default account

    return format_user(user)


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

@app.route('/transactions/<int:user_id>', methods=['GET'])
def get_user_transactions(user_id):
    user = User.query.get(user_id)
    if not user:
        return {'message': 'User not found!'}, 404

    all_transactions = Transaction.query.all()
    transactions = [transaction for transaction in all_transactions if transaction.sender_account.user_id == user_id or transaction.receiver_account.user_id == user_id]
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


# ADMIN ROUTES
@app.route('/admin/users', methods=['POST'])
def create_user():
    admin_id = request.json['admin_id']
    username = request.json['username']
    password = request.json['password']

    admin = User.query.get(admin_id)
    if not admin or not admin.is_admin:
        return {'message': 'Unauthorized access!'}, 401

    if not username:
        return {'message': 'Username is required!'}, 400
    if not password:
        return {'message': 'Password is required!'}, 400

    if len(username.split(" ")) > 1:
        return {'message': 'Username cannot have spaces!'}, 400

    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()

    default_account = user.default_account()
    user.add_acount(default_account)
    db.session.add(default_account)
    db.session.commit()  # Commit the default account

    return format_user(user)



@app.route('/admin/users/<int:id>', methods=['PUT'])
def update_user(id):
    admin_id = request.json['admin_id']
    new_username = request.json['new_username']
    new_password = request.json['new_password']

    print('new_username:', new_username)
    print('new_password:', new_password)
    admin = User.query.get(admin_id)
    if not admin or not admin.is_admin or admin.id == id:
        return {'message': 'Unauthorized access!'}, 401

    user = User.query.get(id)
    if not user:
        return {'message': 'User not found!'}, 404

    if not new_username and not new_password:
        return {'message': 'No changes provided!'}, 400

    if len(new_username.split(" ")) > 1:
        return {'message': 'Username cannot have spaces!'}, 400

    if new_username and new_username != user.username:
        user.username = new_username

    if new_password and new_password != user.password:
        user.set_password(new_password)

    db.session.commit()
    return format_user(user)


@app.route('/admin/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    admin_id = request.args.get('admin_id')
    admin = User.query.get(admin_id)

    if not admin or not admin.is_admin or admin.id == id:
        return {'message': 'Unauthorized access!'}, 401

    user = User.query.get(user_id)
    if not user:
        return {'message': 'User not found!'}, 404

    for account in user.accounts:
        db.session.delete(account)

    db.session.delete(user)
    db.session.commit()
    return {"message": "User deleted successfully!"}


@app.route('/admin/users', methods=['GET'])
def get_users():
    # admin_id = request.json['admin_id']
    admin_id = request.args.get('admin_id')
    print('admin_id:', admin_id)
    admin = User.query.get(admin_id)
    if not admin or not admin.is_admin:
        return {'message': 'Unauthorized access!'}, 401

    users = User.query.all()

    return {'users': [format_user(user) for user in users if not user.is_admin]}


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
