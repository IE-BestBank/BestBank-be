from iebank_api.models import Account, User, Transaction
# import pytest

def test_create_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the username, password and id fields are defined correctly
    """
    user = User("michaelscott", "scottpassword")
    assert user.username == "michaelscott"
    assert user.check_password("scottpassword")


def test_create_account():
    """
    GIVEN a Account model
    WHEN a new Account is created
    THEN check the name, account_number, balance, currency, status and created_at fields are defined correctly
    """
    account = Account('John Doe', '€', 'Spain', 1)
    assert account.name == 'John Doe'
    assert account.currency == '€'
    assert account.account_number != None
    assert account.balance == 0.0
    assert account.status == 'Active'
    assert account.country == 'Spain'
    assert account.user_id == 1


def test_create_transaction():
    """
    GIVEN a Account model
    WHEN a transfer is made between two accounts
    THEN check the balance of the sender and receiver accounts are updated correctly
    """
    sender = Account('John Doe Account', '€', 'Spain', 1)
    sender.deposit(100.0) # deposit 100.0 to the sender account

    receiver = Account('Jane Smith Account', '€', 'Spain', 2)

    amount = 40.0
    sender.transfer(amount, receiver) # transfer 40.0 from sender to receiver

    transaction = Transaction(amount, sender.id, receiver.id)

    assert transaction.amount == 40.0
    assert transaction.sender_account_id == sender.id
    assert transaction.receiver_account_id == receiver.id
    assert sender.balance == 60.0
    assert receiver.balance == 40.0
