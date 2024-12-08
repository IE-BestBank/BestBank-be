from iebank_api import app
from iebank_api.models import Account, User, Transaction

# List of all routes in this file:
    # 1. GET /
    # 2. GET /skull
    # 3. POST /accounts
    # 4. GET /accounts
    # 5. GET /accounts/<int:id>
    # 6. PUT /accounts/<int:id>
    # 7. DELETE /accounts/<int:id>
    # 8. POST /users/register
    # 9. POST /users/login
    # 10. GET /users/<int:id>
    # 11. POST /transactions
    # 12. GET /transactions
    # 13. POST /deposit

# / (GET)
def test_hello_world(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = testing_client.get('/')
    assert response.status_code == 200
    assert response.data == b'Hello, World!'


# /skull (GET)
def test_skull(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/skull' page is requested (GET)
    THEN check the response is valid
    """
    response = testing_client.get('/skull')
    assert response.status_code == 200
    assert b'BACKEND SKULL' in response.data

# /wrong_path (GET)
def test_dummy_wrong_path():
    """
    GIVEN a Flask application
    WHEN the '/wrong_path' page is requested (GET)
    THEN check the response is valid
    """
    with app.test_client() as client:
        response = client.get('/wrong_path')
        assert response.status_code == 404

# /accounts (GET)
def test_get_accounts(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is requested (GET)
    THEN check the response is valid
    """
    response = testing_client.get('/accounts')
    assert response.status_code == 200

# /accounts (POST)
def test_create_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is posted to (POST)
    THEN check the response is valid
    """
    response = testing_client.post('/accounts', json={'name': 'John Doe', 'currency': '€', 'country':'Spain', 'user_id': 1})
    assert response.status_code == 200
    assert response.json['name'] == 'John Doe'
    assert response.json['country'] == 'Spain'
    assert response.json['currency'] == '€'


# /accounts/<int:id> (GET)
def test_get_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts/<int:id>' page is requested (GET)
    THEN check the response is valid and the account is retrieved
    """
    _ = testing_client.post('/accounts', json={'name': 'John Doe', 'currency': '€', 'country':'Spain', 'user_id': 1})

    account = Account.query.filter_by(name='John Doe')[0]
    response = testing_client.get(f'/accounts/{account.id}')
    account = Account.query.get(account.id)

    assert response.status_code == 200
    assert response.json['country'] == account.country


# /accounts/<int:id> (DELETE)
def test_delete_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts/<int:id>' page is deleted (DELETE)
    THEN check the response is valid and the account is deleted
    """
    _ = testing_client.post('/accounts', json={'name': 'John Doe', 'currency': '€', 'country':'Spain', 'user_id': 1})

    account = Account.query.filter_by(name='John Doe')[0]
    response = testing_client.delete(f'/accounts/{account.id}')
    assert response.status_code == 200

    accounts = Account.query.filter_by(name='John Doe').all()
    assert accounts == []

# /accounts/<int:id> (PUT)
def test_update_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts/<id>' page is updated (PUT) with valid data
    THEN check the response is valid
    """

    # at least one member has to be created
    response = testing_client.post('/accounts', json={'name': 'John Doe Personal', 'country': 'Spain', 'currency': '€', 'user_id': 1})
    assert response.status_code == 200
    account_data = response.get_json()
    account_id = account_data['id']

    # check the account has been created with the initial values
    get_response = testing_client.get(f'/accounts/{account_id}')
    assert get_response.status_code == 200
    data = get_response.get_json()
    assert data['name'] == 'John Doe Personal'
    assert data['country'] == 'Spain'
    assert data['currency'] == '€'

    # check the values are updated to the new values
    put_response = testing_client.put(f'/accounts/{account_id}', json={'name': 'John Doe Expenses'})
    assert response.status_code == 200
    json_data = put_response.get_json()

    assert json_data['name'] == 'John Doe Expenses'
    assert json_data['country'] == 'Spain'
    assert json_data['currency'] == '€'




# /users/register (POST)
def test_register_user(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/users/register' page is posted to (POST)
    THEN check the response is valid
    """
    response = testing_client.post('/users/register', json={'username': 'johnnydoe', 'password': 'mypassword', 'password2': 'mypassword'})
    user = User.query.filter_by(username='johnnydoe').first()

    assert response.status_code == 200
    assert user.username == 'johnnydoe'
    assert user.check_password('mypassword')
    assert len(user.accounts) != 0  # at least one account is created

# /users/register (POST)
def test_register_user_invalid_password(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/users/register' page is posted to (POST) with invalid password
    THEN check the response is valid
    """
    response = testing_client.post('/users/register', json={'username': 'johnnydoe', 'password': 'mypassword', 'password2': 'mypassword2'})
    assert response.status_code == 400
    assert response.json['message'] == 'Passwords do not match!'


# /users/login (POST)
def test_login_user(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/users/login' page is posted to (POST)
    THEN check the response is valid
    """
    response = testing_client.post('/users/login', json={'username': 'johndoe', 'password': 'mypassword'}) # use credentials from conftest.py

    assert response.status_code == 200
    assert response.json['username'] == 'johndoe'
    assert len(response.json['accounts']) != 0

# /users/login (POST)
def test_login_user_invalid(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/users/login' page is posted to (POST) with invalid credentials
    THEN check the response is valid
    """
    response = testing_client.post('/users/login', json={'username': 'johndoe', 'password': 'somethingrandom'}) # use credentials from conftest.py

    assert response.status_code == 401
    assert response.json['message'] == 'Invalid password!'

# /users/<int:id> (GET)
def test_get_user(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/users/<int:id>' page is requested (GET)
    THEN check the response is valid
    """
    create_response = testing_client.post('/users/register', json={'username': 'johnsmith', 'password': 'mypassword', 'password2': 'mypassword'})
    assert create_response.status_code == 200

    data = create_response.get_json()

    user = User.query.filter_by(username=data['username']).first()

    assert user is not None

    response = testing_client.get('/users/' + str(user.id))
    assert response.status_code == 200
    assert response.json['username'] == 'johnsmith'
    assert user.check_password('mypassword')



# /deposit (POST)
def test_deposit(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/deposit' page is posted to (POST)
    THEN check the response is valid
    """
    response = testing_client.post('/accounts', json={'name': 'John Doe', 'currency': '€', 'country':'Spain', 'user_id': 1})
    assert response.status_code == 200
    data = response.get_json()

    account = Account.query.filter_by(name=data['name']).first()

    response = testing_client.post('/deposit', json={'account_number': account.account_number, 'amount': 50})
    assert response.status_code == 200

    account = Account.query.filter_by(name=data['name']).first()
    assert account.balance == 50
    assert account.balance != 49


# /transactions (POST)
def test_make_transaction(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/transactions' page is posted to (POST)
    THEN check the response is valid
    """

    # create sender account and deposit 100
    sender_response = testing_client.post('/accounts', json={'name': 'Sender account', 'currency': '€', 'country':'Spain', 'user_id': 1})
    assert sender_response.status_code == 200
    data = sender_response.get_json()

    sender = Account.query.filter_by(name=data['name']).first()
    assert sender is not None

    deposit_response = testing_client.post('/deposit', json={'account_number': sender.account_number, 'amount': 100})
    assert deposit_response.status_code == 200
    assert deposit_response.json['balance'] == 100

    # create receiver account
    receiver_response = testing_client.post('/accounts', json={'name': 'Receiver account', 'currency': '€', 'country':'Spain', 'user_id': 2})
    assert receiver_response.status_code == 200
    data = receiver_response.get_json()

    receiver = Account.query.filter_by(name=data['name']).first()
    assert receiver is not None

    response = testing_client.post('/transactions', json={'sender_account_number': sender.account_number, 'receiver_account_number': receiver.account_number, 'amount': 30})
    assert response.status_code == 200


    transaction = Transaction.query.filter_by(sender_account_id=sender.id, receiver_account_id=receiver.id).first()
    assert transaction is not None
    assert transaction.amount == 30
    assert transaction.sender_account.balance == 70
    assert transaction.receiver_account.balance == 30


# /transactions (POST)
def test_make_transaction_insufficient_funds(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/transactions' page is posted to (POST) with insufficient funds
    THEN check the response is valid and the transaction is not made
    """

    # create sender account and deposit 100
    sender_response = testing_client.post('/accounts', json={'name': 'Sender account', 'currency': '€', 'country':'Spain', 'user_id': 1})
    assert sender_response.status_code == 200
    data = sender_response.get_json()

    sender = Account.query.filter_by(name=data['name']).first()
    assert sender is not None

    deposit_response = testing_client.post('/deposit', json={'account_number': sender.account_number, 'amount': 100})
    assert deposit_response.status_code == 200
    assert deposit_response.json['balance'] == 100

    # create receiver account
    receiver_response = testing_client.post('/accounts', json={'name': 'Receiver account', 'currency': '€', 'country':'Spain', 'user_id': 2})
    assert receiver_response.status_code == 200
    data = receiver_response.get_json()

    receiver = Account.query.filter_by(name=data['name']).first()
    assert receiver is not None

    # make a 200 transaction with only 100 in the account
    response = testing_client.post('/transactions', json={'sender_account_number': sender.account_number, 'receiver_account_number': receiver.account_number, 'amount': 200})
    assert response.status_code == 400
    assert response.json['message'] == 'Insufficient funds!'


# /transactions (GET)
def test_get_transactions(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/transactions' page is requested (GET)
    THEN check the response is valid
    """
    response = testing_client.get('/transactions')
    assert response.status_code == 200


# /admin/users (GET)
def test_get_users(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/admin/users' page is requested (GET)
    THEN check the response is valid
    """
    response = testing_client.get('/admin/users?admin_id=1')
    assert response.status_code == 200

# /admin/users (POST)
def test_create_user_admin(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/admin/users' page is posted to (POST)
    THEN check the response is valid
    """
    response = testing_client.post('/admin/users', json={'username': 'testadmin', 'password': 'mypassword', 'admin_id': 1})
    user = User.query.filter_by(username='testadmin').first()

    assert response.status_code == 200
    assert user.username == 'testadmin'
    assert user.check_password('mypassword')
    assert len(user.accounts) == 1  # default account is created

# /admin/users/<int:id> (PUT)
def test_update_username_admin(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/admin/users/<int:id>' page is updated (PUT) with valid data
    THEN check the response is valid
    """

    # create one user
    response = testing_client.post('/admin/users', json={'username': 'testadmin', 'password': 'mypassword', 'admin_id': 1})
    assert response.status_code == 200
    user_data = response.get_json()
    user_id = user_data['id']

    user = User.query.filter_by(username='testadmin').first()
    assert user is not None

    # check the values are updated to the new values
    put_response = testing_client.put(f'/admin/users/{user_id}', json={'new_username': 'testadmin2', 'new_password': '', 'admin_id': 1})
    assert response.status_code == 200
    json_data = put_response.get_json()

    assert json_data['username'] == 'testadmin2'
    assert user.check_password('mypassword')

# /admin/users/<int:id> (PUT)
def test_update_password_admin(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/admin/users/<int:id>' page is updated (PUT) with valid data
    THEN check the response is valid
    """

    # create one user
    response = testing_client.post('/admin/users', json={'username': 'testadmin', 'password': 'mypassword', 'admin_id': 1})
    assert response.status_code == 200
    user_data = response.get_json()
    user_id = user_data['id']

    user = User.query.filter_by(username='testadmin').first()
    assert user is not None
    assert user.check_password('mypassword')

    # check the values are updated to the new values
    put_response = testing_client.put(f'/admin/users/{user_id}', json={'new_username': '', 'new_password': 'mypassword2', 'admin_id': 1})
    assert response.status_code == 200
    json_data = put_response.get_json()

    user = User.query.filter_by(username='testadmin').first() # update the user object
    assert user is not None
    assert json_data['username'] == 'testadmin'
    assert user.check_password('mypassword2')

# /admin/users/<int:id> (PUT)
def test_update_username_password_admin(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/admin/users/<int:id>' page is updated (PUT) with valid data
    THEN check the response is valid
    """

    # create one user
    response = testing_client.post('/admin/users', json={'username': 'testadmin', 'password': 'mypassword', 'admin_id': 1})
    assert response.status_code == 200
    user_data = response.get_json()
    user_id = user_data['id']

    user = User.query.filter_by(username='testadmin').first()
    assert user is not None
    assert user.check_password('mypassword')

    # check the values are updated to the new values
    put_response = testing_client.put(f'/admin/users/{user_id}', json={'new_username': 'testadmin2', 'new_password': 'mypassword2', 'admin_id': 1})
    assert response.status_code == 200
    json_data = put_response.get_json()

    user = User.query.filter_by(username='testadmin2').first() # update the user object
    assert user is not None
    assert json_data['username'] == 'testadmin2'
    assert user.check_password('mypassword2')


# /admin/users/<int:id> (DELETE)
def test_delete_user_admin(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/admin/users/<int:id>' page is deleted (DELETE)
    THEN check the response is valid and the user is deleted
    """
    response = testing_client.post('/admin/users', json={'username': 'testadmin', 'password': 'mypassword', 'admin_id': 1})
    assert response.status_code == 200


    user = User.query.filter_by(username='testadmin').first()
    assert user is not None

    response = testing_client.delete(f'/admin/users/{user.id}?admin_id=1')
    assert response.status_code == 200

    user = User.query.filter_by(username='testadmin').first()
    assert user is None
