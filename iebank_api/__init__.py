from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
# from sqlalchemy import text
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

migrate = Migrate(app, db) # to handle db migrations with flask-migrate

from iebank_api.models import create_default_admin

with app.app_context():
    db.create_all()

    # Create the default admin user
    create_default_admin(
        app.config['DEFAULT_ADMIN_USERNAME'],
        app.config['DEFAULT_ADMIN_PASS']
    )
CORS(app)

from iebank_api import routes
