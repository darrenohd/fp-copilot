import os
from opentelemetry import trace
from phoenix.otel import register
from opentelemetry.trace import Status, StatusCode
from openinference.instrumentation.openai import OpenAIInstrumentor

def initialize_tracer():
    # Configure Phoenix tracer
    tracer_provider = register(
        project_name="feature-positioning-copilot",  # Default is 'default'
    )
    
    # Initialize OpenAI instrumentation
    OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)
    
    # Set environment variables for Phoenix
    os.environ["PHOENIX_API_KEY"] = "f320c64dbf1666453f7:7519083"
    os.environ["PHOENIX_CLIENT_HEADERS"] = f"api_key={os.environ['PHOENIX_API_KEY']}"
    os.environ["PHOENIX_COLLECTOR_ENDPOINT"] = "https://app.phoenix.arize.com"
    
    return tracer_provider

def create_span(name: str, attributes: dict = None):
    """Create a new span for tracing"""
    tracer = trace.get_tracer(__name__)
    span = tracer.start_span(name)
    
    if attributes:
        for key, value in attributes.items():
            span.set_attribute(key, str(value))
    
    return span

def end_span(span, status: str = "success", error: Exception = None):
    """End a span with status and optional error information"""
    if status == "success":
        span.set_status(Status(StatusCode.OK))
    else:
        span.set_status(Status(StatusCode.ERROR))
        if error:
            span.record_exception(error)
    span.end() 