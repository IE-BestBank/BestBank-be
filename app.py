from iebank_api import app

# Import the `azure.monitor.opentelemetry` package.
from azure.monitor.opentelemetry import configure_azure_monitor

# Import the tracing API from the `opentelemetry` package.
from opentelemetry import trace
import json

# Load the connection string from appinsights.json
with open("appinsights.json", "r") as f:
    config = json.load(f)
    connection_string = config["connectionString"]

# Configure Azure Monitor with the loaded connection string
configure_azure_monitor(connection_string=connection_string)

# Start the Flask application
if __name__ == "__main__":
    app.run(debug=True)
