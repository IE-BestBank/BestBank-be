from iebank_api.models import Account, User
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
