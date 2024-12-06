from iebank_api import app
from applicationinsights.flask.ext import AppInsights
import os

# Initialize Application Insights
app.config['APPINSIGHTS_INSTRUMENTATIONKEY'] = os.getenv('APPLICATIONINSIGHTS_CONNECTION_STRING', '')
appinsights = AppInsights(app)

if __name__ == '__main__':
    # Determine debug mode from environment variables
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']
    app.run(debug=debug_mode)
