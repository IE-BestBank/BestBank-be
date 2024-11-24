import os

class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_ECHO = True  # Enable SQLAlchemy debug output
    DEBUG = False
    # Fetch the connection string from the environment, use default as fallback
    APPLICATIONINSIGHTS_CONNECTION_STRING = os.getenv(
        "APPLICATIONINSIGHTS_CONNECTION_STRING"
    )
    APPINSIGHTS_INSTRUMENTATIONKEY = os.getenv(
        "APPINSIGHTS_INSTRUMENTATIONKEY"
    )
class LocalConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///local.db'
    DEBUG = True
    DEFAULT_ADMIN_USERNAME = 'admin'
    DEFAULT_ADMIN_PASSWORD = 'password'

class GithubCIConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    DEBUG = True
    DEFAULT_ADMIN_USERNAME = 'admin'
    DEFAULT_ADMIN_PASSWORD = 'password'

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
        dbuser=os.getenv('DBUSER'),
        dbpass=os.getenv('DBPASS'),
        dbhost=os.getenv('DBHOST'),
        dbname=os.getenv('DBNAME')
    )
    DEBUG = True
    DEFAULT_ADMIN_USERNAME = os.getenv('DEFAULT_ADMIN_USERNAME')
    DEFAULT_ADMIN_PASSWORD = os.getenv('DEFAULT_ADMIN_PASSWORD')

class UATConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
        dbuser=os.getenv('DBUSER'),
        dbpass=os.getenv('DBPASS'),
        dbhost=os.getenv('DBHOST'),
        dbname=os.getenv('DBNAME')
    )
    DEBUG = True
    DEFAULT_ADMIN_USERNAME = os.getenv('DEFAULT_ADMIN_USERNAME')
    DEFAULT_ADMIN_PASSWORD = os.getenv('DEFAULT_ADMIN_PASSWORD')
