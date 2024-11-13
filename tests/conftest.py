import pytest
from iebank_api.models import Account, User
from iebank_api import db, app



@pytest.fixture
def testing_client(scope='module'):
    with app.app_context():
        db.create_all()
        user = User('johndoe', 'mypassword')
        user2 = User('janesmith', 'mypassword')

        db.session.add(user)
        db.session.add(user2)
        db.session.commit()

        user = User.query.filter_by(username='johndoe').first()
        user2 = User.query.filter_by(username='janesmith').first()

        account = Account('Test Account', '€', 'Spain', user.id)
        account2 = Account('Test Account 2', '€', 'Spain', user2.id)
        db.session.add(account)
        db.session.add(account2)
        db.session.commit()

    with app.test_client() as testing_client:
        yield testing_client

    with app.app_context():
        db.drop_all()
