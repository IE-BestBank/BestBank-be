from flask import Flask
from opencensus.ext.azure.log_exporter import AzureLogHandler
import logging
import os

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')  # Adjust based on your environment

# Set up Application Insights logging
if app.config['APPLICATIONINSIGHTS_CONNECTION_STRING']:
    logger = logging.getLogger(__name__)
    logger.addHandler(AzureLogHandler(
        connection_string=app.config['APPLICATIONINSIGHTS_CONNECTION_STRING']
    ))
    logger.setLevel(logging.INFO)
    logger.info('Application Insights configured successfully.')
else:
    print("Application Insights connection string is not set.")
