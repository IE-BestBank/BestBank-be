from flask import Flask
import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler
import os
app = Flask(__name__)

# Configure logging for Application Insights
logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(
    connection_string=os.getenv('APPLICATIONINSIGHTS_CONNECTION_STRING')
))
logger.setLevel(logging.INFO)

# Test logging
logger.info("Test log for Application Insights monitoring.")

@app.route("/")
def home():
    return "Hello, Application Insights!"

if __name__ == "__main__":
    app.run(debug=True)
