from iebank_api import app
from applicationinsights.flask.ext import AppInsights
from applicationinsights import TelemetryClient
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Application Insights connection string
connection_string = os.getenv('APPLICATIONINSIGHTS_CONNECTION_STRING', '')

# Initialize AppInsights for Flask integration
if connection_string:
    app.config['APPINSIGHTS_INSTRUMENTATIONKEY'] = connection_string
    appinsights = AppInsights(app)
    telemetry_client = TelemetryClient(connection_string)
    logging.info("Application Insights initialized with both AppInsights and TelemetryClient.")
else:
    appinsights = None
    telemetry_client = None
    logging.error("Application Insights connection string is not configured.")

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']
    app.run(debug=debug_mode)
