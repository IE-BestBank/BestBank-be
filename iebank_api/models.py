from iebank_api import db
from datetime import datetime
import string, random
import bcrypt # library for hashing passwords




class User(db.Model):
    __tablename__ = 'user' # This is used to explicitly set the name of the table in the database that will store instances of this class

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String(32), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    accounts = db.relationship('Account', backref='user', lazy=True) # each user can hold multiple accounts

    def __repr__(self):
        return '<User %r>' % self.username

    def __init__(self, username, password, is_admin=False):
        self.username = username
        self.set_password(password)
        self.is_admin = is_admin
        self.accounts = [self.default_account()] if not is_admin else []

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        # Check the provided password against the stored hash
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def default_account(self):
        return Account(name=self.username, currency="€", country="Spain", user_id=self.id)



class Account(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    account_number = db.Column(db.String(20), nullable=False, unique=True)
    balance = db.Column(db.Float, nullable=False, default = 0.0)
    currency = db.Column(db.String(1), nullable=False, default="€")
    status = db.Column(db.String(10), nullable=False, default="Active")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    country = db.Column(db.String(15), nullable=False, default="No Country Selected")

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Event %r>' % self.account_number

    def __init__(self, name, currency, country, user_id):
        self.name = name
        self.account_number = ''.join(random.choices(string.digits, k=20))
        self.currency = currency
        self.balance = 0.0
        self.status = "Active"
        self.country = country
        self.user_id = user_id

    def deposit(self, amount):
        self.balance += amount

    def transfer(self, amount, receiver_account: 'Account'):
        self.balance -= amount
        receiver_account.balance += amount

class Transaction(db.Model):
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Foreign keys for sender and receiver accounts
    sender_account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    receiver_account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=True)

    # Relationships to access sender and receiver accounts
    sender_account = db.relationship('Account', foreign_keys=[sender_account_id], backref='sent_transactions')
    receiver_account = db.relationship('Account', foreign_keys=[receiver_account_id], backref='received_transactions')

    def __repr__(self):
        return '<Transaction %r>' % self.id

    def __init__(self, amount, sender_account_id, receiver_account_id):
        self.amount = amount
        self.sender_account_id = sender_account_id
        self.receiver_account_id = receiver_account_id


def create_default_admin(username, password):
    admin = User.query.filter_by(username=username).first()
    if not admin:
        # Create the default admin user
        admin = User(
            username=username,
            password=password,
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("Default admin account created.")
    else:
        print("Admin account already exists.")
