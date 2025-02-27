import os
from opentelemetry import trace
from phoenix.otel import register
from opentelemetry.trace import Status, StatusCode
from openinference.instrumentation.langchain import LangChainInstrumentor
from contextlib import contextmanager

def initialize_tracer():
    # Configure Phoenix tracer
    tracer_provider = register(
        project_name="feature-positioning-copilot",  # Default is 'default'
    )
    LangChainInstrumentor().instrument(tracer_provider=tracer_provider)
    
    # Set environment variables for Phoenix if not already set
    if not os.environ.get("PHOENIX_API_KEY"):
        raise EnvironmentError("PHOENIX_API_KEY environment variable is not set")
    
    os.environ["PHOENIX_CLIENT_HEADERS"] = f"api_key={os.environ['PHOENIX_API_KEY']}"
    
    if not os.environ.get("PHOENIX_COLLECTOR_ENDPOINT"):
        os.environ["PHOENIX_COLLECTOR_ENDPOINT"] = "https://app.phoenix.arize.com"
    
    return tracer_provider

@contextmanager
def create_span(name, attributes=None, parent_context=None):
    """
    Creates a span for tracing using OpenTelemetry.
    
    Args:
        name: The name of the span
        attributes: Optional dictionary of span attributes
        parent_context: Optional parent span context
        
    Yields:
        The created span
    """
    tracer = trace.get_tracer("feature-positioning-copilot")
    
    # Use parent context if provided
    if parent_context:
        context_manager = tracer.start_as_current_span(name, context=parent_context)
    else:
        context_manager = tracer.start_as_current_span(name)
    
    with context_manager as span:
        if attributes:
            for key, value in attributes.items():
                span.set_attribute(key, value)
        try:
            yield span
            span.set_status(Status(StatusCode.OK))
        except Exception as e:
            span.set_status(Status(StatusCode.ERROR))
            span.record_exception(e)
            raise