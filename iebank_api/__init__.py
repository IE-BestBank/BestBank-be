from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
import logging
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from applicationinsights import TelemetryClient  # Use TelemetryClient instead of AppInsights
import os

# Initialize Flask app
app = Flask(__name__)

# Set default environment to 'local'
os.environ['ENV'] = os.getenv('ENV', 'local')

# Select environment based on the ENV environment variable
if os.getenv('ENV') == 'local':
    print("Running in local mode")
    app.config.from_object('config.LocalConfig')
elif os.getenv('ENV') == 'dev':
    print("Running in development mode")
    app.config.from_object('config.DevelopmentConfig')
elif os.getenv('ENV') == 'ghci':
    print("Running in GitHub mode")
    app.config.from_object('config.GithubCIConfig')
elif os.getenv('ENV') == 'uat':
    print("Running in UAT mode")
    app.config.from_object('config.UATConfig')

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Handle DB migrations with flask-migrate
CORS(app)

# **Step 1: Set up OpenTelemetry**
FlaskInstrumentor().instrument_app(app)  # Instrument Flask with OpenTelemetry

resource = Resource.create({"service.name": "iebank_api"})
tracer_provider = TracerProvider(resource=resource)
exporter = AzureMonitorTraceExporter(
    connection_string=os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
)
span_processor = BatchSpanProcessor(exporter)
tracer_provider.add_span_processor(span_processor)

# **Step 2: Configure Telemetry Client**
instrumentation_key = os.getenv("APPINSIGHTS_INSTRUMENTATIONKEY", "YOUR_LEGACY_INSTRUMENTATION_KEY")
telemetry_client = TelemetryClient(instrumentation_key)

# **Step 3: Configure Logging**
logger = logging.getLogger("iebank_api")
logger.setLevel(logging.INFO)

# Add a console handler for local debugging
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)

# Create default admin
from iebank_api.models import create_default_admin

with app.app_context():
    db.create_all()

    # Create the default admin user
    create_default_admin(
        app.config['DEFAULT_ADMIN_USERNAME'],
        app.config['DEFAULT_ADMIN_PASSWORD']
    )

# Define a testing route
@app.route("/test-monitoring")
def test_monitoring():
    try:
        logger.info("Testing monitoring setup")

        # Use the TelemetryClient to send custom telemetry
        telemetry_client.track_request(
            name="Test Monitoring Request",
            url="/test-monitoring",
            success=True,
            response_code=200,
            duration=0
        )
        telemetry_client.flush()  # Ensure the telemetry is sent

        logger.info("Test log for Application Insights monitoring triggered via /test-monitoring")
        return jsonify({"message": "Monitoring log sent!"}), 200
    except Exception as e:
        logger.error(f"Error in /test-monitoring: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Import routes
from iebank_api import routes
