from iebank_api import app
from applicationinsights import TelemetryClient
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize Application Insights TelemetryClient
connection_string = os.getenv('APPLICATIONINSIGHTS_CONNECTION_STRING', '')
if not connection_string:
    logging.error("Application Insights connection string is not set.")
    telemetry_client = None
else:
    telemetry_client = TelemetryClient(connection_string)
    logging.info("Application Insights TelemetryClient initialized.")

@app.route('/test-telemetry', methods=['GET'])
def test_telemetry():
    if telemetry_client:
        telemetry_client.track_event("TestEvent", {"property": "TestValue"})
        telemetry_client.flush()  # Ensure the event is sent immediately
        return {"message": "Test event sent to Application Insights"}
    else:
        return {"error": "TelemetryClient is not initialized"}, 500

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']
    app.run(debug=debug_mode)
