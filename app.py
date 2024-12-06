from iebank_api import app
from applicationinsights.flask.ext import AppInsights
import os
import logging

# Initialize Application Insights
try:
    app.config['APPINSIGHTS_INSTRUMENTATIONKEY'] = os.getenv('APPLICATIONINSIGHTS_CONNECTION_STRING', '')
    if not app.config['APPINSIGHTS_INSTRUMENTATIONKEY']:
        raise ValueError("Application Insights connection string is not set.")
    
    appinsights = AppInsights(app)
    app.logger.info("Application Insights successfully initialized.")
except Exception as e:
    app.logger.error(f"Failed to initialize Application Insights: {e}")

if __name__ == '__main__':
    # Set up logging for development and debugging
    log_level = logging.DEBUG if os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1', 't'] else logging.INFO
    logging.basicConfig(level=log_level)

    # Determine debug mode from environment variables
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']
    app.logger.info(f"Starting app in {'debug' if debug_mode else 'production'} mode.")
    app.run(debug=debug_mode)
