# sample_tracer.py

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Define service name (appears in Jaeger)
resource = Resource(attributes={
    "service.name": "python-service"
})

# Configure the tracer provider
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

# Configure the OTLP exporter (pointing to OpenTelemetry Collector running in Docker)
otlp_exporter = OTLPSpanExporter(
    endpoint="http://otel-collector:4317",  # Or "otel-collector:4317" if running inside a container
    insecure=True
)

# Add BatchSpanProcessor to send spans to the collector
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Sample trace
with tracer.start_as_current_span("sample-trace-span"):
    print("✅ Hello, tracing from Python!")
