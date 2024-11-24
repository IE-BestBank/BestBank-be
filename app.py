from flask import Flask
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
import os

# Initialize Flask app
app = Flask(__name__)

# Instrument Flask with OpenTelemetry
FlaskInstrumentor().instrument_app(app)

# Set up OpenTelemetry Tracer with Azure Monitor Exporter
resource = Resource.create({"service.name": "BestBankBackend"})
tracer_provider = TracerProvider(resource=resource)
exporter = AzureMonitorTraceExporter(
    connection_string=os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
)
span_processor = BatchSpanProcessor(exporter)
tracer_provider.add_span_processor(span_processor)

# Define routes
@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route("/test-monitoring")
def test_monitoring():
    from opentelemetry.trace import get_tracer
    tracer = get_tracer(__name__)
    with tracer.start_as_current_span("test-monitoring-span"):
        print("Test log for Application Insights monitoring triggered via /test-monitoring")
        return "Monitoring log sent!"

if __name__ == "__main__":
    app.run(debug=True)
