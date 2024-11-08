import pytest
from iebank_api.models import Account, User
from iebank_api import db, app



@pytest.fixture
def testing_client(scope='module'):
    with app.app_context():
        db.create_all()
        user = User('johndoe', 'mypassword')
        db.session.add(user)
        db.session.commit()

        account = Account('Test Account', '€', 'Spain', 1)
        db.session.add(account)
        db.session.commit()

    with app.test_client() as testing_client:
        yield testing_client

    with app.app_context():
        db.drop_all()
