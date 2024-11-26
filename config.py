import os
import urllib.parse
from azure.identity import DefaultAzureCredential

class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_ECHO = True  # Enable SQLAlchemy debug output
    DEBUG = False
    # Fetch the connection string from the environment, use default as fallback
    APPLICATIONINSIGHTS_CONNECTION_STRING = os.getenv(
        "APPLICATIONINSIGHTS_CONNECTION_STRING"
    )
    if not APPLICATIONINSIGHTS_CONNECTION_STRING:
        raise ValueError("Missing APPLICATIONINSIGHTS_CONNECTION_STRING")
    APPINSIGHTS_INSTRUMENTATIONKEY = os.getenv(
        "APPINSIGHTS_INSTRUMENTATIONKEY"
    )
class LocalConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///local.db'
    DEBUG = True
    DEFAULT_ADMIN_USERNAME = 'admin'
    DEFAULT_ADMIN_PASS = 'password'

class GithubCIConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    DEBUG = True
    DEFAULT_ADMIN_USERNAME = 'admin'
    DEFAULT_ADMIN_PASS = 'password'

class DevelopmentConfig(Config):
    if os.getenv('ENV') == 'dev':
        credential = DefaultAzureCredential()
        SQLALCHEMY_DATABASE_URI = 'postgresql://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
            dbuser=urllib.parse.quote(os.getenv('DBUSER')),
            dbpass=credential.get_token(
            'https://ossrdbms-aad.database.windows.net').token,
            dbhost=os.getenv('DBHOST'),
            dbname=os.getenv('DBNAME')
        )
        DEBUG = True
        DEFAULT_ADMIN_USERNAME = os.getenv('DEFAULT_ADMIN_USERNAME')
        DEFAULT_ADMIN_PASS = os.getenv('DEFAULT_ADMIN_PASS')


class UATConfig(Config):
    if os.getenv('ENV') == 'uat':
        credential = DefaultAzureCredential()
        SQLALCHEMY_DATABASE_URI = 'postgresql://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
        dbuser=urllib.parse.quote(os.getenv('DBUSER')),
        dbpass=credential.get_token(
            'https://ossrdbms-aad.database.windows.net').token,
            dbhost=os.getenv('DBHOST'),
            dbname=os.getenv('DBNAME')
        )
        DEBUG = True
        DEFAULT_ADMIN_USERNAME = os.getenv('DEFAULT_ADMIN_USERNAME')
        DEFAULT_ADMIN_PASS = os.getenv('DEFAULT_ADMIN_PASS')
