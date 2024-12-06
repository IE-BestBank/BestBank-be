from iebank_api import app
from applicationinsights.flask.ext import AppInsights
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize Application Insights
app.config['APPINSIGHTS_INSTRUMENTATIONKEY'] = os.getenv('APPLICATIONINSIGHTS_CONNECTION_STRING', '')
if app.config['APPINSIGHTS_INSTRUMENTATIONKEY']:
    appinsights = AppInsights(app)  # Initialize AppInsights Flask extension
    logging.info("AppInsights successfully initialized.")
else:
    appinsights = None
    logging.error("Application Insights connection string is not set.")

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']
    app.run(debug=debug_mode)
