from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import text
import os

app = Flask(__name__)

# Select environment based on the ENV environment variable
if os.getenv('ENV') == 'local':
    print("Running in local mode")
    app.config.from_object('config.LocalConfig')
elif os.getenv('ENV') == 'dev':
    print("Running in development mode")
    app.config.from_object('config.DevelopmentConfig')
elif os.getenv('ENV') == 'ghci':
    print("Running in github mode")
    app.config.from_object('config.GithubCIConfig')
elif os.getenv('ENV') == 'uat':
    print("Running in github mode")
    app.config.from_object('config.UATConfig')

db = SQLAlchemy(app)

from iebank_api.models import Account

with app.app_context():
    # We need to add the db column user_id to the account table manually
    """ #Ideally, use migrations instead of this
        db.session.execute(text("DROP TABLE IF EXISTS account"))

        # Recreate the table with user_id as a foreign key
        db.session.execute(text(""
                CREATE TABLE account (
                id INTEGER PRIMARY KEY,
                name VARCHAR(32) NOT NULL,
                account_number VARCHAR(20) UNIQUE NOT NULL,
                balance FLOAT NOT NULL DEFAULT 0.0,
                currency VARCHAR(1) NOT NULL DEFAULT '€',
                status VARCHAR(10) NOT NULL DEFAULT 'Active',
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                country VARCHAR(15) NOT NULL DEFAULT 'No Country Selected',
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
            )
        ""))
        db.session.commit()
    """
    db.create_all()
CORS(app)

from iebank_api import routes
